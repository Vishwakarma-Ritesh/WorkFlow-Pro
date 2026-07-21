from __future__ import annotations

from collections.abc import Generator

import pytest

from workflowpro_qa.api.clients.project_client import ProjectClient
from workflowpro_qa.config.settings import AppSettings


@pytest.fixture
def project_client(settings: AppSettings, api_token: str) -> ProjectClient:
    return ProjectClient(settings, token=api_token)


@pytest.fixture
def created_projects(
    project_client: ProjectClient,
) -> Generator[list[tuple[str, int | str]], None, None]:
    projects: list[tuple[str, int | str]] = []
    try:
        yield projects
    finally:
        for tenant_id, project_id in projects:
            project_client.delete_project(tenant_id, project_id)
