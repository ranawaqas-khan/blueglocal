from fastapi import FastAPI
from pydantic import BaseModel
from app.scraper import scrape_single
import asyncio

app = FastAPI(title="Local Business Finder API (Instant Mode)")

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"status": "running", "message": "Local Business Finder API (Instant Mode)"}

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    """Scrape single URL and return results instantly."""
    result = await scrape_single(request.url)
    return result
