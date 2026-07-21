from __future__ import annotations

import json
from dataclasses import dataclass

from playwright.sync_api import Browser, Page, Playwright

from workflowpro_qa.config.settings import AppSettings
from workflowpro_qa.utils.logger import get_logger

from .capabilities import build_cdp_url

LOGGER = get_logger(__name__)


@dataclass
class BrowserStackSession:
    browser: Browser
    page: Page

    @classmethod
    def create(
        cls,
        *,
        playwright: Playwright,
        settings: AppSettings,
        capability_name: str,
        session_name: str,
    ) -> BrowserStackSession:
        cdp_url = build_cdp_url(settings, capability_name, session_name)
        browser = playwright.chromium.connect(cdp_url)
        page = browser.new_page()
        return cls(browser=browser, page=page)

    def mark_status(self, status: str, reason: str) -> None:
        payload = {
            "action": "setSessionStatus",
            "arguments": {"status": status, "reason": reason[:250]},
        }
        try:
            self.page.evaluate("_ => {}", f"browserstack_executor: {json.dumps(payload)}")
        except Exception as exc:
            LOGGER.warning("Unable to mark BrowserStack session status: %s", exc)

    def close(self) -> None:
        try:
            self.page.close()
        finally:
            self.browser.close()
