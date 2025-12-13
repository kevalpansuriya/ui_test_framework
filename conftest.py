import pytest
import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config_loader import ConfigLoader
from utils.logger import Logger
from utils.screenshot import Screenshot


@pytest.fixture(scope="session")
def config():
    """Configuration fixture"""
    return ConfigLoader()


@pytest.fixture(scope="session")
def logger(config):
    """Logger fixture"""
    return Logger(config.getLogPath())


@pytest.fixture(scope="function")
def driver(config):
    """
    WebDriver fixture with screenshot on failure
    
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    browser = config.getBrowser().lower()
    headless = config.isHeadless()
    
    # Detect CI environment
    is_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"
    if is_ci:
        headless = True  # Force headless in CI
    
    # Setup WebDriver
    if browser == "chrome":
        chromeOptions = Options()
        if headless:
            chromeOptions.add_argument("--headless=new")  # Use new headless mode
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--window-size=1920,1080")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("--disable-software-rasterizer")
        chromeOptions.add_argument("--disable-background-timer-throttling")
        chromeOptions.add_argument("--disable-backgrounding-occluded-windows")
        chromeOptions.add_argument("--disable-renderer-backgrounding")
        chromeOptions.add_argument("--disable-features=TranslateUI")
        chromeOptions.add_argument("--disable-ipc-flooding-protection")
        if is_ci:
            chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeService = ChromeService(ChromeDriverManager().install())
        driverInstance = webdriver.Chrome(service=chromeService, options=chromeOptions)
    elif browser == "firefox":
        firefoxOptions = FirefoxOptions()
        if headless:
            firefoxOptions.add_argument("--headless")
        firefoxService = FirefoxService(GeckoDriverManager().install())
        driverInstance = webdriver.Firefox(service=firefoxService, options=firefoxOptions)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driverInstance.implicitly_wait(config.getImplicitWait())
    driverInstance.maximize_window()
    
    yield driverInstance
    
    # Cleanup
    driverInstance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    # Check if test failed
    if report.when == "call" and report.failed:
        # Get driver from fixture if available
        driver = None
        for fixtureName in item.fixturenames:
            if fixtureName == "driver":
                driver = item.funcargs.get("driver")
                break
        
        if driver:
            screenshot = Screenshot()
            testName = item.name
            screenshotPath = screenshot.takeScreenshotOnFailure(driver, testName)
            if screenshotPath:
                print(f"\nScreenshot saved: {screenshotPath}")
                # Attach screenshot to pytest report
                if hasattr(report, "extra"):
                    if not hasattr(report.extra, "__iter__"):
                        report.extra = []
                    report.extra.append(("image", screenshotPath))


@pytest.fixture(scope="function")
def apiBaseTest():
    """
    API base test fixture
    
    Yields:
        BaseApiTest: Base API test instance
    """
    from base.base_api_test import BaseApiTest
    apiTest = BaseApiTest()
    apiTest._initialize()
    yield apiTest


def pytest_configure(config):
    """
    Configure pytest to generate timestamped HTML reports
    """
    # Create reports directory if it doesn't exist
    reportsDir = Path("reports")
    reportsDir.mkdir(exist_ok=True)
    
    # Only override htmlpath if it's not already set via command line
    # This allows run_tests_with_report.py to set its own timestamped path
    if hasattr(config.option, 'htmlpath') and config.option.htmlpath:
        # If htmlpath is already set (e.g., from command line), use it
        pass
    elif hasattr(config.option, 'html') and config.option.html:
        # If --html option is used without a path, generate timestamped version
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        reportFileName = f"report_{timestamp}.html"
        reportPath = reportsDir / reportFileName
        config.option.htmlpath = str(reportPath)

