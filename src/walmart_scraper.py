from playwright.async_api import Page


async def scrape_walmart(page: Page, sku: str):

    url = f"https://www.walmart.com/ip/{sku}"

    await page.goto(url, timeout=60000)

    await page.wait_for_timeout(3000)

    await page.wait_for_load_state("domcontentloaded")

    # detect captcha page by content
    page_text = await page.content()

    if "Press and hold" in page_text or "Verify you are human" in page_text:
        raise Exception("Blocked by Walmart verification")

    await page.wait_for_load_state("networkidle")

    title_locator = page.locator("h1")

    if await title_locator.count() == 0:
        raise Exception("Walmart product page blocked or CAPTCHA")

    title = await title_locator.first.inner_text()

    price_locator = page.locator('[itemprop="price"]')

    price = "Not available"
    if await price_locator.count() > 0:
        price = await price_locator.first.inner_text()

    reviews_locator = page.locator('span:has-text("ratings")')

    reviews = "No reviews"
    if await reviews_locator.count() > 0:
        reviews = await reviews_locator.first.inner_text()

    description = "Not available"

    return {
        "title": title,
        "price": price,
        "description": description,
        "reviews": reviews
    }