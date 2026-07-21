# BrowserStack Strategy

## Purpose

BrowserStack validates real-device and cross-platform behavior without maintaining local device labs.

## Execution Model

- Local desktop browsers run through pytest-playwright for fast feedback.
- BrowserStack desktop and mobile sessions run through Playwright CDP.
- Mobile runs are separated and usually manual or scheduled to control cost.
- Sessions are named with test context and marked pass/fail through `browserstack_executor`.

## Cost Optimization

- Run full BrowserStack mobile smoke on release branches and manual dispatch.
- Run a small mobile smoke set on pull requests only for high-risk UI changes.
- Keep parallel count aligned with BrowserStack plan capacity.
- Prefer API setup over UI setup to reduce remote session duration.

## Required Secrets

- `BROWSERSTACK_USERNAME`
- `BROWSERSTACK_ACCESS_KEY`
- `BROWSERSTACK_BUILD_NAME`
- Optional `BROWSERSTACK_LOCAL_IDENTIFIER`
