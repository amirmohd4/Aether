from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any, Dict, List


def event(action: str, actor: str, case_id: str, data: Dict[str, Any] | None = None, sequence: int = 0) -> Dict[str, Any]:
    return {
        "sequence": sequence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "actor": actor,
        "case_id": case_id,
        "data": data or {},
    }


class AuditTrail:
    """Append-only in-process execution ledger; replace storage backend later."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._lock = RLock()

    def record(self, action: str, actor: str, case_id: str, data: Dict[str, Any] | None = None):
        with self._lock:
            entry = event(action, actor, case_id, data, sequence=len(self.events) + 1)
            self.events.append(entry)
            return entry

    def for_case(self, case_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return [e.copy() for e in self.events if e["case_id"] == case_id]
