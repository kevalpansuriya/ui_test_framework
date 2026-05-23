# UI Test Framework (Playwright + pytest)

A small, readable UI automation framework using **Python**, **pytest**, and **Playwright**.  
It includes one sample test: search Google for a name and open the first LinkedIn profile.

## Features

- **Playwright** for fast, reliable browser automation
- **Page Object Model** with clear, snake_case Python code
- **Trace on failure** — video + trace zip saved under `test-results/`
- **Screenshot on failure** — PNG saved under `screenshots/`
- **Google → DuckDuckGo fallback** when Google shows a CAPTCHA
- **Playwright MCP** in Cursor for AI-assisted test development
- **GitHub Actions** CI with artifact upload on failure

## Project structure

```
ui_test_framework/
├── .cursor/
│   └── mcp.json              # Playwright MCP for Cursor
├── config/
│   └── config.json           # URLs, search query, browser settings
├── pages/
│   ├── base_page.py          # Shared browser helpers
│   ├── google_search_page.py
│   ├── duckduckgo_search_page.py
│   └── web_search.py         # Main search flow + fallback
├── tests/
│   └── ui/
│       └── test_google_linkedin_search.py
├── utils/
│   ├── config_loader.py
│   ├── logger.py
│   └── screenshot.py
├── scripts/
│   ├── setup.ps1             # Windows setup
│   └── setup.sh              # macOS / Linux setup
├── conftest.py               # Playwright fixtures + failure hooks
├── pytest.ini                # pytest + trace/video on failure
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- **Node.js 18+** (only for Playwright MCP in Cursor)
- Google Chrome installed locally (recommended — reduces Google CAPTCHA)

## Setup

### Windows

```powershell
cd ui_test_framework
.\scripts\setup.ps1
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
```

### macOS / Linux

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
source venv/bin/activate
export PYTHONPATH=.
```

### Manual setup

```bash
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
playwright install chromium
```

## Run tests

```bash
# All tests (trace + video kept only on failure)
pytest

# Smoke test only
pytest -m smoke

# Visible browser window
pytest --headed

# HTML report
python run_tests_with_report.py
```

## View trace after a failure

Playwright saves a trace zip when a test fails (`retain-on-failure` in `pytest.ini`).

```bash
# List trace files
dir test-results   # Windows
ls test-results    # macOS / Linux

# Open the trace viewer (use the path to your trace.zip)
playwright show-trace test-results\...\trace.zip
```

The trace viewer shows clicks, network, DOM snapshots, and timing — ideal for debugging flaky tests.

## Playwright CLI (installed with the package)

| Command | Purpose |
|--------|---------|
| `playwright install` | Download browser binaries |
| `playwright install chromium` | Install Chromium only |
| `playwright codegen google.com` | Record actions → Python code |
| `playwright show-trace <file.zip>` | Open trace viewer |
| `playwright --help` | Full CLI reference |

Run via the venv: `.\venv\Scripts\playwright` (Windows) or `./venv/bin/playwright`.

## Playwright MCP in Cursor (feature development)

This repo includes [Playwright MCP](https://playwright.dev/docs/getting-started-mcp) so Cursor can drive a real browser while you write tests.

1. Install **Node.js 18+**
2. Open the project in **Cursor**
3. Confirm `.cursor/mcp.json` exists (already added):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

4. **Cursor Settings → MCP** — ensure `playwright` is enabled (green)
5. Restart Cursor if the server does not connect
6. Ask the agent to navigate pages, inspect elements, or help build page objects

Use MCP while authoring tests; run `pytest` to execute them in CI and locally.

## Configuration

Edit `config/config.json`:

| Key | Description |
|-----|-------------|
| `search_query` | Text to search for |
| `search_engine` | Primary engine: `google` |
| `search_engine_fallback` | Used when Google CAPTCHA appears: `duckduckgo` |
| `playwright.headless` | `false` locally, forced `true` in CI |
| `playwright.use_chrome_channel` | Use installed Chrome instead of bundled Chromium |

## Writing a new test

```python
import pytest
from pages.web_search import WebSearch

@pytest.mark.ui
def test_example(page, test_config):
    search = WebSearch(page, test_config)
    linkedin = search.search_and_open_first_linkedin_profile("your query")
    assert "linkedin.com" in linkedin.url
```

## CI (GitHub Actions)

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

| Job | What it runs | When |
|-----|----------------|------|
| **lint** | `flake8` (uses `.flake8` in the repo) | Every push / PR to `main` or `master` |
| **smoke** | `pytest -m smoke` with Playwright + Chromium | After lint passes |

Smoke tests run headless in CI (`CI=true`). On failure, artifacts include screenshots, traces, and videos from `test-results/`.

Run the same checks locally:

```bash
flake8 .
pytest -m smoke
```

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Google CAPTCHA | Run `pytest --headed` with Chrome installed; or rely on DuckDuckGo fallback |
| `playwright` not found | Activate venv and run `pip install -r requirements.txt` |
| MCP not connecting | Install Node.js, restart Cursor, check MCP panel |
| No trace file | Traces are only kept when a test **fails** (`retain-on-failure`) |

## License

Open source — use freely.
