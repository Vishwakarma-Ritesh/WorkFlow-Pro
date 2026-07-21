# Test Execution Guide

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install
cp .env.example .env
```

Update `.env` with staging test credentials.

## Common Commands

```bash
pytest
pytest -m smoke
pytest tests/api -m api
pytest tests/ui -m ui --browser chromium
pytest tests/ui -m ui --browser firefox
pytest tests/ui -m ui --browser webkit
pytest tests/integration -m integration
pytest -n auto
```

## BrowserStack

```bash
export BROWSERSTACK_USERNAME=...
export BROWSERSTACK_ACCESS_KEY=...
pytest tests/mobile -m browserstack --mobile-capability android-chrome-pixel-7
pytest tests/mobile -m browserstack --mobile-capability ios-safari-iphone-14
```

## Reports

```bash
pytest --html=reports/html/report.html --self-contained-html
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
```

## CI

GitHub Actions runs linting, cross-browser smoke tests, and artifact upload. BrowserStack mobile runs on manual dispatch to control cost.
