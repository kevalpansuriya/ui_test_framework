import pytest
from pages.UI.home_page import HomePage
from base.base_ui_test import BaseUiTest


@pytest.mark.ui
class TestHomePage(BaseUiTest):
    """
    UI tests for Home page following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.setUp()
        self.homePage = HomePage(self.driver)
        self.logger.info("Setting up Home Page UI test")
    
    def teardown_method(self):
        """Teardown method called after each test"""
        self.tearDown()
    
    @pytest.mark.smoke
    def testHomePageLoads(self):
        """Test that home page loads correctly"""
        self.navigateTo("/")
        
        # Verify page is loaded
        assert self.homePage.isPageLoaded(), "Home page should be loaded"
        self.logger.info("Home page load test passed successfully")
    
    @pytest.mark.regression
    def testPageTitleExists(self):
        """Test that page title exists"""
        self.navigateTo("/")
        
        pageTitle = self.homePage.getPageTitle()
        assert pageTitle is not None, "Page title should exist"
        assert len(pageTitle) > 0, "Page title should not be empty"
        self.logger.info(f"Page title test passed. Title: {pageTitle}")

