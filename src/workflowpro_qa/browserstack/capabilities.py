from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
from typing import Any

from workflowpro_qa.config.settings import AppSettings, ConfigurationError


def _playwright_version() -> str:
    result = subprocess.run(
        ["python", "-m", "playwright", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    parts = result.stdout.strip().split()
    return parts[-1] if parts else "1.latest"


def _find_capability(settings: AppSettings, capability_name: str) -> dict[str, Any]:
    matrix = [
        *settings.browserstack.get("desktop_matrix", []),
        *settings.browserstack.get("mobile_matrix", []),
    ]
    for capability in matrix:
        if capability["name"] == capability_name:
            return dict(capability)
    raise ConfigurationError(f"Unknown BrowserStack capability: {capability_name}")


def build_browserstack_caps(
    settings: AppSettings,
    capability_name: str,
    session_name: str,
) -> dict[str, Any]:
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if not username or not access_key:
        raise ConfigurationError("BrowserStack credentials are required for remote execution.")

    caps = _find_capability(settings, capability_name)
    caps.update(
        {
            "browserstack.username": username,
            "browserstack.accessKey": access_key,
            "project": os.getenv("BROWSERSTACK_PROJECT_NAME", "WorkFlow Pro QA Automation"),
            "build": os.getenv("BROWSERSTACK_BUILD_NAME", "workflowpro-local"),
            "name": session_name,
            "browserstack.local": os.getenv("BROWSERSTACK_LOCAL", "false"),
            "browserstack.playwrightVersion": settings.browserstack["playwright_version"],
            "client.playwrightVersion": _playwright_version(),
            "browserstack.debug": str(settings.browserstack["debug"]).lower(),
            "browserstack.console": settings.browserstack["console"],
            "browserstack.networkLogs": str(settings.browserstack["network_logs"]).lower(),
            "browserstack.interactiveDebugging": str(
                settings.browserstack["interactive_debugging"]
            ).lower(),
            "browserstack.maskCommands": "setValues, getValues, setCookies",
        }
    )
    local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")
    if local_identifier:
        caps["browserstack.localIdentifier"] = local_identifier
    return caps


def build_cdp_url(settings: AppSettings, capability_name: str, session_name: str) -> str:
    caps = build_browserstack_caps(settings, capability_name, session_name)
    endpoint = settings.browserstack["cdp_endpoint"]
    return f"{endpoint}?caps={urllib.parse.quote(json.dumps(caps))}"
