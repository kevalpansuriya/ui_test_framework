from typing import Dict, Any, Optional
import json
import os
from pathlib import Path


class ConfigLoader:
    """
    Configuration loader class following SRP - handles only configuration loading
    """
    
    def __init__(self, configPath: str = "config/config.json") -> None:
        self.configPath: str = configPath
        self.config: Dict[str, Any] = self._loadConfig()
    
    def _loadConfig(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            configFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.configPath)
            with open(configFilePath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Config file not found at {self.configPath}, using default values")
            return self._getDefaultConfig()
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file, using default values")
            return self._getDefaultConfig()
    
    def _getDefaultConfig(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "baseUrl": "https://jsonplaceholder.typicode.com",
            "uiBaseUrl": "https://the-internet.herokuapp.com",
            "browser": "chrome",
            "headless": False,
            "implicitWait": 10,
            "explicitWait": 20,
            "screenshotPath": "screenshots",
            "logPath": "logs"
        }
    
    def get(self, key: str, defaultValue: Optional[Any] = None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key, defaultValue)
    
    def getBaseUrl(self) -> str:
        """Get API base URL"""
        return self.config.get("baseUrl", "https://jsonplaceholder.typicode.com")
    
    def getUiBaseUrl(self) -> str:
        """Get UI base URL"""
        return self.config.get("uiBaseUrl", "https://the-internet.herokuapp.com")
    
    def getBrowser(self) -> str:
        """Get browser name"""
        return self.config.get("browser", "chrome")
    
    def isHeadless(self) -> bool:
        """Check if headless mode is enabled"""
        return self.config.get("headless", False)
    
    def getImplicitWait(self) -> int:
        """Get implicit wait time"""
        return self.config.get("implicitWait", 10)
    
    def getExplicitWait(self) -> int:
        """Get explicit wait time"""
        return self.config.get("explicitWait", 20)
    
    def getScreenshotPath(self) -> str:
        """Get screenshot directory path"""
        return self.config.get("screenshotPath", "screenshots")
    
    def getLogPath(self) -> str:
        """Get log directory path"""
        return self.config.get("logPath", "logs")

