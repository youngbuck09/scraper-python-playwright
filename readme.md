# Web Scraper Assessment – Amazon & Walmart

## Overview

This project implements a web scraper using **Python and Playwright** to extract product information from **Amazon and Walmart** using product SKUs.

The scraper reads SKUs from a JSON file, visits the corresponding product pages, extracts relevant product details, and stores the results in a CSV file.

The implementation focuses on **robust automation practices**, including modular design, concurrency control, retry mechanisms, and structured error logging.

---

## Extracted Data

For each product SKU, the scraper collects:

* Product Title
* Product Description
* Product Price
* Number of Reviews / Ratings

The extracted data is written to:

```
product_data.csv
```

---

## Project Structure

```
PlaywrightAssignment
│
├── src
│   ├── scraper.py
│   ├── amazon_scraper.py
│   ├── walmart_scraper.py
│   └── utils.py
│
├── skus.json
├── product_data.csv
├── errors.log
├── requirements.txt
└── README.md
```

### File Descriptions

| File               | Purpose                            |
| ------------------ | ---------------------------------- |
| scraper.py         | Main orchestration logic           |
| amazon_scraper.py  | Amazon scraping implementation     |
| walmart_scraper.py | Walmart scraping implementation    |
| utils.py           | Retry logic and logging utilities  |
| skus.json          | Input file containing product SKUs |

---

## Input Format

The scraper expects a JSON file `skus.json` with the following structure:

```json
{
  "skus": [
    {"Type": "Amazon", "SKU": "B0CT4BB651"},
    {"Type": "Walmart", "SKU": "5326288985"},
    {"Type": "Amazon", "SKU": "B01LR5S6HK"}
  ]
}
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone <repository-url>
cd PlaywrightAssignment
```

### 2. Create a virtual environment

```
python -m venv venv
```

Activate the environment:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

Install Playwright browsers:

```
playwright install
```

---

## Running the Scraper

Run the scraper from the project root directory:

```
python src/scraper.py
```

The script will:

1. Load SKUs from `skus.json`
2. Open product pages using Playwright
3. Extract product data
4. Save results to `product_data.csv`

---

## Concurrency

The scraper uses **asynchronous concurrency with asyncio**.

A semaphore is used to limit the number of simultaneous scraping tasks:

```
CONCURRENCY_LIMIT = 3
```

This improves performance while reducing the risk of triggering website anti-bot protections.

---

## Error Handling

The scraper includes multiple resilience mechanisms:

* Retry logic for temporary failures
* Graceful fallbacks when product data is unavailable
* Structured error logging (`errors.log`)
* CAPTCHA detection for blocked pages

If a product page cannot be scraped, the error is logged and the scraper continues processing remaining SKUs.

---

## Limitations

E-commerce websites employ sophisticated anti-bot protection mechanisms.

In some cases, Walmart may trigger human verification challenges that prevent automated scraping. When this occurs:

* The scraper logs the failure
* The SKU is recorded as unavailable in the output file

This ensures the script continues processing other products without interruption.

---

## Technologies Used

* Python
* Playwright
* Asyncio
* CSV module

---

## Author

Dhanesh Chaudhary
