import asyncio, random, os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from app.utils import parse_results

load_dotenv()

PROXY_USER = os.getenv("WEBSHARE_USER")
PROXY_PASS = os.getenv("WEBSHARE_PASS")

# Add more proxies later when you share your list
PROXIES = []

async def scrape_single(playwright, url: str, proxy: str):
    browser = await playwright.chromium.launch(
        headless=True,
        proxy={"server": proxy, "username": PROXY_USER, "password": PROXY_PASS}
    )
    page = await browser.new_page()
    try:
        await page.goto(url, timeout=60000)
        await asyncio.sleep(2)
        for _ in range(10):
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(random.uniform(1, 2))
        html = await page.content()
        data = parse_results(html, url)
        print(f"[✅] Scraped {url} -> {len(data)} results")
    except Exception as e:
        print(f"[❌] Error on {url}: {e}")
    finally:
        await browser.close()

async def scrape_multiple(urls: list[str]):
    async with async_playwright() as p:
        tasks = []
        for url in urls:
            proxy = random.choice(PROXIES) if PROXIES else None
            tasks.append(scrape_single(p, url, proxy))
        await asyncio.gather(*tasks)
