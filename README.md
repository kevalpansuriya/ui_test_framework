# Test Automation Framework

A comprehensive test automation framework built with Python, pytest, and Selenium following best practices including Single Responsibility Principle (SRP), camelCase naming conventions, Page Object Model (POM), logging, and automatic screenshot capture on test failures.

## Features

- ✅ **Single Responsibility Principle (SRP)**: Each class has a single, well-defined responsibility
- ✅ **camelCase Naming**: All variables and methods follow camelCase convention
- ✅ **API Testing**: Complete support for REST API testing with separate API classes
- ✅ **UI Testing**: Full Selenium WebDriver support for browser automation
- ✅ **Page Object Model (POM)**: Clean separation of page logic from test logic
- ✅ **Logging**: Comprehensive logging system with file and console output
- ✅ **Screenshot on Failure**: Automatic screenshot capture when UI tests fail
- ✅ **Configuration Management**: Centralized configuration using JSON
- ✅ **pytest Integration**: Full pytest support with fixtures and hooks
- ✅ **CI/CD Ready**: GitHub Actions workflow with artifact uploads
- ✅ **Test Documentation**: Detailed test steps in plain English for all tests
- ✅ **Headless Mode Support**: Automatic headless mode in CI environments
- ✅ **Code Quality**: Automated linting with flake8 and pylint
- ✅ **Naming Conventions**: Enforced camelCase for variables and methods

## Project Structure

```
gen2/
├── .github/
│   └── workflows/
│       ├── tests.yml              # GitHub Actions CI/CD workflow
│       └── lint.yml               # GitHub Actions linting workflow
├── .flake8                        # flake8 configuration
├── .pylintrc                      # pylint configuration
├── config/
│   └── config.json                # Configuration file
├── base/
│   ├── base_api_test.py           # Base class for API tests
│   └── base_ui_test.py            # Base class for UI tests
├── pages/
│   ├── API/
│   │   ├── __init__.py            # API package exports
│   │   ├── base_api.py            # Base API class with common functionality
│   │   ├── posts_api.py           # Posts API class with endpoints and validations
│   │   └── users_api.py           # Users API class with endpoints and validations
│   └── UI/
│       ├── base_page.py           # Base Page Object Model class
│       ├── login_page.py          # Login page POM
│       └── home_page.py           # Home page POM
├── utils/
│   ├── logger.py                  # Logging utility
│   ├── screenshot.py              # Screenshot utility
│   └── config_loader.py           # Configuration loader
├── tests/
│   ├── api/
│   │   ├── test_posts_api.py      # API tests for posts
│   │   └── test_users_api.py      # API tests for users
│   └── ui/
│       ├── test_login.py          # UI tests for login
│       └── test_home_page.py      # UI tests for home page
├── conftest.py                    # pytest configuration and fixtures
├── run_tests_with_report.py       # Script to run tests with HTML reports
├── run_linting.py                 # Script to run linting checks locally
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Setup

### Prerequisites

- Python 3.8 or higher
- Chrome or Firefox browser installed
- ChromeDriver or GeckoDriver (automatically managed by webdriver-manager)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the framework:**
   Edit `config/config.json` to set your test environment:
   ```json
   {
     "baseUrl": "https://jsonplaceholder.typicode.com",
     "uiBaseUrl": "https://the-internet.herokuapp.com",
     "browser": "chrome",
     "headless": false,
     "implicitWait": 10,
     "explicitWait": 20,
     "screenshotPath": "screenshots",
     "logPath": "logs"
   }
   ```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run API Tests Only
```bash
pytest tests/api/
```

### Run UI Tests Only
```bash
pytest tests/ui/
```

### Run Specific Test File
```bash
pytest tests/api/test_posts_api.py
```

### Run Tests by Marker
```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run API tests
pytest -m api

# Run UI tests
pytest -m ui

# Run UI regression tests
pytest -m "ui and regression"
```

### Run with HTML Report (with timestamp and logs)
```bash
python run_tests_with_report.py
```

Or manually:
```bash
pytest --html=reports/report_YYYYMMDD_HHMMSS.html --self-contained-html
```

**Note:** Logs are automatically included in the HTML report and displayed in the console during test execution.

### Run in Headless Mode
Update `config/config.json` to set `"headless": true`

**Note:** Headless mode is automatically enabled in CI environments (GitHub Actions).

### Run with Verbose Output
```bash
pytest -v
```

## Code Quality and Linting

The framework includes automated code quality checks using flake8 and pylint.

### Linting Rules

- **Line Length**: Maximum 120 characters per line
- **Naming Convention**: camelCase for variables, methods, and functions
- **Unused Variables**: Not allowed (will fail linting)
- **Code Complexity**: Maximum complexity of 10
- **Pylint Score**: Minimum score of 7.0/10

### Run Linting Locally

```bash
# Run all linting checks
python run_linting.py

# Or run individually:
# flake8 checks
flake8 . --max-line-length=120

# Check for unused variables
flake8 . --select=F841

