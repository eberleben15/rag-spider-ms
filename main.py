# main.py

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from src.core import crawl_and_extract
from src.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="RAG-Ready Web Spider", version="1.0")

class URLInput(BaseModel):
    url: str
    depth: int = 1

class CrawlRequest(BaseModel):
    urls: Union[URLInput, List[URLInput]]
    extract_text_only: bool = True

@app.post("/crawl")
async def crawl_webpages(request: CrawlRequest):
    try:
        url_list = request.urls if isinstance(request.urls, list) else [request.urls]
        logger.info(f"Received crawl request with {len(url_list)} URL(s).")
        results = await crawl_and_extract(url_list, request.extract_text_only)
        return {"status": "success", "data": results}
    except Exception as e:
        logger.exception("Error during crawl.")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)