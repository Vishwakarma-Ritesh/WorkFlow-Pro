from __future__ import annotations

import allure
import pytest

from workflowpro_qa.config.settings import AppSettings, UserCredentials
from workflowpro_qa.pages.dashboard_page import DashboardPage
from workflowpro_qa.pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.external]


@allure.feature("Authentication")
@allure.story("Login flow using Page Object Model")
def test_login_reference_fix(
    app_page,
    settings: AppSettings,
    tenant_id: str,
    user_credentials: UserCredentials,
) -> None:
    """Use the LoginPage page object instead of raw Playwright locators."""
    tenant = settings.tenant(tenant_id)

    LoginPage(app_page, settings).open(tenant).login(user_credentials)
    LoginPage(app_page, settings).expect_login_complete()

    DashboardPage(app_page, settings).expect_loaded()
