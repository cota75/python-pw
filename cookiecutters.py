import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
import time

@pytest.fixture(scope="function")
def setup_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Start tracing
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        
        yield page

        # Stop tracing and save it to a file
        context.tracing.stop(path="trace.zip")
        
    
        context.close()
        browser.close()

def test_cookie_clicker(setup_browser):
    page = setup_browser
    page.goto("https://orteil.dashnet.org/cookieclicker/")

    # Choose English language
    page.get_by_text("English").click()

    product_price = page.locator("#productPrice0").text_content()
    num_cookies = page.locator('#cookies').text_content().split(" ")[0]

    # Click the big cookie multiple times
    #for i in range(16):
    while num_cookies != product_price:
        page.locator("#bigCookie").click()
        num_cookies = page.locator('#cookies').text_content().split(" ")[0]
        if int(num_cookies) > 20:
            break

    # Check if the first product becomes unlocked
    product = page.locator("#product0")
    assert product.is_enabled(), "Product 0 should be enabled after clicking the big cookie"

    # Try to buy the first product
    product.click()

    time.sleep(10)
    # Verify that the product was purchased (this depends on the game's logic, adjust as needed)
    assert product.get_attribute("class").find("enabled") == -1, "Product 0 should be disabled after purchase"

