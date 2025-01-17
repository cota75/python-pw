import re
from playwright.sync_api import Playwright, sync_playwright, expect


#productPrice0 = "15"

#cookies - <div id="cookies" class="title">15 cookies<div id="cookiesPerSecond">per second: 0</div></div>

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://orteil.dashnet.org/cookieclicker/")
    page.get_by_text("English").click()

    price_prize0 = page.locator("#productPrice0").text_content()

    cookies_count = page.locator("#cookies").text_content().split(" ")[0]
    while cookies_count != price_prize0:
        page.locator("#bigCookie").click()
        cookies_count = page.locator("#cookies").text_content().split(" ")[0]
        print(cookies_count)
        if int(cookies_count) > 20:
            break



    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
