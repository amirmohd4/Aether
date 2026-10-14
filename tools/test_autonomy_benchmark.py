import csv
import tempfile
import unittest
from pathlib import Path

from tools.autonomy_benchmark import analyze


FIELDS = [
    "case_id", "task_id", "execution_mode", "task_status",
    "manual_intervention", "outcome_verified", "outcome_correct",
    "unauthorized_action", "baseline_staff_minutes", "actual_staff_minutes",
    "baseline_handoffs", "actual_handoffs",
]


def write_csv(rows):
    handle = tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8", suffix=".csv", delete=False)
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    handle.close()
    return Path(handle.name)


def task(task_id, mode, status, intervention="false", verified="true", correct="true", unauthorized="false"):
    return {
        "case_id": "case-1", "task_id": task_id, "execution_mode": mode,
        "task_status": status, "manual_intervention": intervention,
        "outcome_verified": verified, "outcome_correct": correct,
        "unauthorized_action": unauthorized, "baseline_staff_minutes": "30",
        "actual_staff_minutes": "10", "baseline_handoffs": "3", "actual_handoffs": "1",
    }


class AutonomyBenchmarkTests(unittest.TestCase):
    def test_computes_autonomy_and_impact_without_claiming_live_validation(self):
        path = write_csv([
            task("intake", "automated", "completed"),
            task("review", "human", "completed", intervention="true"),
            task("verify", "automated", "blocked"),
        ])
        try:
            result = analyze(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(result["cases"], 1)
        self.assertEqual(result["tasks"], 3)
        self.assertEqual(result["autonomous_task_rate"], 0.3333)
        self.assertEqual(result["automated_task_share"], 0.6667)
        self.assertEqual(result["manual_interventions"], 1)
        self.assertEqual(result["staff_minutes_reduced"], 20.0)
        self.assertEqual(result["handoffs_removed"], 2.0)
        self.assertFalse(result["release_gate"]["pass"])
        self.assertIn("not independently validated", result["measurement_scope"])

    def test_passes_gate_only_when_all_tasks_complete_and_outcome_is_verified(self):
        path = write_csv([
            task("intake", "automated", "completed"),
            task("review", "human", "completed", intervention="true"),
        ])
        try:
            result = analyze(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertTrue(result["release_gate"]["pass"])

    def test_fails_gate_on_unauthorized_action(self):
        path = write_csv([task("submit", "automated", "completed", unauthorized="true")])
        try:
            result = analyze(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(result["unauthorized_actions"], 1)
        self.assertFalse(result["release_gate"]["pass"])

    def test_rejects_inconsistent_case_outcome_flags(self):
        rows = [
            task("intake", "automated", "completed", verified="true", correct="true"),
            task("verify", "automated", "completed", verified="false", correct="false"),
        ]
        path = write_csv(rows)
        try:
            with self.assertRaisesRegex(ValueError, "repeated consistently"):
                analyze(path)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
