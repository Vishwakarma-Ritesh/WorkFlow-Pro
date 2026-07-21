# CI/CD Explanation

## Pipeline Stages

1. Checkout source.
2. Install Python dependencies.
3. Run Ruff, Black, and isort quality gates.
4. Install Playwright browsers.
5. Run smoke tests across Chromium, Firefox, and WebKit.
6. Upload HTML and Allure artifacts.
7. Run BrowserStack mobile smoke manually or on scheduled release gates.

## Why This Design

- Quality fails fast before expensive browser execution.
- Browser matrix catches browser-specific regressions.
- `pytest-xdist` reduces execution time for independent tests.
- Secrets remain in GitHub Actions secrets, never in files.
- BrowserStack is separated to control cost and reduce PR wait time.

## Required GitHub Secrets

- `WORKFLOWPRO_API_BASE_URL`
- `WORKFLOWPRO_COMPANY1_BASE_URL`
- `WORKFLOWPRO_COMPANY2_BASE_URL`
- `WORKFLOWPRO_COMPANY1_ADMIN_EMAIL`
- `WORKFLOWPRO_COMPANY1_ADMIN_PASSWORD`
- `WORKFLOWPRO_COMPANY2_ADMIN_EMAIL`
- `WORKFLOWPRO_COMPANY2_ADMIN_PASSWORD`
- `BROWSERSTACK_USERNAME`
- `BROWSERSTACK_ACCESS_KEY`
