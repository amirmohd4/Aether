from __future__ import annotations

from typing import Any, Dict, Iterable, Set


def _ids(items: Iterable[Dict[str, Any]] | None) -> Set[str]:
    values = set()
    for item in items or []:
        if isinstance(item, dict):
            value = item.get("id") or item.get("code") or item.get("name")
            if value:
                values.add(str(value))
        elif item:
            values.add(str(item))
    return values


def diff_process_profiles(old: Dict[str, Any] | None, new: Dict[str, Any] | None) -> Dict[str, Any]:
    old = old or {}
    new = new or {}

    old_steps = _ids(old.get("steps"))
    new_steps = _ids(new.get("steps"))
    old_docs = _ids(old.get("required_documents"))
    new_docs = _ids(new.get("required_documents"))
    old_auth = _ids(old.get("authority_matrix"))
    new_auth = _ids(new.get("authority_matrix"))

    changed = []
    for key in ("receiving_portal", "official_form_reference", "effective_date", "source_url"):
        if old.get(key) != new.get(key):
            changed.append(key)

    if old.get("service_level") != new.get("service_level"):
        changed.append("service_level")

    return {
        "service_id": new.get("service_id") or old.get("service_id"),
        "old_effective_date": old.get("effective_date"),
        "new_effective_date": new.get("effective_date"),
        "added_steps": sorted(new_steps - old_steps),
        "removed_steps": sorted(old_steps - new_steps),
        "added_documents": sorted(new_docs - old_docs),
        "removed_documents": sorted(old_docs - new_docs),
        "changed_authority_entries": sorted((old_auth ^ new_auth)),
        "changed_metadata": sorted(set(changed)),
        "impact": {
            "requires_recheck": bool(
                changed
                or old_steps != new_steps
                or old_docs != new_docs
                or old_auth != new_auth
            ),
            "invalidate_open_submissions": bool(new_docs - old_docs or new_steps - old_steps),
            "reprepare_forms": "official_form_reference" in changed or old_steps != new_steps,
            "recalculate_deadline": "service_level" in changed,
            "revalidate_authority": old_auth != new_auth,
        },
        "safety": {
            "do_not_rewrite_completed_cases_automatically": True,
            "do_not_claim_legal_effect_without_authoritative_source": True,
        },
    }


def case_impact(case, profile_diff: Dict[str, Any]) -> Dict[str, Any]:
    affected = []
    if case.service_id and case.service_id == profile_diff.get("service_id"):
        if profile_diff.get("impact", {}).get("requires_recheck"):
            affected = [
                task_id
                for task_id, task in case.tasks.items()
                if task.status.value not in {"completed"}
                or task.definition.department.strip().lower() == "aether"
            ]

    return {
        "case_id": case.case_id,
        "affected": bool(affected),
        "affected_task_ids": affected,
        "recommended_action": (
            "Run branch-level replan and regenerate only affected packets/forms."
            if affected
            else "No open work requires replan."
        ),
        "preserve_completed_evidence": True,
    }
