from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from workflowpro_qa.config.settings import AppSettings, UserCredentials
from workflowpro_qa.pages.dashboard_page import DashboardPage
from workflowpro_qa.pages.login_page import LoginPage

pytestmark = [pytest.mark.integration, pytest.mark.external]


@allure.feature("Authentication")
@allure.story("Reliable login flow with dynamic dashboard loading")
@pytest.mark.smoke
def test_user_login_flow(
    app_page,
    settings: AppSettings,
    tenant_id: str,
    user_credentials: UserCredentials,
) -> None:
    tenant = settings.tenant(tenant_id)

    LoginPage(app_page, settings).open(tenant).login(user_credentials)
    LoginPage(app_page, settings).expect_login_complete()

    dashboard = DashboardPage(app_page, settings)
    dashboard.expect_loaded()
    expect(app_page.locator(".welcome-message")).to_be_visible(
        timeout=settings.timeouts.assertion_ms,
    )


@allure.feature("Multi-tenant access")
@allure.story("Tenant data isolation in dashboard")
@pytest.mark.tenant_isolation
def test_multi_tenant_access_flow(
    app_page,
    settings: AppSettings,
) -> None:
    tenant = settings.tenant("company2")
    credentials = settings.credentials("company2", "admin")

    LoginPage(app_page, settings).open(tenant).login(credentials)
    LoginPage(app_page, settings).expect_login_complete()

    dashboard = DashboardPage(app_page, settings)
    dashboard.expect_loaded()
    dashboard.expect_only_tenant_projects(tenant.name)
