"""UI test: Google search for a person and open the first LinkedIn profile."""

import pytest

from pages.web_search import WebSearch
from utils.config_loader import ConfigLoader
from utils.logger import get_logger


@pytest.mark.ui
@pytest.mark.smoke
class TestGoogleLinkedInSearch:
    """Search on Google and land on the first LinkedIn profile in the results."""

    @pytest.fixture(autouse=True)
    def setup(self, page, test_config: ConfigLoader):
        self.page = page
        self.config = test_config
        self.web_search = WebSearch(page, test_config)
        self.query = test_config.get_search_query()
        self.logger = get_logger(self.__class__.__name__, test_config.get_log_path())

    def test_search_and_open_first_linkedin_profile(self):
        """
        Steps:
        1. Open Google in Chrome.
        2. Search for the configured query (default: keval pansuriya encora).
        3. Click the first LinkedIn profile link.
        4. Assert the URL is a LinkedIn profile (/in/ or /pub/).
        """
        linkedin_page = self.web_search.search_and_open_first_linkedin_profile(self.query)

        url = linkedin_page.url.lower()
        assert "linkedin.com" in url
        assert "/in/" in url or "/pub/" in url

        self.logger.info("Opened LinkedIn profile: %s", linkedin_page.url)
