from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import Logger
from utils.config_loader import ConfigLoader
from utils.screenshot import Screenshot


class BaseUiTest:
    """
    Base class for UI tests following SRP - handles only UI test base functionality
    """
    
    def _initialize(self) -> None:
        """Initialize UI test components"""
        self.configLoader: ConfigLoader = ConfigLoader()
        self.logger: Logger = Logger(self.configLoader.getLogPath())
        self.screenshot: Screenshot = Screenshot(self.configLoader.getScreenshotPath())
        self.baseUrl: str = self.configLoader.getUiBaseUrl()
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger.info("Initialized UI test base class")
    
    def setUp(self) -> None:
        """Setup WebDriver"""
        browser = self.configLoader.getBrowser().lower()
        headless = self.configLoader.isHeadless()
        
        if browser == "chrome":
            chromeOptions = Options()
            if headless:
                chromeOptions.add_argument("--headless")
            chromeOptions.add_argument("--no-sandbox")
            chromeOptions.add_argument("--disable-dev-shm-usage")
            chromeOptions.add_argument("--disable-gpu")
            chromeOptions.add_argument("--window-size=1920,1080")
            chromeService = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
        elif browser == "firefox":
            firefoxOptions = FirefoxOptions()
            if headless:
                firefoxOptions.add_argument("--headless")
            firefoxService = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=firefoxService, options=firefoxOptions)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Set implicit wait
        implicitWait = self.configLoader.getImplicitWait()
        self.driver.implicitly_wait(implicitWait)
        
        # Setup explicit wait
        explicitWait = self.configLoader.getExplicitWait()
        self.wait = WebDriverWait(self.driver, explicitWait)
        
        # Maximize window
        self.driver.maximize_window()
        
        self.logger.info(f"WebDriver initialized for {browser} browser")
    
    def tearDown(self) -> None:
        """Cleanup WebDriver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
    
    def navigateTo(self, url: str) -> None:
        """
        Navigate to URL
        
        Args:
            url: URL to navigate to
        """
        fullUrl = f"{self.baseUrl}{url}" if url.startswith("/") else url
        self.driver.get(fullUrl)
        self.logger.info(f"Navigated to: {fullUrl}")
    
    def findElement(self, locator: Tuple[By, str], timeout: Optional[float] = None) -> WebElement:
        """
        Find element with wait
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        
        Returns:
            WebElement: Found element
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
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
    
    def isElementVisible(self, locator: Tuple[By, str], timeout: Optional[float] = None) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def takeScreenshot(self, testName: str) -> Optional[str]:
        """
        Take screenshot
        
        Args:
            testName: Name of the test
        
        Returns:
            str: Screenshot file path
        """
        if self.driver:
            return self.screenshot.takeScreenshot(self.driver, testName)
        return None

