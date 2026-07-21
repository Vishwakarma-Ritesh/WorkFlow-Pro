# Bynry QA Automation Case Study Submission Notes

## Part 1: Debugging Flaky Login Tests

The original tests are flaky because they rely on immediate assertions, hardcoded URLs and credentials, no 2FA handling, duplicated browser setup, no tenant-aware configuration, and snapshot reads of dynamically loaded project cards.

The corrected implementation uses pytest fixtures, Playwright `expect` waits, Page Object Model classes, tenant configuration, secure credentials, loading-state handling, and failure artifacts.

Reference files:

- `tests/ui/test_login.py`
- `src/workflowpro_qa/pages/login_page.py`
- `src/workflowpro_qa/pages/dashboard_page.py`
- `docs/flaky-test-analysis.md`

## Part 2: Framework Design

The framework separates API, UI, config, fixtures, utilities, test data, reporting, BrowserStack, and CI. It supports Chrome, Firefox, WebKit, mobile BrowserStack sessions, multiple tenants, multiple roles, API testing, and integration tests.

Reference files:

- `docs/architecture.md`
- `docs/framework-explanation.md`
- `src/workflowpro_qa/config/settings.py`
- `pytest.ini`
- `.github/workflows/qa.yml`

## Part 3: API + UI Integration Flow

The integration test creates a project through API, validates API read consistency, verifies web UI visibility, checks mobile access through BrowserStack, and validates tenant isolation by logging into the other tenant and confirming the project is not visible.

Reference files:

- `tests/integration/test_project_creation_flow.py`
- `src/workflowpro_qa/api/clients/project_client.py`
- `src/workflowpro_qa/browserstack/playwright_remote.py`

## Missing Requirements To Clarify

- Exact selectors and accessible names for login, dashboard, and project pages.
- 2FA automation strategy and security approval.
- Stable test-user lifecycle and data ownership.
- API response contracts for error, pagination, and deletion behavior.
- Which roles can create, view, update, and delete projects.
- Expected tenant-isolation failure codes.
- BrowserStack parallel limits and required device matrix.
- Reporting retention policy and ownership of flaky-test triage.

## Final Positioning

This solution is intentionally framework-first rather than script-first. It is built to show production QA thinking: reliability, security, isolation, configurability, CI diagnostics, maintainability, and interview-ready tradeoff awareness.
