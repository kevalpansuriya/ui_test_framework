from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.UI.base_page import BasePage


class HomePage(BasePage):
    """
    Home Page Object Model following SRP - handles only home page functionality
    """

    # Locators using camelCase naming
    pageTitleLocator: Tuple[By, str] = (By.TAG_NAME, "h1")
    pageHeadingLocator: Tuple[By, str] = (By.TAG_NAME, "h2")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.logger.info("HomePage initialized")

    def getPageTitle(self) -> str:
        """Get page title"""
        return self.getText(self.pageTitleLocator)

    def getPageHeading(self) -> str:
        """Get page heading"""
        return self.getText(self.pageHeadingLocator)

    def isPageLoaded(self) -> bool:
        """Check if page is loaded"""
        return self.isElementVisible(self.pageTitleLocator)

