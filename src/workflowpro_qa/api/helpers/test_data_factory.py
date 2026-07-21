from __future__ import annotations

from workflowpro_qa.api.models.project import ProjectPayload
from workflowpro_qa.utils.helpers import unique_name


class TestDataFactory:
    @staticmethod
    def project_payload(tenant_id: str) -> ProjectPayload:
        return ProjectPayload(
            name=unique_name(f"{tenant_id}-project"),
            description=f"Automated project created for tenant {tenant_id}",
            team_members=[],
        )
