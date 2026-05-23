# One-time setup: virtualenv, Python packages, Playwright browsers, and CLI tools.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Creating virtual environment..."
python -m venv venv

Write-Host "Installing Python dependencies..."
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\pip install -r requirements.txt

Write-Host "Installing Playwright Chrome..."
.\venv\Scripts\playwright install chrome

Write-Host ""
Write-Host "Done. Activate the venv:"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "Run tests:"
Write-Host "  `$env:PYTHONPATH = (Get-Location).Path"
Write-Host "  pytest"
Write-Host ""
Write-Host "View trace after a failure:"
Write-Host "  .\venv\Scripts\playwright show-trace test-results\<path-to-trace.zip>"
