from __future__ import annotations

from collections import Counter
from typing import Any, Dict


def summarize_cases(cases: list[Dict[str, Any]]) -> Dict[str, Any]:
    statuses = Counter(case.get("status", "unknown") for case in cases)
    services = Counter(case.get("service_id") or "unresolved" for case in cases)
    departments = Counter(case.get("service_department") or "unassigned" for case in cases)
    totals = [case.get("tasks_total", 0) for case in cases]
    completed = [case.get("tasks_completed", 0) for case in cases]
    return {
        "case_count": len(cases),
        "status_counts": dict(statuses),
        "service_counts": dict(services),
        "department_counts": dict(departments),
        "tasks_total": sum(totals),
        "tasks_completed": sum(completed),
        "completion_rate": round((sum(completed) / sum(totals) * 100) if sum(totals) else 0, 2),
        "human_actions_pending": sum(case.get("human_actions", 0) for case in cases),
        "exceptions": sum(case.get("exceptions", 0) for case in cases),
    }
