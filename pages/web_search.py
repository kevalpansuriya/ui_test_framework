"""Runs a web search and opens the first LinkedIn profile from the results."""

from playwright.sync_api import Page

from pages.duckduckgo_search_page import DuckDuckGoSearchPage
from pages.google_search_page import GoogleCaptchaError, GoogleSearchPage
from utils.config_loader import ConfigLoader
from utils.logger import get_logger


class WebSearch:
    """
    High-level flow: search on Google (or another engine) and open the first
    LinkedIn profile. Falls back to DuckDuckGo when Google shows a CAPTCHA.
    """

    def __init__(self, page: Page, config: ConfigLoader | None = None) -> None:
        self.page = page
        self.config = config or ConfigLoader()
        self.logger = get_logger(self.__class__.__name__, self.config.get_log_path())

    def search_and_open_first_linkedin_profile(self, query: str) -> Page:
        """Search for `query` and return the Playwright page on LinkedIn."""
        engine = self.config.get_search_engine().lower()
        fallback = self.config.get_search_engine_fallback().lower()

        if engine == "google":
            try:
                return self._search_with_google(query)
            except GoogleCaptchaError as error:
                self.logger.warning(str(error))
                if not fallback or fallback == "google":
                    raise
                self.logger.info("Retrying with fallback engine: %s", fallback)
                return self._search_with_engine(fallback, query)

        return self._search_with_engine(engine, query)

    def _search_with_google(self, query: str) -> Page:
        google = GoogleSearchPage(self.page, self.config)
        google.enable_stealth_mode()
        google.open_homepage()
        google.search(query)

        if google.has_captcha():
            raise GoogleCaptchaError(
                "Google showed a CAPTCHA. Use installed Chrome (headed), or set "
                "search_engine_fallback to duckduckgo in config/config.json."
            )

        linkedin_page = google.open_first_linkedin_result()
        google.assert_linkedin_profile_open(linkedin_page)
        return linkedin_page

    def _search_with_engine(self, engine: str, query: str) -> Page:
        if engine == "duckduckgo":
            duck = DuckDuckGoSearchPage(self.page, self.config)
            duck.search(query)
            linkedin_page = duck.open_first_linkedin_result()
            duck.assert_linkedin_profile_open(linkedin_page)
            return linkedin_page

        if engine == "google":
            return self._search_with_google(query)

        raise ValueError(f"Unknown search engine: {engine}")
