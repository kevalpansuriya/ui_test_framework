"""Save screenshots when a Playwright test fails."""

from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page


class ScreenshotHelper:
    """Captures full-page screenshots on test failure."""

    def __init__(self, folder: str = "screenshots") -> None:
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def capture_failure(self, page: Page, test_name: str) -> str | None:
        """Save a screenshot and return the file path."""
        try:
            safe_name = test_name.replace(" ", "_").replace("::", "_").replace("[", "_").replace("]", "")
            file_name = f"FAILED_{safe_name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            file_path = self.folder / file_name
            page.screenshot(path=str(file_path), full_page=True)
            return str(file_path)
        except Exception as error:
            print(f"Could not save screenshot: {error}")
            return None
