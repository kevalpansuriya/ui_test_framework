"""Pytest fixtures and hooks for Playwright UI tests (Chrome only)."""

import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure project root is importable when pytest is started from a subfolder
_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pytest

from utils.config_loader import ConfigLoader
from utils.screenshot import ScreenshotHelper


@pytest.fixture(scope="session")
def test_config() -> ConfigLoader:
    return ConfigLoader()


def _is_ci() -> bool:
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"


@pytest.fixture(scope="session")
def browser_type_launch_args(test_config):
    """Always use installed Google Chrome (not bundled Chromium)."""
    settings = test_config.get_playwright_settings()
    headless = settings.get("headless", False)
    if _is_ci():
        headless = True

    return {
        "headless": headless,
        "channel": "chrome",
        "args": ["--disable-blink-features=AutomationControlled"],
    }


@pytest.fixture(scope="session")
def browser_context_args(test_config):
    """Browser context: viewport, locale, and a normal desktop user-agent."""
    settings = test_config.get_playwright_settings()
    viewport = settings.get("viewport", {"width": 1920, "height": 1080})

    return {
        "viewport": viewport,
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure: save a screenshot and print where to find the Playwright trace."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    if "page" not in item.fixturenames:
        return

    page = item.funcargs.get("page")
    if not page:
        return

    config = ConfigLoader()
    helper = ScreenshotHelper(config.get_screenshot_path())
    screenshot_path = helper.capture_failure(page, item.name)
    if screenshot_path:
        print(f"\nScreenshot saved: {screenshot_path}")

    trace_dir = Path(config.get_trace_path())
    if trace_dir.exists():
        print("\nPlaywright trace (open after failure):")
        print(f"  playwright show-trace {trace_dir}")
        print("  Or browse zip files under test-results/ in the project folder.")


def pytest_configure(config):
    """Create output folders before tests run."""
    for folder in ("reports", "logs", "screenshots", "test-results"):
        Path(folder).mkdir(exist_ok=True)

    if hasattr(config.option, "html") and config.option.html and not getattr(config.option, "htmlpath", None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config.option.htmlpath = str(Path("reports") / f"report_{timestamp}.html")
