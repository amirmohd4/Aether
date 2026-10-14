#!/usr/bin/env python3
"""Compute Aether autonomy metrics from a case/task CSV export.

This reports measured inputs only; it does not infer successful outcomes from
submission events. See docs/AUTONOMOUS_EXECUTION_PROOF.md for the schema.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

TRUE = {"1", "true", "yes", "y"}
FALSE = {"0", "false", "no", "n", ""}


def boolean(value: str, field: str, row_number: int) -> bool:
    normalized = (value or "").strip().lower()
    if normalized in TRUE:
        return True
    if normalized in FALSE:
        return False
    raise ValueError(f"row {row_number}: {field} must be true/false, got {value!r}")


def number(value: str, field: str, row_number: int) -> float:
    try:
        parsed = float(value or 0)
    except ValueError as exc:
        raise ValueError(f"row {row_number}: {field} must be numeric") from exc
    if parsed < 0:
        raise ValueError(f"row {row_number}: {field} cannot be negative")
    return parsed


def analyze(path: Path) -> dict:
    required = {
        "case_id", "task_id", "execution_mode", "task_status",
        "manual_intervention", "outcome_verified", "outcome_correct",
        "unauthorized_action", "baseline_staff_minutes", "actual_staff_minutes",
        "baseline_handoffs", "actual_handoffs",
    }
    cases: dict[str, dict] = {}
    seen_tasks: set[tuple[str, str]] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV missing required columns: " + ", ".join(sorted(missing)))
        for row_number, row in enumerate(reader, start=2):
            case_id = (row.get("case_id") or "").strip()
            task_id = (row.get("task_id") or "").strip()
            if not case_id or not task_id:
                raise ValueError(f"row {row_number}: case_id and task_id are required")
            key = (case_id, task_id)
            if key in seen_tasks:
                raise ValueError(f"row {row_number}: duplicate case_id/task_id {key!r}")
            seen_tasks.add(key)
            mode = (row.get("execution_mode") or "").strip().lower()
            status = (row.get("task_status") or "").strip().lower()
            if mode not in {"automated", "human", "mixed"}:
                raise ValueError(f"row {row_number}: execution_mode must be automated, human, or mixed")
            if status not in {"completed", "failed", "blocked", "pending"}:
                raise ValueError(f"row {row_number}: invalid task_status {status!r}")
            case = cases.setdefault(case_id, {
                "tasks": [], "baseline_staff_minutes": None, "actual_staff_minutes": None,
                "baseline_handoffs": None, "actual_handoffs": None,
                "outcome_verified": None, "outcome_correct": None,
            })
            measures = {
                "baseline_staff_minutes": number(row.get("baseline_staff_minutes", ""), "baseline_staff_minutes", row_number),
                "actual_staff_minutes": number(row.get("actual_staff_minutes", ""), "actual_staff_minutes", row_number),
                "baseline_handoffs": number(row.get("baseline_handoffs", ""), "baseline_handoffs", row_number),
                "actual_handoffs": number(row.get("actual_handoffs", ""), "actual_handoffs", row_number),
            }
            for name, value in measures.items():
                if case[name] is not None and case[name] != value:
                    raise ValueError(f"row {row_number}: {name} must be consistent across all tasks in case {case_id!r}")
                case[name] = value
            task = {
                "mode": mode,
                "status": status,
                "intervention": boolean(row.get("manual_intervention", ""), "manual_intervention", row_number),
                "verified": boolean(row.get("outcome_verified", ""), "outcome_verified", row_number),
                "correct": boolean(row.get("outcome_correct", ""), "outcome_correct", row_number),
                "unauthorized": boolean(row.get("unauthorized_action", ""), "unauthorized_action", row_number),
            }
            if task["correct"] and not task["verified"]:
                raise ValueError(f"row {row_number}: outcome_correct cannot be true unless outcome_verified is true")
            for name, value in (("outcome_verified", task["verified"]), ("outcome_correct", task["correct"])):
                if case[name] is not None and case[name] != value:
                    raise ValueError(f"row {row_number}: {name} must be repeated consistently across all tasks in case {case_id!r}")
                case[name] = value
            case["tasks"].append(task)

    if not cases:
        raise ValueError("CSV contains no task rows")

    tasks = [task for case in cases.values() for task in case["tasks"]]
    total_tasks = len(tasks)
    automated_tasks = sum(task["mode"] == "automated" for task in tasks)
    completed_tasks = sum(task["status"] == "completed" for task in tasks)
    automated_completed = sum(task["mode"] == "automated" and task["status"] == "completed" and not task["intervention"] for task in tasks)
    interventions = sum(task["intervention"] for task in tasks)
    total_cases = len(cases)
    verified_cases = sum(bool(case["outcome_verified"]) for case in cases.values())
    correct_verified_cases = sum(bool(case["outcome_correct"]) for case in cases.values())
    unauthorized_actions = sum(task["unauthorized"] for task in tasks)
    baseline_staff = sum(case["baseline_staff_minutes"] or 0 for case in cases.values())
    actual_staff = sum(case["actual_staff_minutes"] or 0 for case in cases.values())
    baseline_handoffs = sum(case["baseline_handoffs"] or 0 for case in cases.values())
    actual_handoffs = sum(case["actual_handoffs"] or 0 for case in cases.values())
    return {
        "measurement_scope": "provided CSV only; not independently validated",
        "cases": total_cases,
        "tasks": total_tasks,
        "task_completion_rate": round(completed_tasks / total_tasks, 4),
        "autonomous_task_rate": round(automated_completed / total_tasks, 4),
        "automated_task_share": round(automated_tasks / total_tasks, 4),
        "manual_interventions": interventions,
        "cases_with_verified_outcome": verified_cases,
        "verified_outcome_case_rate": round(verified_cases / total_cases, 4),
        "correct_outcome_case_rate": round(correct_verified_cases / total_cases, 4),
        "unauthorized_actions": unauthorized_actions,
        "baseline_staff_minutes": round(baseline_staff, 2),
        "actual_staff_minutes": round(actual_staff, 2),
        "staff_minutes_reduced": round(baseline_staff - actual_staff, 2),
        "staff_minutes_reduction_rate": round((baseline_staff - actual_staff) / baseline_staff, 4) if baseline_staff else None,
        "baseline_handoffs": baseline_handoffs,
        "actual_handoffs": actual_handoffs,
        "handoffs_removed": baseline_handoffs - actual_handoffs,
        "handoff_reduction_rate": round((baseline_handoffs - actual_handoffs) / baseline_handoffs, 4) if baseline_handoffs else None,
        "release_gate": {
            "pass": unauthorized_actions == 0 and verified_cases == total_cases and correct_verified_cases == total_cases,
            "criteria": "zero unauthorized actions; every case has a verified and correct outcome",
            "note": "This gate is necessary, not sufficient. Security, resilience, legal authority, and source-system reconciliation require separate review.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV containing one row per task")
    args = parser.parse_args()
    try:
        result = analyze(args.csv_file)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
