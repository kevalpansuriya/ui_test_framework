"""Google search page — open Google, search, and pick LinkedIn results."""

import re
from urllib.parse import quote_plus

from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from utils.config_loader import ConfigLoader


class GoogleCaptchaError(Exception):
    """Raised when Google shows a bot-detection page instead of search results."""


class GoogleSearchPage(BasePage):
    """Actions for searching on Google."""

    SEARCH_BOX = 'textarea[name="q"], input[name="q"]'
    LINKEDIN_LINK = 'a[href*="linkedin.com/in/"], a[href*="linkedin.com/pub/"]'
    CAPTCHA_TEXT = re.compile(r"unusual traffic|not a robot", re.IGNORECASE)

    STEALTH_SCRIPT = """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
    """

    def __init__(self, page: Page, config: ConfigLoader | None = None) -> None:
        self.config = config or ConfigLoader()
        settings = self.config.get_playwright_settings()
        super().__init__(page, timeout_ms=settings.get("timeout_ms", 30_000))
        self.google_url = self.config.get_google_url()

    def enable_stealth_mode(self) -> None:
        """Hide common automation signals before the first navigation."""
        self.page.add_init_script(self.STEALTH_SCRIPT)

    @property
    def search_box(self) -> Locator:
        return self.page.locator(self.SEARCH_BOX).first

    def open_homepage(self) -> None:
        """Go to Google and dismiss cookie banners when shown."""
        self.go_to(self.google_url)
        self._accept_cookies_if_needed()

    def _accept_cookies_if_needed(self) -> None:
        # Short timeout: most runs have no banner; avoids ~8s of idle waiting
        for label in ("Accept all", "I agree"):
            self.click_if_visible(label, wait_ms=800)

    def search(self, query: str) -> None:
        """Open Google search results for the query (single page load)."""
        search_url = f"{self.google_url}/search?q={quote_plus(query)}&hl=en&gl=us"
        self.go_to(search_url)
        self._accept_cookies_if_needed()

        if self.has_captcha():
            return

        self.logger.info("Search results loaded for: %s", query)

    def has_captcha(self) -> bool:
        """True when Google blocks automation with a CAPTCHA page."""
        body_text = self.page.locator("body").inner_text(timeout=5_000)
        return bool(self.CAPTCHA_TEXT.search(body_text))

    def first_linkedin_result(self) -> Locator:
        """Wait for and return the first LinkedIn profile link in results."""
        links = self.page.locator(self.LINKEDIN_LINK)
        expect(links.first).to_be_visible(timeout=self.timeout_ms)
        return links.first

    def open_first_linkedin_result(self) -> Page:
        """Click the first LinkedIn profile link and return the active tab."""
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
        """Verify the browser is on a LinkedIn profile URL."""
        target = active_page or self.page
        expect(target).to_have_url(
            re.compile(r"linkedin\.com/(in|pub)/"),
            timeout=self.timeout_ms,
        )
