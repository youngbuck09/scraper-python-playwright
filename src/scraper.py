import asyncio
import json
import csv
import time

from playwright.async_api import async_playwright

from amazon_scraper import scrape_amazon
from walmart_scraper import scrape_walmart
from utils import log_error, retry

# limit number of concurrent pages
CONCURRENCY_LIMIT = 3
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


async def process_sku(context, item, index, total):

    async with semaphore:

        sku = item["SKU"]
        source = item["Type"]

        page = await context.new_page()

        try:

            print(f"[{index}/{total}] Scraping {source} {sku}")

            if source == "Amazon":
                result = await retry(lambda: scrape_amazon(page, sku))

            elif source == "Walmart":
                result = await retry(lambda: scrape_walmart(page, sku))

            await page.close()

            return [
                sku,
                source,
                result["title"],
                result["description"],
                result["price"],
                result["reviews"]
            ]

        except Exception as e:

            log_error(f"{sku} failed: {str(e)}")

            await page.close()

            return [
                sku,
                source,
                "Unavailable",
                "Unavailable",
                "Unavailable",
                "Unavailable"
            ]


async def run():

    start_time = time.time()

    # load SKUs
    with open("../skus.json") as f:
        data = json.load(f)

    skus = data["skus"]
    total = len(skus)

    async with async_playwright() as p:

        context = await p.chromium.launch_persistent_context(
            user_data_dir="../browser_profile",
            headless=False,
            slow_mo=200,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
        )

        tasks = []

        for i, item in enumerate(skus, start=1):
            tasks.append(process_sku(context, item, i, total))

        results = await asyncio.gather(*tasks)

        await context.close()

    # write CSV
    with open("../product_data.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "SKU",
            "Source",
            "Title",
            "Description",
            "Price",
            "Number of Reviews"
        ])

        for row in results:
            if row:
                writer.writerow(row)

    end_time = time.time()

    print(f"\nScraping completed in {round(end_time - start_time, 2)} seconds")


asyncio.run(run())