from __future__ import annotations

import allure
import pytest

from workflowpro_qa.api.helpers.test_data_factory import TestDataFactory
from workflowpro_qa.api.models.project import Project
from workflowpro_qa.config.settings import AppSettings

pytestmark = [pytest.mark.api, pytest.mark.external]


@allure.feature("Projects API")
@pytest.mark.smoke
def test_create_and_read_project(
    settings: AppSettings,
    tenant_id: str,
    project_client,
    created_projects: list[tuple[str, int | str]],
) -> None:
    payload = TestDataFactory.project_payload(tenant_id)

    project = project_client.create_project(tenant_id, payload)
    created_projects.append((tenant_id, project.id))

    assert isinstance(project, Project)
    assert project.name == payload.name
    assert project.status == "active"

    fetched = project_client.get_project(tenant_id, project.id)
    assert fetched.id == project.id
    assert fetched.name == payload.name

    for created_tenant, project_id in created_projects:
        project_client.delete_project(created_tenant, project_id)
