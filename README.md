# Test Automation Framework

A comprehensive test automation framework built with Python, pytest, and Selenium following best practices including Single Responsibility Principle (SRP), camelCase naming conventions, Page Object Model (POM), logging, and automatic screenshot capture on test failures.

## Features

- ✅ **Single Responsibility Principle (SRP)**: Each class has a single, well-defined responsibility
- ✅ **camelCase Naming**: All variables and methods follow camelCase convention
- ✅ **API Testing**: Complete support for REST API testing
- ✅ **UI Testing**: Full Selenium WebDriver support for browser automation
- ✅ **Page Object Model (POM)**: Clean separation of page logic from test logic
- ✅ **Logging**: Comprehensive logging system with file and console output
- ✅ **Screenshot on Failure**: Automatic screenshot capture when tests fail
- ✅ **Configuration Management**: Centralized configuration using JSON
- ✅ **pytest Integration**: Full pytest support with fixtures and hooks

## Project Structure

```
employee_details-/
├── config/
│   └── config.json          # Configuration file
├── base/
│   ├── base_api_test.py     # Base class for API tests
│   └── base_ui_test.py      # Base class for UI tests
├── pages/
│   ├── base_page.py         # Base Page Object Model class
│   ├── login_page.py        # Login page POM
│   └── home_page.py         # Home page POM
├── utils/
│   ├── logger.py            # Logging utility
│   ├── screenshot.py        # Screenshot utility
│   └── config_loader.py     # Configuration loader
├── tests/
│   ├── api/
│   │   ├── test_posts_api.py    # API tests for posts
│   │   └── test_users_api.py    # API tests for users
│   └── ui/
│       ├── test_login.py        # UI tests for login
│       └── test_home_page.py    # UI tests for home page
├── conftest.py              # pytest configuration and fixtures
├── requirements.txt         # Python dependencies
└── README.md               # This file
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

### Run with Verbose Output
```bash
pytest -v
```

## Framework Architecture

### Single Responsibility Principle (SRP)

Each class follows SRP:
- **BaseApiTest**: Handles only API test base functionality
- **BaseUiTest**: Handles only UI test base functionality
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

### Logging

The framework includes comprehensive logging:
- Logs are saved to `logs/` directory with timestamps
- Console output for real-time monitoring
- Different log levels: INFO, DEBUG, ERROR, WARNING, CRITICAL

### Screenshot on Failure

Screenshots are automatically captured when tests fail:
- Screenshots saved to `screenshots/` directory
- Named with test name and timestamp
- Integrated with pytest hooks

## Writing Tests

### API Test Example

```python
from base.base_api_test import BaseApiTest

class TestMyApi(BaseApiTest):
    def setup_method(self):
        super().__init__()
    
    def testGetData(self):
        response = self.get("/endpoint")
        self.assertStatusCode(response, 200)
        self.assertResponseContains(response, "key", "value")
```

### UI Test Example

```python
from pages.login_page import LoginPage
from base.base_ui_test import BaseUiTest

class TestLogin(BaseUiTest):
    def setup_method(self):
        super().__init__()
        self.setUp()
        self.loginPage = LoginPage(self.driver)
    
    def teardown_method(self):
        self.tearDown()
    
    def testLogin(self):
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

## Output Files

- **Logs**: `logs/test_YYYYMMDD_HHMMSS.log`
- **Screenshots**: `screenshots/FAILED_testname_YYYYMMDD_HHMMSS.png`
- **Reports**: HTML reports generated by pytest-html

## Best Practices

1. **Follow SRP**: Each class should have a single responsibility
2. **Use camelCase**: All variables and methods should use camelCase
3. **Page Object Model**: Create page objects for each page/module
4. **Use Base Classes**: Extend base classes for common functionality
5. **Logging**: Use logger for important operations and debugging
6. **Configuration**: Keep all configuration in `config/config.json`
7. **Test Organization**: Organize tests by type (API/UI) and feature

## Troubleshooting

### WebDriver Issues
- Ensure ChromeDriver or GeckoDriver is in PATH
- Or use webdriver-manager (included in requirements)

### Import Errors
- Ensure all `__init__.py` files are present
- Check Python path includes project root

### Screenshot Not Captured
- Check `screenshots/` directory exists
- Verify test is using `driver` fixture from conftest.py

## Contributing

When adding new features:
1. Follow SRP principles
2. Use camelCase naming
3. Add appropriate logging
4. Update documentation
5. Add tests for new functionality

## License

This project is open source and available for use.
