from __future__ import annotations

from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry_until(
    operation: Callable[[], T],
    predicate: Callable[[T], bool],
    *,
    attempts: int,
    delay_seconds: float,
    failure_message: str,
) -> T:
    last_result: T | None = None
    for attempt in range(1, attempts + 1):
        last_result = operation()
        if predicate(last_result):
            return last_result
        if attempt < attempts:
            sleep(delay_seconds)
    raise AssertionError(failure_message)
