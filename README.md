# Xcite Product Scraper

A Python script that searches [xcite.com.sa](https://www.xcite.com.sa) for a product and saves the results to a JSON file.

## What it collects

For each product in the search results:
- Brand
- Name
- Price (or discount price + original price when on sale)
- Product link

## Requirements

```bash
pip install playwright playwright-stealth beautifulsoup4
playwright install chromium
```

## Usage

```bash
python xcite-scrape.py
```

Enter a search term when prompted (e.g. `iphone`). The script clicks "Show more" until all results are loaded, then writes them to `products.json`.

## Output example

```json
[
    {
        "Product Number:": 1,
        "Product Brand": "Apple",
        "Product Name": "iPhone 15 Pro 256GB",
        "Price": "4,999 SAR",
        "Link": "/apple-iphone-15-pro/p"
    }
]
```


