import pytest
from base.base_api_test import BaseApiTest
from pages.API.api_home import ApiHome
from pages.API.validations import ApiValidations


@pytest.mark.api
class TestUsersApi(BaseApiTest):
    """
    API tests for Users endpoint following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.apiHome = ApiHome(self)
        self.apiValidations = ApiValidations(self)
        self.logger.info("Setting up Users API test")
    
    @pytest.mark.smoke
    def testGetAllUsers(self):
        """Test GET all users"""
        response = self.apiHome.getUsers()
        self.apiValidations.verifyGetAllUsers(response)
    
    @pytest.mark.regression
    def testGetUserById(self):
        """Test GET user by ID"""
        userId = 1
        response = self.apiHome.getUserById(userId)
        self.apiValidations.verifyGetUserById(response, userId)

