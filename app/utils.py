from bs4 import BeautifulSoup

def parse_results(html: str, source_url: str):
    """Basic parser – replace later with Playwright element extraction"""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    cards = soup.find_all("div", class_="Nv2PK")  # typical Maps card class
    for card in cards:
        name = card.get_text(" ", strip=True)
        results.append({
            "name": name[:100],
            "source": source_url
        })
    return results
