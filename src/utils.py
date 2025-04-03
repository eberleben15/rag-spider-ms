# src/utils.py

from urllib.parse import urlparse, urljoin
import tldextract


def normalize_url(url: str) -> str:
    """Ensure URLs are consistent for deduplication."""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc
    path = parsed.path.rstrip("/") or "/"
    return f"{scheme}://{netloc}{path}"


def is_same_domain(base_url: str, target_url: str) -> bool:
    """Check if target URL is within the same registered domain as base."""
    base_domain = tldextract.extract(base_url).registered_domain
    target_domain = tldextract.extract(target_url).registered_domain
    return base_domain == target_domain


def resolve_relative_url(base_url: str, link: str) -> str:
    """Join relative link with base URL."""
    return urljoin(base_url, link)


def clean_links(base_url: str, raw_links: list[str]) -> list[str]:
    """Normalize and filter links to same-domain only."""
    seen = set()
    filtered = []
    for link in raw_links:
        absolute = normalize_url(resolve_relative_url(base_url, link))
        if is_same_domain(base_url, absolute) and absolute not in seen:
            seen.add(absolute)
            filtered.append(absolute)
    return filtered