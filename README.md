# 🕸️ RAG Spider Microservice (`rag-spider-ms`)

This is a production-grade, cloud-native web crawler and document asset downloader designed to prepare high-quality content for Retrieval-Augmented Generation (RAG) pipelines. It collects structured HTML content and linked assets like PDFs, CSVs, and Word documents, organizing them into a ready-to-process format.

---

## 🔧 Features

- 🌐 Asynchronous **depth-controlled** web crawling
- 📄 Extraction of **main text** from HTML pages
- 📎 Detection and **download of linked assets** (PDF, CSV, DOCX, etc.)
- 🧱 Organizes output per domain with `linked_assets` metadata
- 🪵 Built-in logging and error handling
- 🐳 Fully Dockerized API powered by FastAPI
- 🧪 Easily testable and ready for CI/CD deployment

---

## 📁 Output Structure

```
output/
├── azcourts.gov.json           # Structured HTML extraction + linked asset metadata
├── assets/
│   └── azcourts.gov/
│       ├── report1.pdf
│       ├── filings.csv
│       └── summary.docx
```

Each JSON file includes fields like:

```json
{
  "url": "https://azcourts.gov/azcjc/Public-Decisions",
  "text": "Extracted clean page text...",
  "linked_assets": [
    {
      "url": "https://azcourts.gov/files/report.pdf",
      "type": "pdf",
      "path": "output/assets/azcourts.gov/report.pdf"
    }
  ]
}
```

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.11+
- Docker (optional but recommended)

### 📦 Install Locally
```bash
pip install -r requirements.txt
python main.py
```

### 🐳 Or Run with Docker
```bash
docker build -t rag-spider-ms .
docker run -it \
  -v $(pwd)/output:/app/output \
  -p 8000:8000 \
  rag-spider-ms
```

---

## 📬 API Usage

### `POST /crawl`
Submit one or more URLs to crawl and extract.

#### Request Body (Single or List)
```json
{
  "urls": [
    { "url": "https://www.azcourts.gov/azcjc/Public-Decisions", "depth": 1 }
  ],
  "extract_text_only": true
}
```

#### Response
```json
{
  "status": "success",
  "data": [
    {
      "url": "...",
      "text": "...",
      "linked_assets": [...]
    }
  ]
}
```

---

## 🧠 RAG Readiness

This microservice prepares clean content and linked documents for RAG pipelines. Next steps:

- Parse PDF/CSV/DOCX content into text
- Chunk + embed with OpenAI / Bedrock
- Store in FAISS / Pinecone / OpenSearch
- Build `/query` endpoint for semantic retrieval

---

## 🗃 File Overview

```
src/
├── core.py           # Orchestrates crawl + extraction + asset download
├── crawler.py        # Asynchronous site-local spider
├── extractor.py      # Extracts clean HTML page content
├── downloader.py     # Downloads linked assets to disk
├── utils.py          # URL normalization + domain filtering
├── logger.py         # Shared logging configuration
```

---

## 🔐 Coming Soon

- `document_parser.py`: PDF/CSV/Word file text extraction
- `s3_helper.py`: S3 storage integration for AWS-native pipelines
- `embedder.py`: Vectorization and retrieval storage
- CI/CD with GitHub Actions + Terraform deployment to AWS

---

## 📜 License
MIT
