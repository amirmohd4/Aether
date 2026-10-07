from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from threading import RLock
from typing import Any, Dict, List


def _event_hash(entry: Dict[str, Any]) -> str:
    canonical = json.dumps(
        {
            "sequence": entry["sequence"],
            "timestamp": entry["timestamp"],
            "action": entry["action"],
            "actor": entry["actor"],
            "case_id": entry["case_id"],
            "data": entry["data"],
            "previous_hash": entry["previous_hash"],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def event(
    action: str,
    actor: str,
    case_id: str,
    data: Dict[str, Any] | None = None,
    sequence: int = 0,
    previous_hash: str | None = None,
) -> Dict[str, Any]:
    entry = {
        "sequence": sequence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "actor": actor,
        "case_id": case_id,
        "data": data or {},
        "previous_hash": previous_hash,
    }
    entry["event_hash"] = _event_hash(entry)
    return entry


class AuditTrail:
    """Append-only tamper-evident execution ledger."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._last_hashes: Dict[str, str] = {}
        self._lock = RLock()

    def seed_case(self, case_id: str, previous_hash: str | None) -> None:
        """Seed a recovered case so a restarted process continues its chain."""
        if previous_hash:
            with self._lock:
                self._last_hashes.setdefault(case_id, previous_hash)

    def record(self, action: str, actor: str, case_id: str, data: Dict[str, Any] | None = None):
        with self._lock:
            previous = self._last_hashes.get(case_id)
            entry = event(
                action,
                actor,
                case_id,
                data,
                sequence=len(self.events) + 1,
                previous_hash=previous,
            )
            self.events.append(entry)
            self._last_hashes[case_id] = entry["event_hash"]
            return entry

    @staticmethod
    def verify_chain(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        previous = None
        for index, item in enumerate(events, start=1):
            if item.get("previous_hash") != previous:
                return {
                    "valid": False,
                    "checked_events": index - 1,
                    "reason": "previous_hash mismatch",
                }
            expected = _event_hash({
                "sequence": item.get("sequence", 0),
                "timestamp": item.get("timestamp", ""),
                "action": item.get("action", ""),
                "actor": item.get("actor", ""),
                "case_id": item.get("case_id", ""),
                "data": item.get("data") or {},
                "previous_hash": item.get("previous_hash"),
            })
            if item.get("event_hash") != expected:
                return {
                    "valid": False,
                    "checked_events": index - 1,
                    "reason": "event_hash mismatch",
                }
            previous = item.get("event_hash")
        return {
            "valid": True,
            "checked_events": len(events),
            "head_hash": previous,
        }

    def for_case(self, case_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return [e.copy() for e in self.events if e["case_id"] == case_id]
