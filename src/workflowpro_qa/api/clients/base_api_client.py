from __future__ import annotations

from typing import Any

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from workflowpro_qa.config.settings import AppSettings
from workflowpro_qa.utils.logger import get_logger

LOGGER = get_logger(__name__)


class ApiError(RuntimeError):
    def __init__(self, message: str, response: Response | None = None) -> None:
        super().__init__(message)
        self.response = response


class BaseApiClient:
    def __init__(self, settings: AppSettings, token: str | None = None) -> None:
        self.settings = settings
        self.base_url = settings.api_base_url.rstrip("/")
        self.session = self._build_session(token)

    def _build_session(self, token: str | None) -> Session:
        session = requests.Session()
        retry = Retry(
            total=int(self.settings.api["retry_total"]),
            backoff_factor=float(self.settings.api["retry_backoff_factor"]),
            status_forcelist=self.settings.api["retry_statuses"],
            allowed_methods={"GET", "POST", "PUT", "PATCH", "DELETE"},
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"Content-Type": "application/json"})
        if token:
            session.headers.update({"Authorization": f"Bearer {token}"})
        return session

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        tenant_id: str | None = None,
        expected_status: int | tuple[int, ...],
        **kwargs: Any,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {}) or {}
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id

        LOGGER.info("API %s %s tenant=%s", method.upper(), endpoint, tenant_id or "none")
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            timeout=self.settings.timeouts.api_seconds,
            **kwargs,
        )

        allowed = (expected_status,) if isinstance(expected_status, int) else expected_status
        if response.status_code not in allowed:
            raise ApiError(
                f"Expected {allowed} from {method.upper()} {endpoint}, got "
                f"{response.status_code}: {response.text[:500]}",
                response=response,
            )
        return response

    def get_json(
        self,
        method: str,
        endpoint: str,
        *,
        tenant_id: str | None = None,
        expected_status: int | tuple[int, ...],
        **kwargs: Any,
    ) -> dict[str, Any] | list[Any]:
        response = self.request(
            method,
            endpoint,
            tenant_id=tenant_id,
            expected_status=expected_status,
            **kwargs,
        )
        if not response.content:
            return {}
        return response.json()