# pylint checks
pylint --rcfile=.pylintrc .
```

### Linting Configuration

- **`.flake8`**: Configuration for flake8
  - Max line length: 120 characters
  - Checks for unused variables (F841)
  - Excludes common directories (venv, __pycache__, etc.)

- **`.pylintrc`**: Configuration for pylint
  - Variable naming: camelCase (`^[a-z][a-zA-Z0-9]*$`)
  - Method naming: camelCase
  - Function naming: camelCase
  - Class naming: PascalCase
  - Max line length: 120 characters
  - Unused variables: Enabled
  - Minimum score: 7.0/10

### CI/CD Linting

The linting workflow (`.github/workflows/lint.yml`) automatically runs on:
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches

The workflow checks:
1. **Critical errors** (syntax errors, etc.)
2. **All flake8 checks** (line length, complexity, etc.)
3. **Unused variables** (F841)
4. **Pylint code quality** (naming conventions, unused variables, etc.)

If any linting check fails, the CI pipeline will fail and you'll need to fix the issues before merging.

## Framework Architecture

### API Testing Structure

The API testing framework is organized by domain:

- **`base_api.py`**: Base class with common functionality (`_validateResponse` method)
- **`posts_api.py`**: PostsApi class containing:
  - `EndPoints` class with posts-related endpoints
  - API methods: `getPosts()`, `getPostById()`, `createPost()`, `updatePost()`, `deletePost()`
  - Validation methods: `verifyGetAllPosts()`, `verifyGetPostById()`, `verifyCreatePost()`, etc.
- **`users_api.py`**: UsersApi class containing:
  - `EndPoints` class with users-related endpoints
  - API methods: `getUsers()`, `getUserById()`
  - Validation methods: `verifyGetAllUsers()`, `verifyGetUserById()`

### Endpoint Naming Convention

Endpoints follow the pattern: `HTTP_METHOD_RESOURCE_NAME`
- `GET_POSTS` - Get all posts
- `GET_POST_BY_ID` - Get post by ID
- `POST_CREATE_POST` - Create a new post
- `PUT_UPDATE_POST` - Update a post
- `DELETE_POST` - Delete a post
- `GET_USERS` - Get all users
- `GET_USER_BY_ID` - Get user by ID

### Single Responsibility Principle (SRP)

Each class follows SRP:
- **BaseApiTest**: Handles only API test base functionality
- **BaseUiTest**: Handles only UI test base functionality
- **BaseApi**: Handles only common API functionality
- **PostsApi**: Handles only posts-related API operations
- **UsersApi**: Handles only users-related API operations
- **Logger**: Handles only logging functionality
- **Screenshot**: Handles only screenshot functionality
- **ConfigLoader**: Handles only configuration loading
- **BasePage**: Handles only page base functionality
- **Page Objects**: Each page object handles only its specific page

### camelCase Naming Convention

All variables and methods use camelCase:
```python
usernameInputLocator = (By.ID, "username")
passwordInputLocator = (By.ID, "password")
loginButtonLocator = (By.CSS_SELECTOR, "button[type='submit']")

def enterUsername(self, username):
    self.enterText(self.usernameInputLocator, username)
```

### Page Object Model (POM)

Page objects encapsulate page-specific logic:
```python
class LoginPage(BasePage):
    usernameInputLocator = (By.ID, "username")
    passwordInputLocator = (By.ID, "password")
    
    def login(self, username, password):
        self.enterUsername(username)
        self.enterPassword(password)
        self.clickLoginButton()
```

### Test Documentation

All tests include detailed test steps in plain English within their docstrings:
```python
def testGetAllPosts(self):
    """
    Test GET all posts
    
    Test Steps:
    1. Send a GET request to retrieve all posts from the API
    2. Verify that the response status code is 200 (success)
    3. Verify that the response contains a list of posts
    4. Verify that the list is not empty
    5. Log the number of posts retrieved
    """
```

### Logging

The framework includes comprehensive logging:
- Logs are saved to `logs/` directory with timestamps
- Console output for real-time monitoring
- Different log levels: INFO, DEBUG, ERROR, WARNING, CRITICAL
- Logs are included in HTML test reports

### Screenshot on Failure

Screenshots are automatically captured when UI tests fail:
- Screenshots saved to `screenshots/` directory
- Named with test name and timestamp: `FAILED_testname_YYYYMMDD_HHMMSS.png`
- Integrated with pytest hooks
- Automatically attached to test reports

### Common Validation Method

The framework includes a shared `_validateResponse()` method in `BaseApi`:
- Validates HTTP status code
- Returns JSON response data
- Reduces code duplication across validation methods

## Writing Tests

### API Test Example

```python
from base.base_api_test import BaseApiTest
from pages.API.posts_api import PostsApi

