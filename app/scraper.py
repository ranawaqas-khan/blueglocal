import asyncio, random, os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from app.utils import parse_results

load_dotenv()

PROXY_USER = os.getenv("WEBSHARE_USER")
PROXY_PASS = os.getenv("WEBSHARE_PASS")

def load_proxies(file_path="proxies.txt"):
    """Load proxies from text file (ip:port:user:pass format)"""
    proxies = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    parts = proxy.split(":")
                    if len(parts) == 4:
                        ip, port, user, pwd = parts
                        proxies.append(f"http://{user}:{pwd}@{ip}:{port}")
                    else:
                        print(f"[⚠️] Skipping invalid proxy: {proxy}")
    else:
        print("[❌] proxies.txt not found.")
    print(f"[🔁] Loaded {len(proxies)} proxies.")
    return proxies

PROXIES = load_proxies()

async def scrape_single(playwright, url: str, proxy_url: str):
    """Scrape a single Google Maps URL with a given proxy"""
    print(f"[🌐] Using proxy: {proxy_url}")
    browser = await playwright.chromium.launch(
        headless=True,
        proxy={"server": proxy_url}
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
    """Run multiple scraping tasks concurrently"""
    async with async_playwright() as p:
        tasks = []
        for url in urls:
            proxy_url = random.choice(PROXIES)
            tasks.append(scrape_single(p, url, proxy_url))
        await asyncio.gather(*tasks)
