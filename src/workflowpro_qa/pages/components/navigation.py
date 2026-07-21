from __future__ import annotations

from playwright.sync_api import Page, expect


class NavigationComponent:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_projects(self) -> None:
        projects_link = self.page.get_by_role("link", name="Projects")
        expect(projects_link).to_be_visible()
        projects_link.click()
