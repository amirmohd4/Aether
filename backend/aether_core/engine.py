from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Iterable
from uuid import uuid4

from .domain import Case, TaskState, TaskStatus, now_iso
from .synthetic_government import SyntheticGovernmentSystem
from .templates import TEMPLATES, infer_template


class AetherExecutionEngine:
    """Core case executor for the Aether MVP."""

    def __init__(self) -> None:
        self.cases: Dict[str, Case] = {}
        self.gov = SyntheticGovernmentSystem()

    def create_case(self, objective: str, customer_type: str, jurisdiction: Dict[str, str], inputs: Dict[str, Any] | None = None) -> Case:
        template = infer_template(objective, customer_type)
        requirements_fn, tasks_fn = TEMPLATES[template]
        tasks = {d.id: TaskState(definition=d) for d in tasks_fn()}
        case = Case(
            case_id=f"A-{uuid4().hex[:10].upper()}",
            objective=objective,
            customer_type=customer_type,
            jurisdiction=jurisdiction,
            inputs=inputs or {},
            requirements=requirements_fn(),
            tasks=tasks,
        )
        self.cases[case.case_id] = case
        self._refresh_ready(case)
        return case

    def get_case(self, case_id: str) -> Case:
        if case_id not in self.cases:
            raise KeyError(case_id)
        return self.cases[case_id]

    def _refresh_ready(self, case: Case) -> None:
        for task in case.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
            deps = [case.tasks[d] for d in task.definition.dependencies if d in case.tasks]
            if any(d.status in {TaskStatus.EXCEPTION, TaskStatus.HUMAN_REVIEW, TaskStatus.BLOCKED} for d in deps):
                task.status = TaskStatus.BLOCKED
            elif all(d.status == TaskStatus.COMPLETED for d in deps):
                task.status = TaskStatus.READY

    def ready_tasks(self, case: Case) -> Iterable[TaskState]:
        return [t for t in case.tasks.values() if t.status == TaskStatus.READY]

    def execute_until_pause(self, case_id: str) -> Case:
        case = self.get_case(case_id)
        case.status = "executing"
        while True:
            self._refresh_ready(case)
            ready = list(self.ready_tasks(case))
            if not ready:
                break
            with ThreadPoolExecutor(max_workers=min(8, len(ready))) as pool:
                futures = {pool.submit(self._execute_task, case, task): task for task in ready}
                for future in as_completed(futures):
                    task = futures[future]
                    try:
                        future.result()
                    except Exception as exc:
                        task.status = TaskStatus.EXCEPTION
                        task.error = str(exc)
                        case.exceptions.append({"task_id": task.definition.id, "error": str(exc)})
            self._refresh_ready(case)
            if any(t.status == TaskStatus.HUMAN_REVIEW for t in case.tasks.values()):
                case.status = "waiting_for_human"
                break

        if all(t.status == TaskStatus.COMPLETED for t in case.tasks.values()):
            case.status = "completed"
            case.outcome = {"status": "completed", "message": "Case completed by Aether."}
        elif any(t.status == TaskStatus.EXCEPTION for t in case.tasks.values()):
            case.status = "exception"
        elif any(t.status == TaskStatus.HUMAN_REVIEW for t in case.tasks.values()):
            case.status = "waiting_for_human"
        else:
            case.status = "waiting"
        case.updated_at = now_iso()
        return case

    def _execute_task(self, case: Case, task: TaskState) -> None:
        task.status = TaskStatus.RUNNING
        task.started_at = now_iso()
        task.attempts += 1
        definition = task.definition
        if definition.authority_required or definition.physical_action:
            task.status = TaskStatus.HUMAN_REVIEW
            case.human_actions.append({
                "task_id": definition.id,
                "task": definition.name,
                "reason": "Legal authority or physical action is required.",
            })
            return

        operation = self._operation_for(definition.id)
        result = self.gov.execute(
            definition.department,
            operation,
            {**case.inputs, "jurisdiction": case.jurisdiction, "case_id": case.case_id},
        )
        if definition.id == "registration_record" and case.inputs.get("simulate_conflict"):
            result["result"]["area"] = case.inputs.get("conflicting_registration_area", 2.08)

        task.result = result["result"]
        task.evidence.append({
            "source": result["result"].get("source", definition.department),
            "request_id": result["request_id"],
            "operation": operation,
            "verified": True,
        })
        case.evidence.extend(task.evidence)
        task.status = TaskStatus.COMPLETED
        task.completed_at = now_iso()

        if definition.id == "risk_reconciliation":
            self._reconcile_property(case)
        elif definition.id == "cross_record_reconciliation":
            self._reconcile_restaurant(case)

    def _reconcile_property(self, case: Case) -> None:
        land = case.tasks.get("land_record")
        registration = case.tasks.get("registration_record")
        if not land or not registration or not land.result or not registration.result:
            return
        if land.result.get("area") != registration.result.get("area"):
            case.exceptions.append({
                "type": "record_conflict",
                "severity": "high",
                "message": "Property area differs between land and registration records.",
                "evidence": {"land_area": land.result.get("area"), "registration_area": registration.result.get("area")},
            })
            legal = case.tasks.get("legal_review")
            if legal and legal.status == TaskStatus.PENDING:
                legal.status = TaskStatus.HUMAN_REVIEW
                case.human_actions.append({
                    "task_id": "legal_review",
                    "task": "Review material exceptions",
                    "reason": "Aether detected conflicting property records.",
                })

    def _reconcile_restaurant(self, case: Case) -> None:
        if not case.inputs.get("premises_verified", True):
            case.exceptions.append({
                "type": "premises_exception",
                "severity": "medium",
                "message": "Premises verification needs human review.",
            })

    @staticmethod
    def _operation_for(task_id: str) -> str:
        mapping = {
            "identity_check": "identity", "land_record": "land_record", "registration_record": "registration_record",
            "court_search": "court_search", "tax_dues": "tax_dues", "tax_check": "tax_dues",
            "premises_check": "land_record", "zoning_check": "zoning", "business_check": "business",
            "food_application": "food", "food_review": "food", "fire_application": "fire", "fire_review": "fire",
            "municipal_application": "municipal", "municipal_review": "municipal", "zoning": "zoning",
            "building": "building", "fire": "fire", "environment": "environment", "rera": "rera",
            "utility": "utility", "document_intake": "document", "encumbrance": "registration_record", "inspection": "inspection",
        }
        return mapping.get(task_id, "generic")

    def complete_human_task(self, case_id: str, task_id: str, decision: str, note: str = "") -> Case:
        case = self.get_case(case_id)
        if task_id not in case.tasks:
            raise KeyError(task_id)
        task = case.tasks[task_id]
        if task.status != TaskStatus.HUMAN_REVIEW:
            raise ValueError(f"Task {task_id} is not awaiting human action")
        task.result = {"decision": decision, "note": note, "authority": "authorised_human"}
        task.evidence.append({"source": "authorised_human", "decision": decision, "note": note})
        task.status = TaskStatus.COMPLETED
        task.completed_at = now_iso()
        case.human_actions = [a for a in case.human_actions if a["task_id"] != task_id]
        case.updated_at = now_iso()
        return self.execute_until_pause(case_id)


engine = AetherExecutionEngine()
