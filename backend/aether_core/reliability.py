from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    retryable_exceptions: tuple[type[BaseException], ...] = (Exception,)

    def can_retry(self, attempt: int) -> bool:
        return attempt < self.max_attempts


def run_with_retry(operation: Callable[[], T], policy: RetryPolicy = RetryPolicy()) -> T:
    last_error: BaseException | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return operation()
        except policy.retryable_exceptions as exc:
            last_error = exc
            if not policy.can_retry(attempt):
                raise
    raise RuntimeError("Retry policy terminated without a result") from last_error
