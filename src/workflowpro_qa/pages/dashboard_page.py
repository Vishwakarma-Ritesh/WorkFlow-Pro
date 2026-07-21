from __future__ import annotations

from playwright.sync_api import expect

from workflowpro_qa.utils.helpers import normalize_text

from .base_page import BasePage


class DashboardPage(BasePage):
    def expect_loaded(self) -> None:
        expect(self.locator("dashboard_root")).to_be_visible(
            timeout=self.settings.timeouts.assertion_ms,
        )
        expect(self.locator("welcome_message")).to_be_visible(
            timeout=self.settings.timeouts.assertion_ms,
        )
        self.wait_for_loading_to_finish()

    def project_cards_text(self) -> list[str]:
        cards = self.locator("project_card")
        expect(cards.first).to_be_visible(timeout=self.settings.timeouts.assertion_ms)
        return [normalize_text(cards.nth(index).text_content()) for index in range(cards.count())]

    def expect_only_tenant_projects(self, tenant_name: str) -> None:
        for text in self.project_cards_text():
            assert (
                tenant_name in text
            ), f"Project card does not belong to tenant {tenant_name}: {text}"
