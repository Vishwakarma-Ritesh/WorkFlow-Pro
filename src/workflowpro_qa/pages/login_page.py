from __future__ import annotations

import os

from playwright.sync_api import expect

from workflowpro_qa.config.settings import TenantSettings, UserCredentials
from workflowpro_qa.utils.otp import MissingOtpError, OtpProvider

from .base_page import BasePage


class LoginPage(BasePage):
    def open(self, tenant: TenantSettings) -> LoginPage:
        self.goto(f"{tenant.base_url.rstrip('/')}/login")
        return self

    def login(self, credentials: UserCredentials, otp_provider: OtpProvider | None = None) -> None:
        self.fill("login_email", credentials.email)
        if not credentials.password:
            raise ValueError("Password is required for UI login.")
        self.fill("login_password", credentials.password)
        self.click("login_button")
        self._complete_2fa_if_present(otp_provider or OtpProvider())

    def expect_login_complete(self) -> None:
        self.wait_for_url_contains("/dashboard")
        expect(self.locator("dashboard_root")).to_be_visible(
            timeout=self.settings.timeouts.assertion_ms,
        )

    def _complete_2fa_if_present(self, otp_provider: OtpProvider) -> None:
        bypass_token = os.getenv("WORKFLOWPRO_2FA_BYPASS_TOKEN")
        if bypass_token:
            self.page.evaluate(
                "token => window.localStorage.setItem('test_2fa_bypass', token)",
                bypass_token,
            )

        otp_input = self.locator("otp_input").first
        try:
            otp_input.wait_for(state="visible", timeout=3000)
        except Exception:
            return

        otp = otp_provider.current_code()
        if not otp:
            raise MissingOtpError("2FA challenge appeared but WORKFLOWPRO_TEST_OTP is not set.")
        otp_input.fill(otp)
        self.click("otp_submit")
