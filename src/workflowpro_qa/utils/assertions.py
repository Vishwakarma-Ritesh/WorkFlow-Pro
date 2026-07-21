from __future__ import annotations

import re

from playwright.sync_api import Locator, Page, expect


def expect_visible(locator: Locator, timeout: int) -> None:
    expect(locator).to_be_visible(timeout=timeout)


def expect_text_contains(locator: Locator, expected: str, timeout: int) -> None:
    expect(locator).to_contain_text(expected, timeout=timeout)


def expect_url_contains(page: Page, fragment: str, timeout: int) -> None:
    expect(page).to_have_url(re.compile(f".*{re.escape(fragment)}.*"), timeout=timeout)
