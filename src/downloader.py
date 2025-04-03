# src/downloader.py

import os
import httpx
from urllib.parse import urlparse
from src.logger import get_logger

logger = get_logger(__name__)

ASSET_DIR = "output/assets"

async def download_file(url: str, domain: str) -> str:
    """
    Downloads a file and saves it under output/assets/{domain}/
    Returns the local file path or empty string on failure.
    """
    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path.split("?")[0])
        if not filename:
            logger.warning(f"No valid filename in URL: {url}")
            return ""

        save_dir = os.path.join(ASSET_DIR, domain)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)

        logger.info(f"Downloaded: {url} → {save_path}")
        return save_path

    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return ""