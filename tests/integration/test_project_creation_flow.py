from __future__ import annotations

import allure
import pytest

from workflowpro_qa.api.helpers.test_data_factory import TestDataFactory
from workflowpro_qa.config.settings import AppSettings
from workflowpro_qa.pages.login_page import LoginPage
from workflowpro_qa.pages.projects_page import ProjectsPage
from workflowpro_qa.utils.retry import retry_until

pytestmark = [pytest.mark.integration, pytest.mark.external]


@allure.feature("API + UI project creation")
@allure.story("Project is created by API and visible only inside the owning tenant")
@pytest.mark.smoke
@pytest.mark.tenant_isolation
def test_project_creation_flow(
    app_page,
    settings: AppSettings,
    tenant_id: str,
    project_client,
    created_projects: list[tuple[str, int | str]],
    browserstack_session_factory,
    pytestconfig: pytest.Config,
) -> None:
    tenant = settings.tenant(tenant_id)
    payload = TestDataFactory.project_payload(tenant_id)

    project = project_client.create_project(tenant_id, payload)
    created_projects.append((tenant_id, project.id))

    fetched = retry_until(
        lambda: project_client.get_project(tenant_id, project.id),
        lambda item: item.name == payload.name and item.status == "active",
        attempts=5,
        delay_seconds=2,
        failure_message="Created project did not become readable through API.",
    )
    assert fetched.id == project.id

    credentials = settings.credentials(tenant_id, "admin")
    LoginPage(app_page, settings).open(tenant).login(credentials)
    LoginPage(app_page, settings).expect_login_complete()
    web_projects = ProjectsPage(app_page, settings).open(tenant.base_url)
    web_projects.search(payload.name)
    web_projects.expect_project_visible(payload.name)

    mobile_capability = pytestconfig.getoption("--mobile-capability")
    try:
        mobile_session = browserstack_session_factory(
            mobile_capability,
            f"Mobile visibility - {payload.name}",
        )
    except Exception as exc:
        pytest.skip(f"BrowserStack mobile session unavailable: {exc}")

    mobile_page = mobile_session.page
    LoginPage(mobile_page, settings).open(tenant).login(credentials)
    ProjectsPage(mobile_page, settings).open(tenant.base_url).search(payload.name)
    ProjectsPage(mobile_page, settings).expect_project_visible(payload.name)

    other_tenant_id = "company2" if tenant_id == "company1" else "company1"
    other_tenant = settings.tenant(other_tenant_id)
    other_credentials = settings.credentials(other_tenant_id, "admin")
    app_page.context.clear_cookies()
    LoginPage(app_page, settings).open(other_tenant).login(other_credentials)
    ProjectsPage(app_page, settings).open(other_tenant.base_url).search(payload.name)
    ProjectsPage(app_page, settings).expect_project_not_visible(payload.name)

    for created_tenant, project_id in created_projects:
        project_client.delete_project(created_tenant, project_id)
