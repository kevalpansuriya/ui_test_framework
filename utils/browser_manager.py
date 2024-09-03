from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self, browser_type='chromium'):
        self.browser_type = browser_type

    def launch_browser(self, headless=True):
        with sync_playwright() as p:
            browser = getattr(p, self.browser_type).launch(headless=headless)
            context = browser.new_context()
            return context.new_page()
