from __future__ import annotations

import re
from pathlib import Path

import allure
from playwright.sync_api import Locator, Page, expect

from workflowpro_qa.config.settings import AppSettings
from workflowpro_qa.utils.logger import get_logger

LOGGER = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page, settings: AppSettings) -> None:
        self.page = page
        self.settings = settings
        self.selectors = settings.selectors

    def goto(self, url: str) -> None:
        LOGGER.info("Navigating to %s", url)
        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=self.settings.timeouts.navigation_ms,
        )
        self.wait_for_loading_to_finish()

    def locator(self, selector_key: str) -> Locator:
        return self.page.locator(self.selectors[selector_key])

    def fill(self, selector_key: str, value: str) -> None:
        field = self.locator(selector_key)
        expect(field).to_be_visible(timeout=self.settings.timeouts.assertion_ms)
        field.fill(value, timeout=self.settings.timeouts.action_ms)

    def click(self, selector_key: str) -> None:
        target = self.locator(selector_key)
        expect(target).to_be_enabled(timeout=self.settings.timeouts.assertion_ms)
        target.click(timeout=self.settings.timeouts.action_ms)

    def wait_for_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(
            re.compile(f".*{re.escape(fragment)}.*"),
            timeout=self.settings.timeouts.navigation_ms,
        )

    def wait_for_loading_to_finish(self) -> None:
        loader = self.locator("loading_indicator")
        try:
            loader.first.wait_for(state="hidden", timeout=self.settings.timeouts.assertion_ms)
        except Exception:
            LOGGER.debug("No blocking loading indicator was visible.")

    def attach_screenshot(self, name: str) -> None:
        path = Path(self.settings.reports["screenshots_dir"])
        path.mkdir(parents=True, exist_ok=True)
        screenshot_path = path / f"{name}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        allure.attach.file(
            str(screenshot_path),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