class TestMyApi(BaseApiTest):
    def setup_method(self):
        self._initialize()
        self.postsApi = PostsApi(self)
    
    def testGetAllPosts(self):
        """
        Test GET all posts
        
        Test Steps:
        1. Send a GET request to retrieve all posts
        2. Verify the response status code is 200
        3. Verify the response contains a list of posts
        """
        response = self.postsApi.getPosts()
        self.postsApi.verifyGetAllPosts(response)
```

### UI Test Example

```python
from pages.UI.login_page import LoginPage
from base.base_ui_test import BaseUiTest

class TestLogin(BaseUiTest):
    def setup_method(self):
        self._initialize()
        self.setUp()
        self.loginPage = LoginPage(self.driver)
    
    def teardown_method(self):
        self.tearDown()
    
    def testLogin(self):
        """
        Test successful login
        
        Test Steps:
        1. Navigate to the login page
        2. Enter username and password
        3. Click login button
        4. Verify success message
        """
        self.navigateTo("/login")
        self.loginPage.login("username", "password")
        assert self.loginPage.isSuccessMessageVisible()
```

## Configuration

### Browser Options
- `chrome`: Use Chrome browser
- `firefox`: Use Firefox browser

### Wait Times
- `implicitWait`: Implicit wait time in seconds
- `explicitWait`: Explicit wait time in seconds

### URLs
- `baseUrl`: Base URL for API tests
- `uiBaseUrl`: Base URL for UI tests

### CI/CD Configuration

The framework automatically detects CI environments and:
- Enables headless mode for browsers
- Adds additional Chrome options for CI compatibility
- Uses `--headless=new` for modern Chrome versions
- Configures remote debugging port for CI environments

## GitHub Actions CI/CD

The framework includes a GitHub Actions workflow (`.github/workflows/tests.yml`) that:

### Features:
- Runs tests in parallel using matrix strategy
- Tests multiple test suites: api-smoke, ui-regression, and all tests
- Automatically generates HTML reports for each test run
- Uploads artifacts for download:
  - **Test Reports**: HTML reports with test results
  - **Test Logs**: All log files from test execution
  - **Screenshots**: Screenshots captured on test failures
  - **Test Files**: All test Python files
- Artifacts are retained for 30 days
- Automatically configures Chrome for headless mode in CI

### Workflow Triggers:
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches

### Viewing Results:
1. Go to the **Actions** tab in your GitHub repository
2. Click on the workflow run
3. Scroll down to the **Artifacts** section
4. Download the artifacts for each test suite

## Output Files

- **Logs**: `logs/test_YYYYMMDD_HHMMSS.log`
- **Screenshots**: `screenshots/FAILED_testname_YYYYMMDD_HHMMSS.png`
- **Reports**: `reports/report_YYYYMMDD_HHMMSS.html` (HTML reports with embedded logs)

## Test Examples

### Failing UI Test (Screenshot Capture)

The framework includes a test (`testNonExistentElement`) that intentionally fails to demonstrate screenshot capture:
- Navigates to a page
- Tries to find a non-existent element
- Fails and automatically captures a screenshot
- Screenshot is saved and attached to the test report

### Failing API Test (Error Reporting)

The framework includes a test (`testGetPostWithInvalidId`) that demonstrates error handling:
- Attempts to retrieve a post with an invalid ID
- Shows detailed error information in the test report
- Demonstrates how API test failures are reported

## Best Practices

1. **Follow SRP**: Each class should have a single responsibility
2. **Use camelCase**: All variables and methods should use camelCase
3. **Page Object Model**: Create page objects for each page/module
4. **Use Base Classes**: Extend base classes for common functionality
5. **Logging**: Use logger for important operations and debugging
6. **Configuration**: Keep all configuration in `config/config.json`
7. **Test Organization**: Organize tests by type (API/UI) and feature
8. **Documentation**: Include test steps in docstrings for clarity
9. **Error Handling**: Use validation methods for consistent error reporting
10. **CI/CD**: Leverage GitHub Actions for automated testing

## Troubleshooting

### WebDriver Issues
- Ensure ChromeDriver or GeckoDriver is in PATH
- Or use webdriver-manager (included in requirements)
- In CI environments, Chrome is automatically configured

### Import Errors
- Ensure all `__init__.py` files are present
- Check Python path includes project root
- Verify PYTHONPATH is set correctly

### Screenshot Not Captured
- Check `screenshots/` directory exists
- Verify test is using `driver` fixture from conftest.py
- Ensure test is actually failing (not skipped)

### CI/CD Issues
- Check GitHub Actions logs for detailed error messages
- Verify Chrome options are correctly configured
- Ensure all dependencies are in `requirements.txt`
- Check that directories are created before test execution

### API Test Failures
- Verify base URL is correct in `config/config.json`
- Check network connectivity
- Review response status codes and error messages
- Check logs for detailed error information

## Contributing

When adding new features:
1. Follow SRP principles
2. Use camelCase naming
3. Add appropriate logging
4. Include test steps in docstrings
5. Update documentation
6. Add tests for new functionality
7. Ensure CI/CD compatibility

## License

This project is open source and available for use.
