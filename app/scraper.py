import asyncio, random, os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from app.utils import parse_results

load_dotenv()

def load_proxies(file_path="proxies.txt"):
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
    print(f"[🔁] Loaded {len(proxies)} proxies.")
    return proxies

PROXIES = load_proxies()

async def scrape_single(url: str):
    """Scrape one URL and return data instantly."""
    proxy_url = random.choice(PROXIES)
    print(f"[🌐] Using proxy: {proxy_url}")

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"],
                proxy={"server": proxy_url},
            )
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await asyncio.sleep(2)

            # Simulate scrolling to load more
            for _ in range(5):
                await page.mouse.wheel(0, 3000)
                await asyncio.sleep(random.uniform(1, 1.5))

            html = await page.content()
            data = parse_results(html, url)
            print(f"[✅] Scraped {url} -> {len(data)} results")
            return {"url": url, "count": len(data), "data": data}

        except Exception as e:
            print(f"[❌] Error on {url}: {e}")
            return {"url": url, "error": str(e), "data": []}

        finally:
            if browser:
                await browser.close()
