"""DuckDuckGo search page — fallback when Google shows a CAPTCHA."""

import re
from urllib.parse import quote_plus

from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from utils.config_loader import ConfigLoader


class DuckDuckGoSearchPage(BasePage):
    """Actions for searching on DuckDuckGo."""

    LINKEDIN_LINK = 'a[href*="linkedin.com/in/"], a[href*="linkedin.com/pub/"]'

    def __init__(self, page: Page, config: ConfigLoader | None = None) -> None:
        self.config = config or ConfigLoader()
        settings = self.config.get_playwright_settings()
        super().__init__(page, timeout_ms=settings.get("timeout_ms", 30_000))
        self.base_url = self.config.get_duckduckgo_url()

    def search(self, query: str) -> None:
        """Open DuckDuckGo with the query in the URL."""
        url = f"{self.base_url}/?q={quote_plus(query)}"
        self.go_to(url)
        self.page.wait_for_load_state("domcontentloaded")
        self.logger.info("Submitted search: %s", query)

    def first_linkedin_result(self) -> Locator:
        links = self.page.locator(self.LINKEDIN_LINK)
        expect(links.first).to_be_visible(timeout=self.timeout_ms)
        return links.first

    def open_first_linkedin_result(self) -> Page:
        link = self.first_linkedin_result()
        href = link.get_attribute("href") or ""
        self.logger.info("Opening LinkedIn profile: %s", href)

        if link.get_attribute("target") == "_blank":
            with self.page.context.expect_page(timeout=self.timeout_ms) as popup:
                link.click()
            new_page = popup.value
            new_page.wait_for_load_state("domcontentloaded")
            return new_page

        link.click()
        self.page.wait_for_url(re.compile(r"linkedin\.com/(in|pub)/"), timeout=self.timeout_ms)
        self.page.wait_for_load_state("domcontentloaded")
        return self.page

    def assert_linkedin_profile_open(self, active_page: Page | None = None) -> None:
        target = active_page or self.page
        expect(target).to_have_url(
            re.compile(r"linkedin\.com/(in|pub)/"),
            timeout=self.timeout_ms,
        )
