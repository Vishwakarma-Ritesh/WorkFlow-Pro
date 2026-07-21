from __future__ import annotations

import os


class OtpProvider:
    """Provides OTP values only from secure test environment channels."""

    def current_code(self) -> str | None:
        return os.getenv("WORKFLOWPRO_TEST_OTP")


class MissingOtpError(RuntimeError):
    """Raised when a login challenge appears but no OTP source is configured."""
