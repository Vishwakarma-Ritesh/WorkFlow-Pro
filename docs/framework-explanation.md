# Framework Explanation

## Pytest

Pytest provides fixtures, marks, hooks, and parallel execution through `pytest-xdist`. This framework uses fixtures for settings, browser contexts, API clients, authentication, and test data cleanup.

## Playwright

Playwright provides auto-waiting locators, reliable browser automation, traces, screenshots, and cross-browser support. The project uses Playwright through pytest fixtures and Page Object Model classes.

## Page Object Model

Page objects keep selectors and page-specific behavior out of tests. Tests read as business workflows, while pages handle synchronization and UI actions.

## API Layer

The API layer uses `requests.Session` with retry-aware adapters for transient network and service failures. Every request can include `X-Tenant-ID`, making tenant scope visible and testable.

## Configuration

`src/workflowpro_qa/config/settings.py` loads base YAML, environment YAML, and environment variables. Secrets are never stored in code.

## Repository Structure

Framework code lives under `src/workflowpro_qa` so it can be installed and versioned like a normal client project. Test files stay under `tests` and consume framework capabilities through package imports.

## Reporting

Pytest HTML gives a simple single-file report. Allure gives richer history, steps, attachments, and trend reporting. Playwright traces and screenshots help debug UI failures.
