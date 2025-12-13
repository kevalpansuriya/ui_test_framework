"""
Users API class - Handles all users-related API calls and validations
"""
import requests
from base.base_api_test import BaseApiTest
from pages.API.base_api import BaseApi


class EndPoints:
    """
    Users endpoint definitions
    """
    GET_USERS = "/users"
    GET_USER_BY_ID = "/users/{userId}"


class UsersApi(BaseApi):
    """
    API component library for Users endpoints.
    Encapsulates Users API calls and validation logic for reuse across tests.
    """
    
    def __init__(self, apiTest: BaseApiTest) -> None:
        super().__init__(apiTest)
        self.endPoints = EndPoints()
    
    # Users endpoints
    def getUsers(self) -> requests.Response:
        """Get all users"""
        return self.apiTest.get(self.endPoints.GET_USERS)
    
    def getUserById(self, userId: int) -> requests.Response:
        """Get user by ID"""
        return self.apiTest.get(self.endPoints.GET_USER_BY_ID.format(userId=userId))
    
    # Validation methods
    def verifyGetAllUsers(self, response: requests.Response) -> None:
        """
        Verify GET all users response
        
        Args:
            response: Response object from getUsers call
        """
        users = self._validateResponse(response, 200)
        assert isinstance(users, list), "Response should be a list"
        assert len(users) > 0, "Users list should not be empty"
        self.logger.info(f"Successfully retrieved {len(users)} users")
    
    def verifyGetUserById(self, response: requests.Response, userId: int) -> None:
        """
        Verify GET user by ID response
        
        Args:
            response: Response object from getUserById call
            userId: Expected user ID
        """
        user = self._validateResponse(response, 200)
        assert user["id"] == userId, f"User ID should be {userId}"
        self.apiTest.assertResponseContains(response, "name")
        self.apiTest.assertResponseContains(response, "email")
        self.apiTest.assertResponseContains(response, "address")
        self.logger.info(f"Successfully retrieved user with ID: {userId}")

