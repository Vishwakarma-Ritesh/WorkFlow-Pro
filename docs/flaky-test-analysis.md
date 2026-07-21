# Part 1: Flaky Test Analysis

## Problems In The Intern Test

- Browser lifecycle is manually duplicated in every test.
- No isolated context configuration for viewport, locale, storage, or tracing.
- Tests use hardcoded production URLs and credentials.
- Immediate `assert page.url == ...` races against redirects and async login completion.
- `.is_visible()` returns current state instead of waiting for the UI to stabilize.
- `.locator(...).all()` captures a snapshot before dynamic project cards finish loading.
- No handling for optional 2FA.
- No tenant-aware configuration.
- No cleanup, screenshots, traces, or useful failure artifacts.
- No cross-browser awareness even though CI runs different browsers and screen sizes.

## Why CI Fails More Than Local

- CI machines are slower and more variable than local machines.
- Headless browser rendering can expose timing and viewport differences.
- Network latency makes dashboard and tenant data load at different speeds.
- Parallel execution can create data collisions when names are static.
- CI often has stricter third-party, cookie, and redirect behavior.

## Production Fix Strategy

- Use pytest fixtures for browser lifecycle.
- Use config and environment variables for URLs, credentials, tenants, roles, and timeouts.
- Use Page Objects for login and dashboard behavior.
- Use Playwright `expect` assertions that wait for conditions.
- Wait for stable page states and loading indicators.
- Support 2FA through test-safe OTP or bypass configuration.
- Capture traces, screenshots, logs, Allure results, and HTML reports.

## Corrected Compact Example

```python
def test_user_login(app_page, settings, tenant_id, user_credentials):
    tenant = settings.tenant(tenant_id)
    LoginPage(app_page, settings).open(tenant).login(user_credentials)
    LoginPage(app_page, settings).expect_login_complete()
    DashboardPage(app_page, settings).expect_loaded()
```

The full implementation is in `tests/ui/test_login.py`.
