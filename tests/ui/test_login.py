import pytest
from pages.UI.login_page import LoginPage
from base.base_ui_test import BaseUiTest


@pytest.mark.ui
class TestLogin(BaseUiTest):
    """
    UI tests for Login page following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.setUp()
        self.loginPage = LoginPage(self.driver)
        self.logger.info("Setting up Login UI test")
    
    def teardown_method(self):
        """Teardown method called after each test"""
        self.tearDown()
    
    @pytest.mark.smoke
    def testSuccessfulLogin(self):
        """Test successful login"""
        self.navigateTo("/login")
        
        username = "tomsmith"
        password = "SuperSecretPassword!"
        
        self.loginPage.login(username, password)
        
        # Verify success message
        assert self.loginPage.isSuccessMessageVisible(), "Success message should be visible"
        successMessage = self.loginPage.getSuccessMessage()
        assert "You logged into a secure area!" in successMessage, "Success message should contain expected text"
        self.logger.info("Login test passed successfully")
    
    @pytest.mark.regression
    def testFailedLoginWithInvalidCredentials(self):
        """Test failed login with invalid credentials"""
        self.navigateTo("/login")
        
        username = "invaliduser"
        password = "invalidpassword"
        
        self.loginPage.login(username, password)
        
        # Verify error message
        assert self.loginPage.isErrorMessageVisible(), "Error message should be visible"
        errorMessage = self.loginPage.getErrorMessage()
        assert "Your username is invalid!" in errorMessage, "Error message should contain expected text"
        self.logger.info("Failed login test passed successfully")
    
    @pytest.mark.regression
    def testFailedLoginWithEmptyFields(self):
        """Test failed login with empty fields"""
        self.navigateTo("/login")
        
        # Try to login without entering credentials
        self.loginPage.clickLoginButton()
        
        # Verify error message
        assert self.loginPage.isErrorMessageVisible(), "Error message should be visible"
        self.logger.info("Empty fields login test passed successfully")

