from __future__ import annotations

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from workflowpro_qa.browserstack.playwright_remote import BrowserStackSession
from workflowpro_qa.config.settings import AppSettings


@pytest.fixture
def app_context(browser: Browser, settings: AppSettings) -> BrowserContext:
    context = browser.new_context(
        viewport=settings.browser["viewport"],
        locale=settings.browser["locale"],
        timezone_id=settings.browser["timezone_id"],
        ignore_https_errors=True,
    )
    context.set_default_timeout(settings.timeouts.action_ms)
    context.set_default_navigation_timeout(settings.timeouts.navigation_ms)
    yield context
    context.close()


@pytest.fixture
def app_page(app_context: BrowserContext) -> Page:
    page = app_context.new_page()
    yield page
    page.close()


@pytest.fixture
def browserstack_session_factory(
    playwright: Playwright,
    settings: AppSettings,
    request: pytest.FixtureRequest,
):
    sessions: list[BrowserStackSession] = []

    def create(capability_name: str, session_name: str) -> BrowserStackSession:
        session = BrowserStackSession.create(
            playwright=playwright,
            settings=settings,
            capability_name=capability_name,
            session_name=session_name,
        )
        sessions.append(session)
        return session

    yield create

    failed = getattr(request.node, "rep_call", None)
    passed = failed is None or failed.passed
    for session in sessions:
        session.mark_status(
            "passed" if passed else "failed",
            "pytest completed" if passed else str(failed.longrepr),
        )
        session.close()
