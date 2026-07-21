from __future__ import annotations

from playwright.sync_api import Locator, expect

from .base_page import BasePage


class ProjectsPage(BasePage):
    def open(self, base_url: str) -> ProjectsPage:
        self.goto(f"{base_url.rstrip('/')}/projects")
        return self

    def search(self, project_name: str) -> None:
        search = self.locator("project_search")
        expect(search).to_be_visible(timeout=self.settings.timeouts.assertion_ms)
        search.fill(project_name)
        self.wait_for_loading_to_finish()

    def project_card(self, project_name: str) -> Locator:
        return self.locator("project_card").filter(has_text=project_name).first

    def expect_project_visible(self, project_name: str) -> None:
        card = self.project_card(project_name)
        expect(card).to_be_visible(timeout=self.settings.timeouts.assertion_ms)

    def expect_project_not_visible(self, project_name: str) -> None:
        card = self.project_card(project_name)
        expect(card).not_to_be_visible(timeout=self.settings.timeouts.assertion_ms)
