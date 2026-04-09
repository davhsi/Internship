import sqlite3
import random
import logging
import asyncio
from bs4 import BeautifulSoup as bs
from playwright.async_api import async_playwright
from config import SEARCH_KEYWORD, DB_PATH, MAX_PAGES, LOG_FILE
from report import generate_report

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Rotate useragents so Amazon doesn't flag as a bot
user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

sem = asyncio.Semaphore(5)  # max 5 workers

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS products(
    asin TEXT,
    product_name TEXT,
    price REAL,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
)

seen_asins = set()


async def scrape_page(browser, page_num, seen_asins):
    async with sem:
        url = f"https://www.amazon.in/s?k={SEARCH_KEYWORD.replace(' ', '+')}&page={page_num}"
        page = await browser.new_page()

        retries = 0
        success = False
        while retries < 3:
            try:
                await page.set_extra_http_headers(
                    {"User-Agent": random.choice(user_agents)}
                )
                await page.goto(url)
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_selector(
                    "div[data-component-type='s-search-result']"
                )
                success = True
                logger.info(f"[OK] Page {page_num} fetched successfully")
                break
            except Exception as e:
                retries += 1
                logger.warning(
                    f"Page {page_num} attempt {retries} failed. Retries left: {3 - retries}"
                )
                await asyncio.sleep(random.uniform(2, 5))

        if not success:
            logger.error(f"[FAILED] Page {page_num} failed after 3 retries, skipping")
            await page.close()
            return []

        soup = bs(await page.content(), "lxml")
        await page.close()

        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        page_asins = {p.get("data-asin") for p in products if p.get("data-asin")}

        if page_asins.issubset(seen_asins):
            logger.info(f"Page {page_num} — all ASINs repeated, stopping")
            return None

        results = []
        for product in products:
            asin = product.get("data-asin")
            if not asin:
                continue

            title_tag = product.select_one("h2 span")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            whole_span = product.find("span", class_="a-price-whole")
            fraction_span = product.find("span", class_="a-price-fraction")
            if whole_span:
                whole = whole_span.text.strip().replace(",", "")
                fraction = fraction_span.text.strip() if fraction_span else "0"
                price = float(whole) + float(fraction) / 100
            else:
                price = None

            results.append((asin, title, price))

        logger.info(f"Page {page_num} — {len(results)} products found")
        return results


async def main():
    logger.info(
        f"Scraper started — target: amazon.in/s?k={SEARCH_KEYWORD.replace(' ', '+')}"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [scrape_page(browser, n, seen_asins) for n in range(1, MAX_PAGES)]
        results = await asyncio.gather(*tasks)

        await browser.close()

    for page_results in results:
        if page_results is None or page_results == []:
            continue
        for asin, title, price in page_results:
            seen_asins.add(asin)

            cursor.execute(
                """
                INSERT INTO products (asin, product_name, price)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM products
                    WHERE asin = ?
                    AND DATE(scraped_at) = DATE('now')
                )
            """,
                (asin, title, price, asin),
            )

    conn.commit()
    conn.close()

    logger.info(
        f"Scraper finished - {len(seen_asins)} total unique products saved to DB"
    )

    generate_report()


if __name__ == "__main__":
    asyncio.run(main())
