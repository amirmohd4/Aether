from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Iterable
from uuid import uuid4

from .audit import AuditTrail
from .case_store import DatabaseCaseStore
from .domain import Case, TaskState, TaskStatus, now_iso
from .dependency_engine import DependencyEngine
from .ontology import GovernmentOntologyBuilder, WorkGraphBuilder
from .reliability import RetryPolicy
from .synthetic_government import SyntheticGovernmentSystem
from .templates import TEMPLATES, infer_template
from .service_registry import ServiceRegistry
from .workers import WorkerContext, WorkerRegistry


class AetherExecutionEngine:
    """Objective-driven, dependency-aware execution engine for the Aether MVP."""

    def __init__(self) -> None:
        self.cases: Dict[str, Case] = {}  # compatibility cache; durable state lives in DatabaseCaseStore
        self.gov = SyntheticGovernmentSystem()
        self.workers = WorkerRegistry(self.gov)
        self.services = ServiceRegistry()
        self.ontology_builder = GovernmentOntologyBuilder()
        self.work_graph_builder = WorkGraphBuilder()
        self.dependencies = DependencyEngine()
        self.retry_policy = RetryPolicy(max_attempts=3)
        self.audit = AuditTrail()
        self.store = DatabaseCaseStore()

    def create_case(self, objective: str, customer_type: str, jurisdiction: Dict[str, str], inputs: Dict[str, Any] | None = None) -> Case:
        service = self.services.resolve(objective, customer_type)
        template = service.template if service and service.template in TEMPLATES else infer_template(objective, customer_type)
        requirements_fn, tasks_fn = TEMPLATES[template]
        tasks = {d.id: TaskState(definition=d) for d in tasks_fn()}
        enriched_inputs = {**(inputs or {}), "customer_type": customer_type}
        ontology = self.ontology_builder.build(enriched_inputs, objective, service)
        work_graph = self.work_graph_builder.build(service, [state.definition for state in tasks.values()])
        case = Case(
            case_id=f"A-{uuid4().hex[:10].upper()}", objective=objective,
            customer_type=customer_type, jurisdiction=jurisdiction, inputs=enriched_inputs,
            requirements=requirements_fn(), tasks=tasks,
            service_id=service.id if service else None,
            service_name=service.name if service else None,
            service_department=service.department if service else None,
            service_outcome=service.outcome if service else None,
            ontology=ontology.as_dict(),
            work_graph=work_graph.as_dict(),
        )
        self.cases[case.case_id] = case
        self._refresh_ready(case)
        self.store.put(case)
        return case

    def get_case(self, case_id: str) -> Case:
        if case_id in self.cases:
            return self.cases[case_id]
        case = self.store.get(case_id)
        self.cases[case_id] = case
        return case

    def _refresh_ready(self, case: Case) -> None:
        self.dependencies.refresh(case)

    def ready_tasks(self, case: Case) -> Iterable[TaskState]:
        return self.dependencies.ready_tasks(case)

    def execute_until_pause(self, case_id: str) -> Case:
        case = self.get_case(case_id)
        case.status = "executing"
        while True:
            self._refresh_ready(case)
            ready = list(self.ready_tasks(case))
            if not ready:
                break

            # Physical actions and statutory authority are hard boundaries.
            executable = [t for t in ready if not t.definition.authority_required and not t.definition.physical_action]
            boundaries = [t for t in ready if t.definition.authority_required or t.definition.physical_action]
            for task in boundaries:
                task.status = TaskStatus.HUMAN_REVIEW
                case.human_actions.append({
                    "task_id": task.definition.id,
                    "task": task.definition.name,
                    "reason": "Legal authority or physical action is required.",
                    "created_at": now_iso(),
                })

            if not executable:
                break

            with ThreadPoolExecutor(max_workers=min(8, len(executable))) as pool:
                futures = {pool.submit(self._execute_task, case, task): task for task in executable}
                for future in as_completed(futures):
                    task = futures[future]
                    try:
                        future.result()
                    except Exception as exc:
                        task.status = TaskStatus.EXCEPTION
                        task.error = str(exc)
                        case.exceptions.append({"task_id": task.definition.id, "error": str(exc), "timestamp": now_iso()})

            # A human-review branch must not pause unrelated executable branches.
            # Recalculate dependencies and continue until no executable work remains.
            self._refresh_ready(case)

        statuses = [t.status for t in case.tasks.values()]
        if statuses and all(s == TaskStatus.COMPLETED for s in statuses):
            case.status = "completed"
            case.outcome = {"status": "completed", "message": "Case completed by Aether."}
        elif any(s == TaskStatus.EXCEPTION for s in statuses):
            case.status = "exception"
        elif any(s == TaskStatus.HUMAN_REVIEW for s in statuses):
            case.status = "waiting_for_human"
        else:
            case.status = "waiting"
        case.updated_at = now_iso()
        self.store.put(case)
        return case

    def _execute_task(self, case: Case, task: TaskState) -> None:
        definition = task.definition
        operation = self._operation_for(definition.id)
        worker = self.workers.get(definition.worker)
        task.idempotency_key = task.idempotency_key or f"{case.case_id}:{definition.id}"

        last_error = None
        for _ in range(self.retry_policy.max_attempts):
            task.status = TaskStatus.RUNNING
            task.started_at = task.started_at or now_iso()
            task.attempts += 1
            self._emit(case, "task.attempted", "aether.execution_engine", {
                "task_id": definition.id, "attempt": task.attempts,
                "idempotency_key": task.idempotency_key,
            })
            try:
                result = worker.execute(WorkerContext(
                    case_id=case.case_id, department=definition.department,
                    operation=operation,
                    payload={
                        **case.inputs, "jurisdiction": case.jurisdiction,
                        "case_id": case.case_id, "idempotency_key": task.idempotency_key,
                    },
                ))
                if definition.id == "registration_record" and case.inputs.get("simulate_conflict"):
                    result["result"]["area"] = case.inputs.get("conflicting_registration_area", 2.08)
                task.result = result["result"]
                evidence = {
                    "source": result["result"].get("source", definition.department),
                    "request_id": result["request_id"], "operation": operation,
                    "idempotency_key": task.idempotency_key, "verified": True, "timestamp": now_iso(),
                }
                task.evidence.append(evidence)
                case.evidence.append(evidence)
                task.status = TaskStatus.COMPLETED
                task.completed_at = now_iso()
                self._emit(case, "task.completed", definition.worker, {
                    "task_id": definition.id, "attempts": task.attempts, "request_id": result["request_id"],
                })
                if definition.id == "risk_reconciliation":
                    self._reconcile_property(case)
                elif definition.id == "cross_record_reconciliation":
                    self._reconcile_restaurant(case)
                return
            except Exception as exc:
                last_error = exc
                self._emit(case, "task.failed_attempt", definition.worker, {
                    "task_id": definition.id, "attempt": task.attempts, "error": str(exc),
                })
        task.status = TaskStatus.EXCEPTION
        task.error = str(last_error or "Task failed")
        self._emit(case, "task.exception", definition.worker, {
            "task_id": definition.id, "attempts": task.attempts, "error": task.error,
        })
        raise RuntimeError(task.error)

    @staticmethod
    def _emit(case: Case, action: str, actor: str, data: Dict[str, Any] | None = None) -> None:
        entry = {
            "sequence": len(case.execution_events) + 1, "timestamp": now_iso(),
            "action": action, "actor": actor, "data": data or {},
        }
        case.execution_events.append(entry)
        self.audit.record(action, actor, case.case_id, data)
        self.store.append_event(case.case_id, action, actor, data)
    def _reconcile_property(self, case: Case) -> None:
        land, registration = case.tasks.get("land_record"), case.tasks.get("registration_record")
        if not land or not registration or not land.result or not registration.result:
            return
        if land.result.get("area") != registration.result.get("area"):
            case.exceptions.append({
                "type": "record_conflict", "severity": "high",
                "message": "Property area differs between land and registration records.",
                "evidence": {"land_area": land.result.get("area"), "registration_area": registration.result.get("area")},
            })
            legal = case.tasks.get("legal_review")
            if legal and legal.status == TaskStatus.PENDING:
                legal.status = TaskStatus.HUMAN_REVIEW
                case.human_actions.append({
                    "task_id": "legal_review", "task": "Review material exceptions",
                    "reason": "Aether detected conflicting property records.", "created_at": now_iso(),
                })

    def _reconcile_restaurant(self, case: Case) -> None:
        if not case.inputs.get("premises_verified", True):
            case.exceptions.append({"type": "premises_exception", "severity": "medium", "message": "Premises verification needs human review."})

    @staticmethod
    def _operation_for(task_id: str) -> str:
        return {
            "identity_check": "identity", "land_record": "land_record", "registration_record": "registration_record",
            "court_search": "court_search", "tax_dues": "tax_dues", "tax_check": "tax_dues", "premises_check": "land_record",
            "zoning_check": "zoning", "business_check": "business", "food_application": "food", "food_review": "food",
            "fire_application": "fire", "fire_review": "fire", "municipal_application": "municipal", "municipal_review": "municipal",
            "zoning": "zoning", "building": "building", "fire": "fire", "environment": "environment", "rera": "rera",
            "utility": "utility", "document_intake": "document", "encumbrance": "registration_record", "inspection": "inspection",
            "risk_reconciliation": "reconciliation", "cross_record_reconciliation": "reconciliation", "decision_package": "decision_package",
            "evidence_package": "decision_package", "outcome": "outcome", "record_update": "record_update", "certificate": "certificate",
        }.get(task_id, "generic")

    def complete_human_task(self, case_id: str, task_id: str, decision: str, note: str = "") -> Case:
        case = self.get_case(case_id)
        if task_id not in case.tasks:
            raise KeyError(task_id)
        task = case.tasks[task_id]
        if task.status != TaskStatus.HUMAN_REVIEW:
            raise ValueError(f"Task {task_id} is not awaiting human action")
        if decision.lower() not in {"approve", "approved", "pass", "passed", "accept", "accepted"}:
            task.status = TaskStatus.EXCEPTION
            task.error = note or "Human authority rejected the action."
            case.exceptions.append({"task_id": task_id, "error": task.error, "timestamp": now_iso()})
        else:
            task.result = {"decision": "approved", "note": note, "authority": "authorised_human"}
            task.evidence.append({"source": "authorised_human", "decision": "approved", "note": note, "timestamp": now_iso()})
            task.status = TaskStatus.COMPLETED
            task.completed_at = now_iso()
        case.human_actions = [a for a in case.human_actions if a.get("task_id") != task_id]
        case.updated_at = now_iso()
        return self.execute_until_pause(case_id)


engine = AetherExecutionEngine()
