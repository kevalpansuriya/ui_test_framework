#!/usr/bin/env bash
# One-time setup: virtualenv, Python packages, and Playwright browsers.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
./venv/bin/playwright install chromium

echo ""
echo "Done. Activate: source venv/bin/activate"
echo "Run tests:     PYTHONPATH=. pytest"
echo "View trace:    playwright show-trace test-results/<trace.zip>"
