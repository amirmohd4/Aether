from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable


def build_operator_batches(briefs: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[tuple[str, str], Dict[str, Any]] = defaultdict(
        lambda: {"task_ids": [], "case_ids": [], "owners": set(), "count": 0}
    )

    for brief in briefs:
        case_id = str(brief.get("case_id") or "")
        for action in brief.get("next_best_actions") or []:
            if action.get("type") != "automated":
                continue
            task_id = str(action.get("task_id") or "")
            owner = str(action.get("owner") or "Aether")
            key = (task_id, owner)
            item = groups[key]
            item["task_ids"].append(task_id)
            item["case_ids"].append(case_id)
            item["owners"].add(owner)
            item["count"] += 1

    batches = []
    for (task_id, owner), item in groups.items():
        unique_cases = sorted(set(item["case_ids"]))
        if len(unique_cases) < 2:
            continue
        batches.append({
            "batch_key": f"{owner}:{task_id}",
            "task_id": task_id,
            "owner": owner,
            "case_count": len(unique_cases),
            "case_ids": unique_cases,
            "suggested_action": (
                "Process these cases as one work batch where the connected "
                "departmental system and applicable rules permit batching."
            ),
            "expected_benefit": "Reduce repeated case opening, repeated lookups and repeated handoff preparation.",
            "authority_safe": True,
            "execution_mode": "prepare_and_review",
        })

    batches.sort(key=lambda item: (-item["case_count"], item["batch_key"]))
    return batches[:50]
