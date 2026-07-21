from __future__ import annotations

from workflowpro_qa.config.settings import UserCredentials

from .base_api_client import BaseApiClient


class AuthClient(BaseApiClient):
    def login(self, credentials: UserCredentials) -> str:
        if credentials.token:
            return credentials.token
        if not credentials.password:
            raise ValueError("Password is required when token is not provided.")

        data = self.get_json(
            "POST",
            self.settings.api["auth_endpoint"],
            tenant_id=credentials.tenant_id,
            expected_status=200,
            json={
                "email": credentials.email,
                "password": credentials.password,
            },
        )
        token = data.get("token") if isinstance(data, dict) else None
        if not token:
            raise ValueError("Authentication response did not include token.")
        return token
