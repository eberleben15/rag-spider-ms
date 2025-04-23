# src/extractor.py

from bs4 import BeautifulSoup
from trafilatura import extract as trafilatura_extract
from src.logger import get_logger

logger = get_logger(__name__)

def extract_with_trafilatura(html: str) -> str:
    try:
        return trafilatura_extract(html) or ""
    except Exception as e:
        logger.warning(f"Trafilatura extraction failed: {e}")
        return ""

def extract_with_bs4(html: str) -> dict:
    try:
        soup = BeautifulSoup(html, "html.parser")
        title = (soup.title.string or "").strip() if soup.title else ""
        body = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
        headers = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
        return {
            "title": title,
            "headers": headers,
            "body": body
        }
    except Exception as e:
        logger.warning(f"BeautifulSoup fallback extraction failed: {e}")
        return {"title": "", "headers": [], "body": ""}

def extract_content(entry: dict, extract_text_only: bool = True) -> dict:
    html = entry.get("html", "")
    if not html:
        return {"url": entry.get("url"), "title": "", "text": ""}

    if extract_text_only:
        text = extract_with_trafilatura(html)
        if not text:
            logger.info(f"Falling back to BeautifulSoup for {entry['url']}")
            parsed = extract_with_bs4(html)
            text = parsed.get("body", "")
        return {
            "url": entry["url"],
            "text": text.strip()
        }
    else:
        parsed = extract_with_bs4(html)
        return {
            "url": entry["url"],
            "title": parsed["title"],
            "headers": parsed["headers"],
            "text": parsed["body"]
        }