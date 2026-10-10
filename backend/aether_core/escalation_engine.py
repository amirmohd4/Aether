from __future__ import annotations

from typing import Any, Dict, List


def classify_escalation(case) -> Dict[str, Any]:
    objective = str(case.objective or "").lower()
    reasons: List[str] = []
    score = 0

    if any(token in objective for token in ("appeal", "hearing", "notice", "legal", "court")):
        score += 30
        reasons.append("legal/adjudicatory language detected")

    if any(token in objective for token in ("fire", "hazardous", "dangerous", "safety", "medical")):
        score += 25
        reasons.append("safety-sensitive objective")

    if len(case.exceptions) >= 1:
        score += 25
        reasons.append("unresolved exception present")
    if len(case.exceptions) >= 3:
        score += 15
        reasons.append("repeated exception pattern")

    human_tasks = sum(
        1 for task in case.tasks.values()
        if task.definition.authority_required or task.definition.physical_action
    )
    score += min(20, human_tasks * 5)
    if human_tasks:
        reasons.append("statutory or field boundary remains")

    repeated_attempts = sum(max(0, task.attempts - 1) for task in case.tasks.values())
    if repeated_attempts:
        score += min(20, repeated_attempts * 5)
        reasons.append("repeated task attempts")

    level = (
        "critical" if score >= 70
        else "high" if score >= 45
        else "medium" if score >= 25
        else "normal"
    )

    return {
        "level": level,
        "score": min(100, score),
        "reasons": reasons,
        "supervisor_attention": level in {"critical", "high"},
        "employee_action": (
            "Escalate with prepared decision/inspection packet."
            if level in {"critical", "high"}
            else "Continue automated processing; surface exceptions if they appear."
        ),
        "statutory_decision_automation": False,
    }
