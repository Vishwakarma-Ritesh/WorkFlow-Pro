from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT_DIR / "config"


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigurationError(f"Configuration file not found: {path}")
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ConfigurationError(f"Configuration file must contain a mapping: {path}")
    return data


def _env_value(name: str | None, *, required: bool = False) -> str | None:
    if not name:
        return None
    value = os.getenv(name)
    if required and not value:
        raise ConfigurationError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class TimeoutSettings:
    navigation_ms: int
    action_ms: int
    assertion_ms: int
    api_seconds: int


@dataclass(frozen=True)
class UserCredentials:
    tenant_id: str
    tenant_name: str
    role: str
    email: str
    password: str | None
    token: str | None = None


@dataclass(frozen=True)
class TenantSettings:
    id: str
    name: str
    base_url: str
    roles: dict[str, dict[str, str]]


@dataclass(frozen=True)
class AppSettings:
    environment: str
    app_name: str
    api_base_url: str
    default_tenant: str
    default_role: str
    tenants: dict[str, TenantSettings]
    timeouts: TimeoutSettings
    browser: dict[str, Any]
    reports: dict[str, str]
    selectors: dict[str, str]
    api: dict[str, Any]
    browserstack: dict[str, Any]

    def tenant(self, tenant_id: str | None = None) -> TenantSettings:
        selected = tenant_id or self.default_tenant
        try:
            return self.tenants[selected]
        except KeyError as exc:
            raise ConfigurationError(f"Unknown tenant '{selected}'") from exc

    def credentials(
        self,
        tenant_id: str | None = None,
        role: str | None = None,
        *,
        require_password: bool = True,
    ) -> UserCredentials:
        tenant = self.tenant(tenant_id)
        selected_role = role or self.default_role
        role_config = tenant.roles.get(selected_role)
        if not role_config:
            raise ConfigurationError(f"Unknown role '{selected_role}' for tenant '{tenant.id}'")

        token = _env_value(role_config.get("token_env"))
        email = _env_value(role_config.get("email_env"), required=require_password or not token)
        password = _env_value(
            role_config.get("password_env"),
            required=require_password or not token,
        )
        return UserCredentials(
            tenant_id=tenant.id,
            tenant_name=tenant.name,
            role=selected_role,
            email=email or "",
            password=password,
            token=token,
        )


@lru_cache(maxsize=8)
def load_settings(environment: str | None = None) -> AppSettings:
    load_dotenv(ROOT_DIR / ".env")

    base_config = _read_yaml(CONFIG_DIR / "config.yaml")
    selected_environment = (
        environment or os.getenv("TEST_ENV") or base_config["application"]["default_environment"]
    )
    env_config = _read_yaml(CONFIG_DIR / "environments" / f"{selected_environment}.yaml")

    tenants: dict[str, TenantSettings] = {}
    for tenant_id, tenant_config in env_config.get("tenants", {}).items():
        base_url = _env_value(tenant_config.get("base_url_env"), required=True)
        tenants[tenant_id] = TenantSettings(
            id=tenant_config["id"],
            name=tenant_config["name"],
            base_url=base_url or "",
            roles=tenant_config.get("roles", {}),
        )

    api_base_url = _env_value(env_config.get("api_base_url_env"), required=True)
    timeouts = TimeoutSettings(**base_config["timeouts"])

    return AppSettings(
        environment=selected_environment,
        app_name=base_config["application"]["name"],
        api_base_url=api_base_url or "",
        default_tenant=os.getenv("DEFAULT_TENANT", base_config["application"]["default_tenant"]),
        default_role=os.getenv("DEFAULT_ROLE", base_config["application"]["default_role"]),
        tenants=tenants,
        timeouts=timeouts,
        browser=base_config["browser"],
        reports=base_config["reports"],
        selectors=base_config["selectors"],
        api=base_config["api"],
        browserstack=base_config["browserstack"],
    )
