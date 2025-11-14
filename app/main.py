from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.scraper import scrape_multiple
import asyncio

app = FastAPI(title="Local Business Finder API")

class ScrapeRequest(BaseModel):
    urls: list[str]

@app.get("/")
async def root():
    return {"status": "running", "message": "Local Business Finder API"}

@app.post("/scrape")
async def scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_multiple, request.urls)
    return {"status": "accepted", "urls": len(request.urls)}
