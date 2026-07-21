from __future__ import annotations

# pytest-playwright is configured through pytest.ini and CLI options.
# This file documents the cross-browser matrix expected in CI and interviews.

PROJECTS = [
    {"name": "chromium", "browser": "chromium"},
    {"name": "firefox", "browser": "firefox"},
    {"name": "webkit", "browser": "webkit"},
]

MOBILE_PROJECTS = [
    {"name": "mobile-chrome-pixel", "device": "Pixel 7"},
    {"name": "mobile-safari-iphone", "device": "iPhone 14"},
]
