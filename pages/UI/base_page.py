from typing import List, Tuple
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger


class BasePage:
    """
    Base Page Object Model class following SRP - handles only page base functionality
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.logger: logging.Logger = Logger().getLogger(self.__class__.__name__)
        self.wait: WebDriverWait = WebDriverWait(driver, 20)

    def findElement(self, locator: Tuple[By, str]) -> WebElement:
        """
        Find element with wait

        Args:
            locator: Tuple of (By, value)

        Returns:
            WebElement: Found element
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise

    def findElements(self, locator: Tuple[By, str]) -> List[WebElement]:
        """
        Find multiple elements

        Args:
            locator: Tuple of (By, value)

        Returns:
            list: List of WebElements
        """
        try:
            elements = self.driver.find_elements(*locator)
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except Exception as e:
            self.logger.error(f"Error finding elements: {locator}, Error: {str(e)}")
            return []

    def clickElement(self, locator: Tuple[By, str]) -> None:
        """
        Click element

        Args:
            locator: Tuple of (By, value)
        """
        element = self.findElement(locator)
        element.click()
        self.logger.info(f"Clicked element: {locator}")

    def enterText(self, locator: Tuple[By, str], text: str) -> None:
        """
        Enter text into element

        Args:
            locator: Tuple of (By, value)
            text: Text to enter
        """
        element = self.findElement(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text into element: {locator}")

    def getText(self, locator: Tuple[By, str]) -> str:
        """
        Get text from element

        Args:
            locator: Tuple of (By, value)

        Returns:
            str: Element text
        """
        element = self.findElement(locator)
        text = element.text
        self.logger.debug(f"Got text from element {locator}: {text}")
        return text

    def isElementVisible(self, locator: Tuple[By, str]) -> bool:
        """
        Check if element is visible

        Args:
            locator: Tuple of (By, value)

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def waitForElement(self, locator: Tuple[By, str], timeout: int = 20) -> None:
        """
        Wait for element to be present

        Args:
            locator: Tuple of (By, value)
            timeout: Timeout in seconds
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        self.logger.info(f"Element appeared: {locator}")

