"""
Base API class with common functionality
"""
from typing import Any
import requests
from base.base_api_test import BaseApiTest


class BaseApi:
    """
    Base API class with common functionality for all API classes
    """
    
    def __init__(self, apiTest: BaseApiTest) -> None:
        self.apiTest = apiTest
        self.logger = apiTest.logger
    
    def _validateResponse(self, response: requests.Response, expectedStatusCode: int) -> Any:
        """
        Common validation method to check status code and return JSON response
        
        Args:
            response: Response object from API call
            expectedStatusCode: Expected HTTP status code
            
        Returns:
            JSON data from response
        """
        self.apiTest.assertStatusCode(response, expectedStatusCode)
        return response.json()

