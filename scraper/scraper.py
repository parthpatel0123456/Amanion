import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import CrawlerRunConfig
import json

async def main():
    schema = {
        "name": "AmazonProduct",
        "baseSelector": "body",
        "fields": [
            {"name": "title", "selector": "#productTitle", "type": "text"},
            {"name": "reviews", "selector": "#acrPopover .a-icon-alt", "type": "text"},
            {"name": "price", "selector": ".aok-offscreen", "type": "text"},
            {"name": "brand", "selector": "tr.po-brand .po-break-word", "type": "text"},
            {"name": "model_name", "selector": "tr.po-model_name .po-break-word", "type": "text"},
            {"name": "screen_size", "selector": "tr.po-display\\.size .po-break-word", "type": "text"},
            {"name": "color", "selector": "tr.po-color .po-break-word", "type": "text"},
            {"name": "hard_disk_size", "selector": "tr.po-hard_disk\\.size .po-break-word", "type": "text"},
            {"name": "cpu_model", "selector": "tr.po-cpu_model\\.family .po-break-word", "type": "text"},
            {"name": "ram_memory_installed_size", "selector": "tr.po-ram_memory\\.installed_size .po-break-word", "type": "text"},
            {"name": "operating_system", "selector": "tr.po-operating_system .po-break-word", "type": "text"},
            {"name": "special_feature", "selector": "tr.po-special_feature .po-break-word", "type": "text"},
            {"name": "graphics_card_description", "selector": "tr.po-graphics_description .po-break-word", "type": "text"},
        ],
    }

    extraction = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(extraction_strategy=extraction)

    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://www.amazon.com/Apple-2024-MacBook-Laptop-10%E2%80%91core/dp/B0DLHBYRPS", config=config)

        data = json.loads(result.extracted_content)

        # Print the extracted content
        with open("product_data.json", "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# Run the async main function
asyncio.run(main())
