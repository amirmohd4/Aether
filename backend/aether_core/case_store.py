from __future__ import annotations

from threading import RLock
from typing import Dict

from .domain import Case


class InMemoryCaseStore:
    """MVP store. Replace with PostgreSQL repository without changing the API layer."""

    def __init__(self):
        self._cases: Dict[str, Case] = {}
        self._lock = RLock()

    def put(self, case: Case) -> Case:
        with self._lock:
            self._cases[case.case_id] = case
        return case

    def get(self, case_id: str) -> Case:
        with self._lock:
            if case_id not in self._cases:
                raise KeyError(case_id)
            return self._cases[case_id]
