from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def build_deadline_guard(
    *,
    case_created_at: str | None,
    process_profile: Dict[str, Any] | None,
    task_states: Dict[str, Any],
) -> Dict[str, Any]:
    profile = process_profile or {}
    service_level = profile.get("service_level") or {}
    deadline_at = service_level.get("deadline_at")
    source = profile.get("source_url")

    if not deadline_at:
        return {
            "status": "no_authoritative_deadline",
            "deadline_at": None,
            "deadline_source": source,
            "risk": "unknown",
            "reason": "No effective-dated jurisdiction SLA/deadline was supplied; Aether will not invent one.",
        }

    try:
        deadline = datetime.fromisoformat(str(deadline_at).replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        remaining_minutes = int((deadline - now).total_seconds() / 60)
    except (TypeError, ValueError):
        return {
            "status": "invalid_profile_deadline",
            "deadline_at": deadline_at,
            "deadline_source": source,
            "risk": "unknown",
        }

    incomplete = [
        task_id for task_id, state in task_states.items()
        if isinstance(state, dict) and state.get("status") not in {"completed"}
    ]

    return {
        "status": "tracked",
        "deadline_at": deadline.isoformat(),
        "deadline_source": source,
        "remaining_minutes": remaining_minutes,
        "risk": "breach" if remaining_minutes < 0 else "high" if remaining_minutes <= 120 else "normal",
        "incomplete_task_count": len(incomplete),
        "incomplete_task_ids": incomplete[:50],
        "escalation_recommended": remaining_minutes <= 120 and bool(incomplete),
        "note": "Legal/service-level timing comes only from the loaded jurisdiction process profile.",
    }
