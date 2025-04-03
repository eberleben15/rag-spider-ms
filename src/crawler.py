import httpx
import asyncio
from bs4 import BeautifulSoup
from src.utils import normalize_url, clean_links
from src.logger import get_logger

logger = get_logger(__name__)

HEADERS = {
    "User-Agent": "rag-spider-ms/1.0 (+https://github.com/your-repo)"
}

async def fetch(session: httpx.AsyncClient, url: str) -> str:
    try:
        response = await session.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error {e.response.status_code} on {url}")
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
    return ""

async def crawl_url(session: httpx.AsyncClient, url: str, depth: int, visited: set) -> list[dict]:
    if url in visited or depth < 0:
        return []

    logger.info(f"Crawling: {url} (depth={depth})")
    visited.add(url)
    html = await fetch(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    child_links = clean_links(url, links)

    result = [{
        "url": url,
        "html": html,
        "depth": depth
    }]

    tasks = [crawl_url(session, link, depth - 1, visited) for link in child_links]
    children = await asyncio.gather(*tasks)
    for sublist in children:
        result.extend(sublist)

    return result

async def crawl_all(urls: list[dict], extract_text_only: bool) -> list[dict]:
    async with httpx.AsyncClient(headers=HEADERS) as session:
        visited = set()
        all_results = []
        for item in urls:
            norm_url = normalize_url(item["url"])
            depth = item.get("depth", 1)
            crawled = await crawl_url(session, norm_url, depth, visited)
            all_results.extend(crawled)
        return all_results