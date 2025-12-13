import pytest
from selenium.webdriver.common.by import By
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
        """
        Test that home page loads correctly
        
        Test Steps:
        1. Navigate to the home page (root URL)
        2. Verify that the page has loaded successfully
        3. Verify that the page elements are present and visible
        4. Log that the home page load test passed successfully
        """
        self.navigateTo("/")
        
        # Verify page is loaded
        assert self.homePage.isPageLoaded(), "Home page should be loaded"
        self.logger.info("Home page load test passed successfully")
    
    @pytest.mark.regression
    def testPageTitleExists(self):
        """
        Test that page title exists
        
        Test Steps:
        1. Navigate to the home page (root URL)
        2. Get the page title from the page
        3. Verify that the page title exists (is not None)
        4. Verify that the page title is not empty (has content)
        5. Log the page title and that the test passed successfully
        """
        self.navigateTo("/")
        
        pageTitle = self.homePage.getPageTitle()
        assert pageTitle is not None, "Page title should exist"
        assert len(pageTitle) > 0, "Page title should not be empty"
        self.logger.info(f"Page title test passed. Title: {pageTitle}")
    
    @pytest.mark.regression
    def testNonExistentElement(self):
        """
        Test that intentionally fails to demonstrate screenshot capture on failure
        
        Test Steps:
        1. Navigate to the home page (root URL)
        2. Try to find an element that does not exist on the page
        3. This test will fail and trigger automatic screenshot capture
        4. The screenshot will be saved in the screenshots directory
        """
        self.navigateTo("/")
        
        # This will fail because the element doesn't exist - screenshot will be captured
        # The findElement method will raise a TimeoutException when element is not found
        nonExistentElement = self.findElement((By.ID, "non-existent-element-id"), timeout=2)
        assert nonExistentElement is not None, "This test intentionally fails to demonstrate screenshot capture"

