from __future__ import annotations

import pytest

from workflowpro_qa.api.clients.auth_client import AuthClient
from workflowpro_qa.config.settings import AppSettings, UserCredentials


@pytest.fixture
def tenant_id(pytestconfig: pytest.Config, settings: AppSettings) -> str:
    return pytestconfig.getoption("--tenant") or settings.default_tenant


@pytest.fixture
def role(pytestconfig: pytest.Config, settings: AppSettings) -> str:
    return pytestconfig.getoption("--role") or settings.default_role


@pytest.fixture
def user_credentials(settings: AppSettings, tenant_id: str, role: str) -> UserCredentials:
    return settings.credentials(tenant_id, role)


@pytest.fixture
def api_token(settings: AppSettings, tenant_id: str, role: str) -> str:
    credentials = settings.credentials(tenant_id, role, require_password=False)
    return AuthClient(settings).login(credentials)
