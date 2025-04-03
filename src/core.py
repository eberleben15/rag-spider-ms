# src/core.py

import os
import json
from urllib.parse import urlparse
from src.crawler import crawl_all
from src.extractor import extract_content
from src.downloader import download_file
from src.logger import get_logger

logger = get_logger(__name__)
OUTPUT_DIR = "output"


def write_output_to_file(domain: str, data: list[dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{domain}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


async def crawl_and_extract(url_inputs: list, extract_text_only: bool = True) -> list[dict]:
    """
    Accepts a list of {url, depth} inputs, crawls each domain, and extracts clean content.
    Returns a structured list of extracted documents for RAG or further processing.
    Also writes grouped domain-based outputs to ./output
    """
    logger.info("Starting crawl and extract workflow...")

    # Normalize to plain dicts if needed
    url_inputs = [{"url": item.url, "depth": item.depth} for item in url_inputs]

    # Step 1: Crawl all pages
    crawled_pages = await crawl_all(url_inputs, extract_text_only)
    logger.info(f"Crawled {len(crawled_pages)} total pages.")

    # Step 2: Extract structured content from each HTML page
    results = []
    for entry in crawled_pages:
        try:
            content = extract_content(entry, extract_text_only=extract_text_only)
            domain = urlparse(entry["url"]).netloc.replace("www.", "")
            assets = entry.get("assets", [])
            linked_assets = []

            for asset_url in assets:
                file_path = await download_file(asset_url, domain)
                if file_path:
                    linked_assets.append({
                        "url": asset_url,
                        "type": asset_url.split(".")[-1].lower(),
                        "path": file_path
                    })

            content["linked_assets"] = linked_assets
            results.append(content)

        except Exception as e:
            logger.error(f"Extraction failed for {entry.get('url')}: {e}")

    logger.info(f"Extraction complete. Returning {len(results)} documents.")

    # Step 3: Group and write to output/{domain}.json
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