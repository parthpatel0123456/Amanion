from playwright.sync_api import sync_playwright

def scrape_macs_newegg(limit=5):
    url = "https://www.newegg.com/p/pl?d=macbook"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to the URL and wait until network is idle
        page.goto(url, wait_until="networkidle")

        # Close any popups if present
        try:
            page.click("button[class*='close']")  # adjust if selector changes
        except:
            pass

        # Wait for product containers to appear
        page.wait_for_selector(".item-cell", timeout=60000)
        items = page.query_selector_all(".item-cell")

        for item in items[:limit]:
            product = {}

            # Basic info
            try:
                product['title'] = item.query_selector(".item-title").inner_text().strip()
            except:
                product['title'] = None
            try:
                product['price'] = item.query_selector(".price-current").inner_text().strip()
            except:
                product['price'] = None
            try:
                product['link'] = item.query_selector(".item-title").get_attribute("href")
            except:
                product['link'] = None

            # Open product page for specs
            if product['link']:
                page.goto(product['link'], wait_until="networkidle")
                specs = {}

                # Handle popup on product page
                try:
                    page.click("button[class*='close']")
                except:
                    pass

                # Iterate over tables
                tables = page.query_selector_all("table.table-horizontal")
                for table in tables:
                    rows = table.query_selector_all("tr")
                    for row in rows:
                        try:
                            key = row.query_selector("th").inner_text().strip()
                            value = row.query_selector("td").inner_text().strip()
                            specs[key] = value
                        except:
                            continue
                product['specs'] = specs

            results.append(product)

        browser.close()
    return results

# Example usage
if __name__ == "__main__":
    data = scrape_macs_newegg(limit=3)
    for d in data:
        print(d)
