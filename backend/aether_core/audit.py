from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


def event(action: str, actor: str, case_id: str, data: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "actor": actor,
        "case_id": case_id,
        "data": data or {},
    }


class AuditTrail:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def record(self, action: str, actor: str, case_id: str, data: Dict[str, Any] | None = None):
        self.events.append(event(action, actor, case_id, data))

    def for_case(self, case_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.events if e["case_id"] == case_id]
