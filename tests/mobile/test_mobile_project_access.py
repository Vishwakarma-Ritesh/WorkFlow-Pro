from __future__ import annotations

import allure
import pytest

from workflowpro_qa.config.settings import AppSettings
from workflowpro_qa.pages.login_page import LoginPage
from workflowpro_qa.pages.projects_page import ProjectsPage

pytestmark = [pytest.mark.mobile, pytest.mark.browserstack, pytest.mark.external]


@allure.feature("Mobile web")
def test_projects_page_loads_on_mobile(
    settings: AppSettings,
    tenant_id: str,
    browserstack_session_factory,
    pytestconfig: pytest.Config,
) -> None:
    tenant = settings.tenant(tenant_id)
    credentials = settings.credentials(tenant_id, "admin")
    session = browserstack_session_factory(
        pytestconfig.getoption("--mobile-capability"),
        f"Mobile projects page - {tenant_id}",
    )

    LoginPage(session.page, settings).open(tenant).login(credentials)
    ProjectsPage(session.page, settings).open(tenant.base_url)
