"""Shared helpers for all Playwright page objects."""

import logging
import re
from typing import Pattern, Union

from playwright.sync_api import Locator, Page


class BasePage:
    """Common browser actions used by every page object."""

    def __init__(self, page: Page, timeout_ms: int = 30_000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms
        self.page.set_default_timeout(timeout_ms)
        self.logger = logging.getLogger(self.__class__.__name__)

    def go_to(self, url: str) -> None:
        """Open a URL and wait for the DOM."""
        self.page.goto(url, wait_until="domcontentloaded")
        self.logger.info("Opened %s", url)

    def click_if_visible(self, button_name_pattern: Union[str, Pattern[str]], wait_ms: int = 2_000) -> None:
        """Click a button (e.g. cookie banner) only when it appears."""
        pattern = (
            button_name_pattern
            if isinstance(button_name_pattern, re.Pattern)
            else re.compile(button_name_pattern, re.IGNORECASE)
        )
        button = self.page.get_by_role("button", name=pattern).first
        try:
            button.wait_for(state="visible", timeout=wait_ms)
            button.click()
            self.logger.info("Clicked button matching: %s", pattern.pattern)
        except Exception:
            pass
