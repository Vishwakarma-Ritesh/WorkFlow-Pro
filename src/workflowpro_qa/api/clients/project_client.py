from __future__ import annotations

from typing import Any

from workflowpro_qa.api.endpoints.projects import PROJECTS, project_by_id
from workflowpro_qa.api.models.project import Project, ProjectPayload
from workflowpro_qa.config.settings import AppSettings

from .base_api_client import BaseApiClient


class ProjectClient(BaseApiClient):
    def __init__(self, settings: AppSettings, token: str) -> None:
        super().__init__(settings, token=token)

    def create_project(self, tenant_id: str, payload: ProjectPayload) -> Project:
        data = self.get_json(
            "POST",
            PROJECTS,
            tenant_id=tenant_id,
            expected_status=201,
            json=payload.as_dict(),
        )
        if not isinstance(data, dict):
            raise ValueError("Project creation response must be an object.")
        return Project.from_api(data)

    def get_project(self, tenant_id: str, project_id: int | str) -> Project:
        data = self.get_json(
            "GET",
            project_by_id(project_id),
            tenant_id=tenant_id,
            expected_status=200,
        )
        if not isinstance(data, dict):
            raise ValueError("Project detail response must be an object.")
        return Project.from_api(data)

    def list_projects(self, tenant_id: str) -> list[dict[str, Any]]:
        data = self.get_json("GET", PROJECTS, tenant_id=tenant_id, expected_status=200)
        if isinstance(data, dict):
            return list(data.get("items", []))
        return list(data)

    def delete_project(self, tenant_id: str, project_id: int | str) -> None:
        self.request(
            "DELETE",
            project_by_id(project_id),
            tenant_id=tenant_id,
            expected_status=(200, 202, 204, 404),
        )
