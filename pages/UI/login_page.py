from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.UI.base_page import BasePage


class LoginPage(BasePage):
    """
    Login Page Object Model following SRP - handles only login page functionality
    """

    # Locators using camelCase naming
    usernameInputLocator: Tuple[By, str] = (By.ID, "username")
    passwordInputLocator: Tuple[By, str] = (By.ID, "password")
    loginButtonLocator: Tuple[By, str] = (By.CSS_SELECTOR, "button[type='submit']")
    successMessageLocator: Tuple[By, str] = (By.CSS_SELECTOR, ".flash.success")
    errorMessageLocator: Tuple[By, str] = (By.CSS_SELECTOR, ".flash.error")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.logger.info("LoginPage initialized")

    def enterUsername(self, username: str) -> None:
        """Enter username"""
        self.enterText(self.usernameInputLocator, username)

    def enterPassword(self, password: str) -> None:
        """Enter password"""
        self.enterText(self.passwordInputLocator, password)

    def clickLoginButton(self) -> None:
        """Click login button"""
        self.clickElement(self.loginButtonLocator)

    def login(self, username: str, password: str) -> None:
        """Perform login action"""
        self.enterUsername(username)
        self.enterPassword(password)
        self.clickLoginButton()
        self.logger.info(f"Login attempted with username: {username}")

    def getSuccessMessage(self) -> str:
        """Get success message text"""
        return self.getText(self.successMessageLocator)

    def getErrorMessage(self) -> str:
        """Get error message text"""
        return self.getText(self.errorMessageLocator)

    def isSuccessMessageVisible(self) -> bool:
        """Check if success message is visible"""
        return self.isElementVisible(self.successMessageLocator)

    def isErrorMessageVisible(self) -> bool:
        """Check if error message is visible"""
        return self.isElementVisible(self.errorMessageLocator)

