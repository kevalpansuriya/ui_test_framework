import pytest
from base.base_api_test import BaseApiTest
from pages.API.users_api import UsersApi


@pytest.mark.api
class TestUsersApi(BaseApiTest):
    """
    API tests for Users endpoint following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.usersApi = UsersApi(self)
        self.logger.info("Setting up Users API test")
    
    @pytest.mark.smoke
    def testGetAllUsers(self):
        """
        Test GET all users
        
        Test Steps:
        1. Send a GET request to retrieve all users from the API
        2. Verify that the response status code is 200 (success)
        3. Verify that the response contains a list of users
        4. Verify that the list is not empty
        5. Log the number of users retrieved
        """
        response = self.usersApi.getUsers()
        self.usersApi.verifyGetAllUsers(response)
    
    @pytest.mark.regression
    def testGetUserById(self):
        """
        Test GET user by ID
        
        Test Steps:
        1. Set the user ID to 1
        2. Send a GET request to retrieve the user with the specified ID
        3. Verify that the response status code is 200 (success)
        4. Verify that the returned user has the correct ID
        5. Verify that the user contains required fields: name, email, and address
        6. Log that the user was successfully retrieved
        """
        userId = 1
        response = self.usersApi.getUserById(userId)
        self.usersApi.verifyGetUserById(response, userId)

