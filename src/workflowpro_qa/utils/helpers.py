from __future__ import annotations

import re
from datetime import UTC, datetime
from uuid import uuid4


def unique_name(prefix: str) -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}-{uuid4().hex[:8]}"


def normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def redact(value: str | None, *, visible_suffix: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= visible_suffix:
        return "*" * len(value)
    return f"{'*' * (len(value) - visible_suffix)}{value[-visible_suffix:]}"
