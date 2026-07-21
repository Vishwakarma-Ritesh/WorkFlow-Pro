from __future__ import annotations

import pytest

from workflowpro_qa.config.settings import AppSettings, load_settings


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> AppSettings:
    return load_settings(pytestconfig.getoption("--env"))
