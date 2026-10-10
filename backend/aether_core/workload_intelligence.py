from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List


def build_workload_snapshot(cases: Iterable[Any]) -> Dict[str, Any]:
    by_department: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {
            "pending": 0,
            "running": 0,
            "human_review": 0,
            "exceptions": 0,
            "completed": 0,
            "oldest_age_minutes": 0,
        }
    )
    critical_cases: List[Dict[str, Any]] = []

    now = datetime.now(timezone.utc)

    for case in cases:
        case_attention = len(case.exceptions)
        oldest_minutes = 0

        for task in case.tasks.values():
            department = str(task.definition.department or "Unassigned")
            bucket = by_department[department]
            status = task.status.value

            if status == "completed":
                bucket["completed"] += 1
                continue
            if status == "running":
                bucket["running"] += 1
            elif status == "human_review":
                bucket["human_review"] += 1
            elif status == "exception":
                bucket["exceptions"] += 1
                case_attention += 1
            else:
                bucket["pending"] += 1

            started = task.started_at or task.definition.id
            if isinstance(started, str) and "T" in started:
                try:
                    dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                    age = max(0, int((now - dt).total_seconds() / 60))
                    oldest_minutes = max(oldest_minutes, age)
                except ValueError:
                    pass

        for values in [by_department[str(t.definition.department or "Unassigned")] for t in case.tasks.values()]:
            values["oldest_age_minutes"] = max(values["oldest_age_minutes"], oldest_minutes)

        if case_attention or case.human_actions:
            critical_cases.append({
                "case_id": case.case_id,
                "service_id": case.service_id,
                "status": case.status,
                "exceptions": len(case.exceptions),
                "human_actions": len(case.human_actions),
                "oldest_age_minutes": oldest_minutes,
            })

    departments = []
    for department, stats in sorted(by_department.items()):
        active = stats["pending"] + stats["running"] + stats["human_review"] + stats["exceptions"]
        departments.append({
            "department": department,
            "active_work": active,
            **stats,
            "management_attention": "high" if stats["exceptions"] or stats["oldest_age_minutes"] >= 120 else "normal",
        })

    critical_cases.sort(
        key=lambda item: (-item["exceptions"], -item["human_actions"], -item["oldest_age_minutes"])
    )

    return {
        "departments": departments,
        "critical_cases": critical_cases[:50],
        "principles": {
            "measure_lateral_movement": True,
            "surface_subject_or_service_bottlenecks": True,
            "batch_repeatable_work": True,
            "do_not_auto_reassign_without_authority_policy": True,
        },
    }
