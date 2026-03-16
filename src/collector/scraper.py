import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

class BookScraper:
    def __init__(self, url, book_name, base_dir="data/raw_screenshots"):
        self.url = url
        # 1. Sanitize the book name for the file system
        # Removes spaces and ensures only alphanumeric/underscores
        clean_name = "".join(c if c.isalnum() else "_" for c in book_name).lower()
        self.book_name = clean_name
        
        # 2. Setup the specific directory: data/raw_screenshots/bookname
        self.output_dir = Path(base_dir) / self.book_name
        
        # Create the directory (and parents) if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) 
            context = await browser.new_context(device_scale_factor=2)
            page = await context.new_page()
            
            print(f"Navigating to {self.url}...")
            await page.goto(self.url, wait_until="networkidle")

            # Zoom out logic
            await page.click('button[title="Zoom out"]')
            await page.wait_for_timeout(1000)

            page_count = 1
            while True:
                print(f"[{self.book_name}] Capturing Page {page_count}...")

                # Define the capture areas
                area_1 = {'x': 260, 'y': 85, 'width': 384, 'height': 546} 
                area_2 = {'x': 644, 'y': 85, 'width': 384, 'height': 546}

                # 3. Construct the organized file paths
                left_file = self.output_dir / f"{self.book_name}_page_{page_count}_left.png"
                right_file = self.output_dir / f"{self.book_name}_page_{page_count}_right.png"

                await page.screenshot(path=str(left_file), clip=area_1)
                await page.screenshot(path=str(right_file), clip=area_2)

                # Slider check for 100%
                handle = page.locator('a.ui-slider-handle')
                style_attr = await handle.get_attribute("style")
                
                if "left: 100%;" in style_attr:
                    print(f"Reached 100% for {self.book_name}. Finishing...")
                    break

                # Flip Right and wait for animation
                await page.click('button[title="Flip right"]')
                await page.wait_for_timeout(1500) 
                
                page_count += 1

            await browser.close()

if __name__ == "__main__":
    # You can now easily queue up multiple books
    async def main():
        # Scrape Book 1
        scraper1 = BookScraper(
            url="https://digitalna.gbsk.mk/viewer/show/425#page/n0/mode/2up", 
            book_name="Nerezi"
        )
        scraper2 = BookScraper(
            url="https://digitalna.gbsk.mk/viewer/show/419#page/n0/mode/2up",
            book_name="Vardar"
        )
        await scraper1.run()
        await scraper2.run()
        

    asyncio.run(main())
