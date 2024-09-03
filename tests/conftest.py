import pytest
from utils.browser_manager import BrowserManager
from utils.logger import setup_logger
from utils.config import load_config

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
def logger():
    return setup_logger()

@pytest.fixture(scope="function")
def page():
    manager = BrowserManager()
    page = manager.launch_browser()
    yield page
    page.context.close()
    page.browser.close()
