from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def get_barcode_title(barcode: str, headless: bool = False) -> str:
    url = f"https://www.barcodelookup.com/{barcode}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            java_script_enabled=True,
        )

        # Bypass navigator.webdriver detection
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle")
            # Simulate user interaction
            page.mouse.move(200, 300)
            page.wait_for_timeout(1500)
            html = page.content()

            soup = BeautifulSoup(html, "html.parser")
            title_tag = soup.find("h4")

            if title_tag:
                return title_tag.get_text(strip=True)
            else:
                return "Product title not found"
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            browser.close()


# Example usage
if __name__ == "__main__":
    barcode = input("Enter barcode: ")
    title = get_barcode_title(barcode, headless=False)  # Set to True to run in headless mode
    print(title)
