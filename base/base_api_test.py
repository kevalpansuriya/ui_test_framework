from typing import Optional, Dict, Any, Union
import requests
from utils.logger import Logger
from utils.config_loader import ConfigLoader


class BaseApiTest:
    """
    Base class for API tests following SRP - handles only API test base functionality
    """
    
    def _initialize(self) -> None:
        """Initialize API test components"""
        self.configLoader: ConfigLoader = ConfigLoader()
        self.logger: Logger = Logger(self.configLoader.getLogPath())
        self.baseUrl: str = self.configLoader.getBaseUrl()
        self.session: requests.Session = requests.Session()
        self.logger.info(f"Initialized API test with base URL: {self.baseUrl}")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
        
        Returns:
            requests.Response: Response object
        """
        url = f"{self.baseUrl}{endpoint}"
        self.logger.info(f"GET request to: {url}")
        response = self.session.get(url, params=params, headers=headers)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def post(self, endpoint: str, data: Optional[Union[Dict[str, Any], str]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform POST request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json: JSON data
            headers: Request headers
        
        Returns:
            requests.Response: Response object
        """
        url = f"{self.baseUrl}{endpoint}"
        self.logger.info(f"POST request to: {url}")
        response = self.session.post(url, data=data, json=json, headers=headers)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def put(self, endpoint: str, data: Optional[Union[Dict[str, Any], str]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform PUT request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json: JSON data
            headers: Request headers
        
        Returns:
            requests.Response: Response object
        """
        url = f"{self.baseUrl}{endpoint}"
        self.logger.info(f"PUT request to: {url}")
        response = self.session.put(url, data=data, json=json, headers=headers)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform DELETE request
        
        Args:
            endpoint: API endpoint
            headers: Request headers
        
        Returns:
            requests.Response: Response object
        """
        url = f"{self.baseUrl}{endpoint}"
        self.logger.info(f"DELETE request to: {url}")
        response = self.session.delete(url, headers=headers)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def assertStatusCode(self, response: requests.Response, expectedStatusCode: int) -> None:
        """
        Assert response status code
        
        Args:
            response: Response object
            expectedStatusCode: Expected status code
        """
        assert response.status_code == expectedStatusCode, \
            f"Expected status code {expectedStatusCode}, but got {response.status_code}"
        self.logger.info(f"Status code assertion passed: {response.status_code}")
    
    def assertResponseContains(self, response: requests.Response, key: str, value: Optional[Any] = None) -> None:
        """
        Assert response contains key/value
        
        Args:
            response: Response object
            key: Key to check
            value: Optional value to check
        """
        responseJson = response.json()
        assert key in responseJson, f"Key '{key}' not found in response"
        if value is not None:
            assert responseJson[key] == value, \
                f"Expected '{key}' to be '{value}', but got '{responseJson[key]}'"
        self.logger.info(f"Response contains assertion passed for key: {key}")

