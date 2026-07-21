# WorkFlow Pro QA Automation

Enterprise-grade pytest + Playwright automation framework for the WorkFlow Pro B2B SaaS case study. It covers flaky-test remediation, multi-tenant framework design, API testing, UI validation, BrowserStack mobile execution, reporting, and CI/CD.

## What This Project Demonstrates

- Python, pytest, Playwright Page Object Model, fixtures, and reusable utilities.
- API automation with `requests`, retries, tenant headers, and cleanup.
- Multi-tenant and role-based configuration without hardcoded credentials.
- BrowserStack desktop and mobile execution through Playwright CDP.
- Allure, pytest-html, screenshots, traces, logs, and GitHub Actions.
- Case-study documentation and interview discussion notes.

## Repository Structure

```text
WorkFlow-Pro/
├── .github/workflows/          CI/CD pipelines
├── config/                     Runtime YAML config, environment files, BrowserStack YAML
├── docs/                       Architecture, strategy, execution, submission notes
├── reports/                    Generated reports, ignored except .gitkeep files
├── src/
│   └── workflowpro_qa/         Installable automation framework package
│       ├── api/                API clients, endpoints, models, test-data helpers
│       ├── browserstack/       Remote Playwright session and capability builders
│       ├── config/             Python settings loader
│       ├── fixtures/           pytest fixtures for browser, API, auth, config
│       ├── pages/              Page Object Model and reusable components
│       └── utils/              logging, retry, assertions, helpers, OTP handling
├── test_data/                  Version-safe data templates, not secrets
├── tests/                      API, UI, mobile, and integration suites
├── .env.example                Local environment variable template
├── conftest.py                 pytest plugin wiring
├── pyproject.toml              package metadata and quality tool config
├── pytest.ini                  pytest defaults, markers, pythonpath
└── requirements.txt            pinned/minimum runtime dependencies
```

## Assessment Assumptions

The assessment intentionally does not provide:

- live application URLs
- credentials or tenant secrets
- a BrowserStack account
- a running API server

Therefore this repository demonstrates:

- Framework design and architecture
- API layer structure and tenant-aware client design
- UI layer and Page Object Model approach
- Mobile and BrowserStack-ready execution patterns
- Multi-tenant design and cleanup strategy
- CI/CD, reporting, and flaky-test reasoning

This repo is focused on design and reasoning, using configurable placeholders and interview-focused assumptions rather than end-to-end execution against a real app.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m playwright install
cp .env.example .env
```

Populate `.env` with non-production test environment values, then run:

```bash
pytest -m smoke --browser chromium
pytest tests/api -m api
pytest tests/ui -m ui --browser firefox
pytest tests/integration -m integration
pytest tests/mobile -m browserstack
```

## Reports

```bash
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
```

The pytest HTML report is generated at `reports/html/report.html`.

## Security

No credentials, tokens, tenant URLs, or BrowserStack keys are committed. Use `.env` locally and GitHub Actions secrets in CI.

## Generated Caches

`.ruff_cache/`, `.pytest_cache/`, and `__pycache__/` are local speed-up folders created by tools. They are ignored by Git and can be deleted safely:

```bash
make clean
```
