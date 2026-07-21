from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    tenant_name: str
    base_url: str
    api_base_url: str
