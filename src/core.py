# src/core.py

import os
import json
from urllib.parse import urlparse
from src.crawler import crawl_all
from src.extractor import extract_content
from src.logger import get_logger

logger = get_logger(__name__)
OUTPUT_DIR = "output"

def write_output_to_file(domain: str, data: list[dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{domain}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


from src.crawler import crawl_all
from src.extractor import extract_content
from src.logger import get_logger
from urllib.parse import urlparse
import os
import json

logger = get_logger(__name__)
OUTPUT_DIR = "output"

def write_output_to_file(domain: str, data: list[dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{domain}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def crawl_and_extract(url_inputs: list, extract_text_only: bool = True) -> list[dict]:
    logger.info("Starting crawl and extract workflow...")

    # ✅ Fix: pass raw values (not dict-style access)
    url_list = [{"url": item.url, "depth": item.depth} for item in url_inputs]

    crawled_pages = await crawl_all(url_list, extract_text_only)
    logger.info(f"Crawled {len(crawled_pages)} total pages.")

    results = []
    for entry in crawled_pages:
        try:
            content = extract_content(entry, extract_text_only=extract_text_only)
            results.append(content)
        except Exception as e:
            logger.error(f"Extraction failed for {entry.get('url')}: {e}")

    logger.info(f"Extraction complete. Returning {len(results)} documents.")

    domain_groups = {}
    for doc in results:
        domain = urlparse(doc["url"]).netloc.replace("www.", "")
        domain_groups.setdefault(domain, []).append(doc)

    for domain, group in domain_groups.items():
        try:
            write_output_to_file(domain, group)
            logger.info(f"Saved {len(group)} pages to output/{domain}.json")
        except Exception as e:
            logger.error(f"Failed to write output for {domain}: {e}")

    return results