"""Google search flow: find a query and open the first LinkedIn profile."""

from playwright.sync_api import Page

from pages.google_search_page import GoogleCaptchaError, GoogleSearchPage
from utils.config_loader import ConfigLoader
from utils.logger import get_logger


class WebSearch:
    """Search on Google with Chrome and open the first LinkedIn profile in the results."""

    def __init__(self, page: Page, config: ConfigLoader | None = None) -> None:
        self.page = page
        self.config = config or ConfigLoader()
        self.logger = get_logger(self.__class__.__name__, self.config.get_log_path())

    def search_and_open_first_linkedin_profile(self, query: str) -> Page:
        """Search Google for `query` and return the Playwright page on LinkedIn."""
        google = GoogleSearchPage(self.page, self.config)
        google.enable_stealth_mode()
        google.open_homepage()
        google.search(query)

        if google.has_captcha():
            raise GoogleCaptchaError(
                "Google showed a CAPTCHA. Run locally with Chrome installed: pytest --headed"
            )

        linkedin_page = google.open_first_linkedin_result()
        google.assert_linkedin_profile_open(linkedin_page)
        self.logger.info("Opened LinkedIn profile: %s", linkedin_page.url)
        return linkedin_page
