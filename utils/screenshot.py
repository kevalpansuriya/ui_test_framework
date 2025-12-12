from typing import Optional
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver


class Screenshot:
    """
    Screenshot utility class following SRP - handles only screenshot functionality
    """
    
    def __init__(self, screenshotPath: str = "screenshots") -> None:
        self.screenshotPath: str = screenshotPath
        self._createScreenshotDirectory()
    
    def _createScreenshotDirectory(self) -> None:
        """Create screenshot directory if it doesn't exist"""
        Path(self.screenshotPath).mkdir(parents=True, exist_ok=True)
    
    def takeScreenshot(self, driver: WebDriver, testName: str) -> Optional[str]:
        """
        Take screenshot of the current browser state
        
        Args:
            driver: Selenium WebDriver instance
            testName: Name of the test case
        
        Returns:
            str: Path to the screenshot file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Clean test name for filename
            cleanTestName = testName.replace(" ", "_").replace("::", "_")
            screenshotFileName = f"{cleanTestName}_{timestamp}.png"
            screenshotFilePath = os.path.join(self.screenshotPath, screenshotFileName)
            
            driver.save_screenshot(screenshotFilePath)
            return screenshotFilePath
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
    
    def takeScreenshotOnFailure(self, driver: WebDriver, testName: str) -> Optional[str]:
        """
        Take screenshot specifically for test failures
        
        Args:
            driver: Selenium WebDriver instance
            testName: Name of the test case
        
        Returns:
            str: Path to the screenshot file
        """
        return self.takeScreenshot(driver, f"FAILED_{testName}")

