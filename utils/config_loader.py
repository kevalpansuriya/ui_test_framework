"""Load test settings from config/config.json."""

import json
import os
from pathlib import Path
from typing import Any


class ConfigLoader:
    """Reads framework settings from a JSON file."""

    DEFAULT_CONFIG = {
        "search_query": "keval pansuriya encora",
        "google_url": "https://www.google.com",
        "screenshot_path": "screenshots",
        "log_path": "logs",
        "trace_path": "test-results",
        "playwright": {
            "browser": "chrome",
            "headless": False,
            "timeout_ms": 30000,
            "viewport": {"width": 1920, "height": 1080},
        },
    }

    def __init__(self, config_path: str = "config/config.json") -> None:
        self.config_path = config_path
        self.settings = self._load()

    def _load(self) -> dict[str, Any]:
        project_root = Path(__file__).resolve().parent.parent
        file_path = project_root / self.config_path

        if not file_path.exists():
            return dict(self.DEFAULT_CONFIG)

        with open(file_path, encoding="utf-8") as file:
            return json.load(file)

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def get_playwright_settings(self) -> dict[str, Any]:
        defaults = self.DEFAULT_CONFIG["playwright"]
        return {**defaults, **self.settings.get("playwright", {})}

    def is_ci(self) -> bool:
        return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

    def get_search_query(self) -> str:
        return self.settings.get("search_query", self.DEFAULT_CONFIG["search_query"])

    def get_google_url(self) -> str:
        return self.settings.get("google_url", self.DEFAULT_CONFIG["google_url"])

    def get_screenshot_path(self) -> str:
        return self.settings.get("screenshot_path", self.DEFAULT_CONFIG["screenshot_path"])

    def get_log_path(self) -> str:
        return self.settings.get("log_path", self.DEFAULT_CONFIG["log_path"])

    def get_trace_path(self) -> str:
        return self.settings.get("trace_path", self.DEFAULT_CONFIG["trace_path"])
