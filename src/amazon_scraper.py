from playwright.async_api import Page


async def scrape_amazon(page: Page, sku: str):

    url = f"https://www.amazon.com/dp/{sku}"

    await page.goto(url, timeout=60000)

    await page.wait_for_load_state("networkidle")

    title_locator = page.locator("span#productTitle")

    if await title_locator.count() == 0:
        raise Exception("Amazon product page not loaded")

    title = await title_locator.first.inner_text()

    price_locator = page.locator(".a-price .a-offscreen")

    price = "Not available"
    if await price_locator.count() > 0:
        price = await price_locator.first.inner_text()
        price = price.replace("\u00A0", " ").strip()

    description_locator = page.locator("#feature-bullets")

    description = "No description"
    if await description_locator.count() > 0:
        description = await description_locator.inner_text()

    review_locator = page.locator("#acrCustomerReviewText")

    reviews = "No reviews"
    if await review_locator.count() > 0:
        reviews = await review_locator.first.inner_text()

    return {
        "title": title.strip(),
        "price": price,
        "description": description.strip(),
        "reviews": reviews
    }