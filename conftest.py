from __future__ import annotations

import pytest

from workflowpro_qa.fixtures.api import created_projects, project_client
from workflowpro_qa.fixtures.auth import api_token, role, tenant_id, user_credentials
from workflowpro_qa.fixtures.browser import app_context, app_page, browserstack_session_factory
from workflowpro_qa.fixtures.config import settings

__all__ = [
    "api_token",
    "app_context",
    "app_page",
    "browserstack_session_factory",
    "created_projects",
    "project_client",
    "role",
    "settings",
    "tenant_id",
    "user_credentials",
]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default=None, help="Environment config name.")
    parser.addoption(
        "--tenant",
        action="store",
        default=None,
        help="Tenant id, for example company1.",
    )
    parser.addoption("--role", action="store", default=None, help="User role, for example admin.")
    parser.addoption(
        "--browserstack-capability",
        action="store",
        default="chrome-windows",
        help="BrowserStack capability name from config/browserstack matrix.",
    )
    parser.addoption(
        "--mobile-capability",
        action="store",
        default="android-chrome-pixel-7",
        help="BrowserStack mobile capability name from config/browserstack matrix.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
