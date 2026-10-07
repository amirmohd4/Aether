from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import RLock
from typing import Any, Dict, Iterable
from uuid import uuid4

from .audit import AuditTrail
from .case_store import DatabaseCaseStore
from .domain import Case, TaskState, TaskStatus, now_iso
from .dependency_engine import DependencyEngine
from .task_queue import DurableTaskQueue, TaskClaim
from .verification import VerificationEngine
from .ontology import GovernmentOntologyBuilder, WorkGraphBuilder
from .reliability import RetryPolicy
from .synthetic_government import SyntheticGovernmentSystem
from .templates import TEMPLATES, generic_tasks, infer_template
from .service_registry import ServiceRegistry
from .workers import WorkerContext, WorkerRegistry


class AetherExecutionEngine:
    """Objective-driven, dependency-aware execution engine for the Aether MVP."""

    def __init__(self) -> None:
        self.cases: Dict[str, Case] = {}
        self.gov = SyntheticGovernmentSystem()
        self.workers = WorkerRegistry(self.gov)
        self.services = ServiceRegistry()
        self.ontology_builder = GovernmentOntologyBuilder()
        self.work_graph_builder = WorkGraphBuilder()
        self.dependencies = DependencyEngine()
        self.retry_policy = RetryPolicy(max_attempts=3)
        self.audit = AuditTrail()
        self.store = DatabaseCaseStore()
        self.queue = DurableTaskQueue()
        self.verifier = VerificationEngine()
        self._event_lock = RLock()
        self._case_locks: Dict[str, RLock] = {}

    def _lock_for(self, case_id: str) -> RLock:
        with self._event_lock:
            return self._case_locks.setdefault(case_id, RLock())

    def create_case(
        self,
        objective: str,
        customer_type: str,
        jurisdiction: Dict[str, str],
        inputs: Dict[str, Any] | None = None,
        owner_user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> Case:
        service = self.services.resolve(objective, customer_type)
        template = infer_template(objective, customer_type, service)
        enriched_inputs = {**(inputs or {}), "customer_type": customer_type}

        if template in TEMPLATES:
            requirements_fn, tasks_fn = TEMPLATES[template]
            requirements = requirements_fn()
            task_definitions = tasks_fn()
        elif service:
            requirements = []
            task_definitions = generic_tasks(service)
        else:
            requirements = []
            task_definitions = []

        tasks = {definition.id: TaskState(definition=definition) for definition in task_definitions}
        ontology = self.ontology_builder.build(enriched_inputs, objective, service)
        work_graph = self.work_graph_builder.build(
            service, [state.definition for state in tasks.values()]
        )
        case = Case(
            case_id=f"A-{uuid4().hex[:10].upper()}",
            objective=objective,
            customer_type=customer_type,
            jurisdiction=jurisdiction,
            inputs=enriched_inputs,
            requirements=requirements,
            tasks=tasks,
            owner_user_id=owner_user_id,
            tenant_id=tenant_id,
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
        if tenant_id:
            self.store.record_usage(
                tenant_id=tenant_id,
                event_type="case_started",
                units=1,
                unit_type="case",
                case_id=case.case_id,
                customer_type=customer_type,
                metadata={"service_id": case.service_id, "service_outcome": case.service_outcome},
            )
        return case

    def get_case(self, case_id: str) -> Case:
        if case_id in self.cases:
            return self.cases[case_id]
        case = self.store.get(case_id)
        self._hydrate_task_checkpoints(case)
        self.cases[case_id] = case
        return case

    def _hydrate_task_checkpoints(self, case: Case) -> None:
        checkpoints = self.store.task_checkpoints(case.case_id)
        for task_id, checkpoint in checkpoints.items():
            task = case.tasks.get(task_id)
            if task is None:
                continue
            try:
                task.status = TaskStatus(checkpoint["status"])
            except (KeyError, ValueError):
                continue
            task.result = checkpoint.get("result")
            task.evidence = checkpoint.get("evidence", [])
            task.error = checkpoint.get("error")
            task.started_at = checkpoint.get("started_at")
            task.completed_at = checkpoint.get("completed_at")
            task.attempts = checkpoint.get("attempts", task.attempts)
            task.idempotency_key = checkpoint.get("idempotency_key") or task.idempotency_key

    def _checkpoint_task(self, case: Case, task: TaskState) -> None:
        self.store.put_task_checkpoint(case.case_id, task)

    def _refresh_ready(self, case: Case) -> None:
        self.dependencies.refresh(case)

    def ready_tasks(self, case: Case) -> Iterable[TaskState]:
        return self.dependencies.ready_tasks(case)

    def _production_connector_guard(self, task) -> None:
        import os

        if os.getenv("AETHER_ENV", "development").strip().lower() != "production":
            return
        if os.getenv("AETHER_ALLOW_SYNTHETIC_IN_PRODUCTION", "").strip().lower() == "true":
            return

        department = task.definition.department.strip().lower()
        internal_departments = {"aether", "authorised authority", "authorised officer"}
        if department in internal_departments:
            return
        if not self.workers.production_connector(task.definition.department):
            raise RuntimeError(
                f"Live execution blocked: no production connector configured for {task.definition.department}."
            )

    def _production_rule_guard(self, case: Case) -> None:
        """Prevent live connector execution when rules are not authoritative."""
        import os
        production = os.getenv("AETHER_ENV", "development").strip().lower() == "production"
        if not production or not self.workers.production_connectors_configured():
            return
        if not case.requirements:
            raise RuntimeError("Live connector execution requires verified requirements")
        unverified = [
            req for req in case.requirements
            if req.get("authority_status") != "source_backed"
        ]
        if unverified and os.getenv("AETHER_ALLOW_BASELINE_RULES", "").strip().lower() != "true":
            raise RuntimeError(
                "Live connector execution is blocked because one or more requirements "
                "lack authoritative, effective-dated rule provenance."
            )

    def execute_until_pause(self, case_id: str) -> Case:
        case = self.get_case(case_id)
        self._production_rule_guard(case)
        self.queue.reclaim_expired(case_id)
        self._recover_task_states(case)
        with self._lock_for(case_id):
            case.status = "executing"
            while True:
                self._refresh_ready(case)
                ready = list(self.ready_tasks(case))
                if not ready:
                    break

                executable = [
                    task for task in ready
                    if not task.definition.authority_required and not task.definition.physical_action
                ]
                boundaries = [
                    task for task in ready
                    if task.definition.authority_required or task.definition.physical_action
                ]
                for task in boundaries:
                    task.status = TaskStatus.HUMAN_REVIEW
                    self._checkpoint_task(case, task)
                    if not any(a.get("task_id") == task.definition.id for a in case.human_actions):
                        reason = (
                            "Physical action is required."
                            if task.definition.physical_action
                            else "Statutory human authority is required."
                        )
                        case.human_actions.append({
                            "task_id": task.definition.id,
                            "task": task.definition.name,
                            "reason": reason,
                            "created_at": now_iso(),
                        })
                        self._emit(
                            case,
                            "human_action.requested",
                            "aether.authority_boundary",
                            {"task_id": task.definition.id, "reason": reason},
                        )

                # Recalculate immediately after a boundary becomes active so
                # downstream authority tasks are visibly blocked rather than
                # retaining the stale pre-boundary pending state.
                self._refresh_ready(case)

                if not executable:
                    break

                for task in executable:
                    self.queue.enqueue(
                        case.case_id,
                        task.definition.id,
                        {
                            "worker": task.definition.worker,
                            "department": task.definition.department,
                            "operation": task.definition.operation or self._operation_for(task.definition.id),
                        },
                    )

                claims: list[TaskClaim] = []
                for _ in executable:
                    claim = self.queue.claim(case.case_id)
                    if claim is None:
                        break
                    claims.append(claim)

                if not claims:
                    break

                with ThreadPoolExecutor(max_workers=min(8, len(claims))) as pool:
                    futures = {}
                    for claim in claims:
                        task = case.tasks.get(claim.task_id)
                        if task is None or task.status != TaskStatus.READY:
                            self.queue.fail(claim.queue_id, "Task no longer ready", retry=False)
                            continue
                        futures[pool.submit(self._execute_task, case, task, claim.queue_id)] = (task, claim)

                    for future in as_completed(futures):
                        task, claim = futures[future]
                        try:
                            future.result()
                        except Exception as exc:
                            if task.status not in {TaskStatus.HUMAN_REVIEW, TaskStatus.EXCEPTION}:
                                task.status = TaskStatus.EXCEPTION
                            task.error = task.error or str(exc)
                            case.exceptions.append({
                                "task_id": task.definition.id,
                                "error": task.error,
                                "timestamp": now_iso(),
                            })

                self.store.put(case)
                self._refresh_ready(case)

            statuses = [task.status for task in case.tasks.values()]
            if statuses and all(status == TaskStatus.COMPLETED for status in statuses):
                already_completed = case.status == "completed"
                case.status = "completed"
                case.outcome = {
                    "status": "completed",
                    "message": "Case completed by Aether.",
                    "service_outcome": case.service_outcome,
                }
                self._emit(case, "case.completed", "aether.outcome_engine", case.outcome)
                if case.tenant_id and not already_completed:
                    self.store.record_usage(
                        tenant_id=case.tenant_id,
                        event_type="case_completed",
                        units=1,
                        unit_type="outcome",
                        case_id=case.case_id,
                        customer_type=case.customer_type,
                        metadata={"service_id": case.service_id, "service_outcome": case.service_outcome},
                    )
            elif any(status == TaskStatus.EXCEPTION for status in statuses):
                case.status = "exception"
            elif any(status == TaskStatus.HUMAN_REVIEW for status in statuses):
                case.status = "waiting_for_human"
            elif case.tasks:
                case.status = "waiting"
            else:
                case.status = "needs_clarification"

            case.updated_at = now_iso()
            self.store.put(case)
            return case

    def _execute_task(self, case: Case, task: TaskState, queue_id: int | None = None) -> None:
        definition = task.definition
        self._production_connector_guard(task)
        operation = definition.operation or self._operation_for(definition.id)
        worker = self.workers.get(definition.worker)
        task.idempotency_key = task.idempotency_key or f"{case.case_id}:{definition.id}"

        last_error: Exception | None = None
        for _ in range(self.retry_policy.max_attempts):
            task.status = TaskStatus.RUNNING
            task.started_at = task.started_at or now_iso()
            task.attempts += 1
            self._checkpoint_task(case, task)
            self._emit(case, "task.attempted", "aether.execution_engine", {
                "task_id": definition.id,
                "attempt": task.attempts,
                "idempotency_key": task.idempotency_key,
            })
            try:
                result = worker.execute(WorkerContext(
                    case_id=case.case_id,
                    department=definition.department,
                    operation=operation,
                    payload={
                        **case.inputs,
                        "task_results": {
                            task_id: state.result
                            for task_id, state in case.tasks.items()
                            if state.result is not None
                        },
                        "case_exceptions": list(case.exceptions),
                        "service_id": case.service_id,
                        "service_outcome": case.service_outcome,
                        "jurisdiction": case.jurisdiction,
                        "required_documents": [
                            document
                            for requirement in case.requirements
                            for document in requirement.get("documents", [])
                        ],
                        "case_id": case.case_id,
                        "idempotency_key": task.idempotency_key,
                    },
                ))

                if result.get("status") == "query":
                    task.status = TaskStatus.HUMAN_REVIEW
                    task.result = result.get("result", {})
                    task.error = "Government system returned a query requiring review."
                    case.human_actions.append({
                        "task_id": definition.id,
                        "task": definition.name,
                        "reason": "Government query requires evidence review or response.",
                        "created_at": now_iso(),
                    })
                    self._emit(case, "government.query", definition.worker, {
                        "task_id": definition.id,
                        "request_id": result.get("request_id"),
                    })
                    self._checkpoint_task(case, task)
                    if queue_id is not None:
                        self.queue.complete(queue_id)
                    return

                if result.get("status") == "rejected":
                    raise RuntimeError(
                        result.get("result", {}).get("reason", "Government system rejected the request.")
                    )

                if definition.id == "registration_record" and case.inputs.get("simulate_conflict"):
                    result["result"]["area"] = case.inputs.get("conflicting_registration_area", 2.08)

                task.result = result["result"]
                evidence = {
                    "source": result["result"].get("source", definition.department),
                    "request_id": result["request_id"],
                    "operation": operation,
                    "idempotency_key": task.idempotency_key,
                    "verified": True,
                    "timestamp": now_iso(),
                }
                required_documents = (
                    [doc for req in case.requirements for doc in req.get("documents", [])]
                    if definition.id == "document_intake" and case.inputs.get("enforce_intake_gate")
                    else []
                )
                verification = self.verifier.verify_result(
                    definition.id,
                    result["result"],
                    required_documents,
                    list(case.inputs.get("documents", [])),
                )
                evidence["verification"] = verification.as_dict()
                task.evidence.append(evidence)
                case.evidence.append(evidence)

                if verification.status == "exception":
                    for finding in verification.findings:
                        case.exceptions.append({
                            "type": finding.code,
                            "severity": finding.severity,
                            "message": finding.message,
                            "evidence": finding.evidence or {},
                            "task_id": definition.id,
                            "timestamp": now_iso(),
                        })
                    task.result["verification"] = verification.as_dict()
                    if verification.risk_level in {"high", "medium"}:
                        task.status = TaskStatus.HUMAN_REVIEW
                        case.human_actions.append({
                            "task_id": definition.id,
                            "task": definition.name,
                            "reason": "Evidence verification detected an exception requiring authorised review.",
                            "created_at": now_iso(),
                        })
                        self._emit(case, "exception.escalated", "aether.verification_engine", {
                            "task_id": definition.id,
                            "risk_level": verification.risk_level,
                            "findings": verification.as_dict()["findings"],
                        })
                        self._checkpoint_task(case, task)
                        if queue_id is not None:
                            self.queue.complete(queue_id)
                        return

                task.status = TaskStatus.COMPLETED
                task.completed_at = now_iso()
                self._checkpoint_task(case, task)
                self._emit(case, "task.completed", definition.worker, {
                    "task_id": definition.id,
                    "attempts": task.attempts,
                    "request_id": result["request_id"],
                })

                if definition.id == "risk_reconciliation":
                    self._reconcile_property(case)
                elif definition.id == "cross_record_reconciliation":
                    self._reconcile_restaurant(case)
                if queue_id is not None:
                    self.queue.complete(queue_id)
                return
            except Exception as exc:
                last_error = exc
                self._emit(case, "task.failed_attempt", definition.worker, {
                    "task_id": definition.id,
                    "attempt": task.attempts,
                    "error": str(exc),
                })

        task.status = TaskStatus.EXCEPTION
        task.error = str(last_error or "Task failed")
        self._checkpoint_task(case, task)
        self._emit(case, "task.exception", definition.worker, {
            "task_id": definition.id,
            "attempts": task.attempts,
            "error": task.error,
        })
        if queue_id is not None:
            self.queue.fail(queue_id, task.error, retry=False)
        raise RuntimeError(task.error)

    def _recover_task_states(self, case: Case) -> None:
        """Turn expired queue leases back into schedulable task state."""
        rows = {row["task_id"]: row for row in self.queue.for_case(case.case_id)}
        for task_id, task in case.tasks.items():
            row = rows.get(task_id)
            if task.status == TaskStatus.RUNNING and row and row["status"] == self.queue.READY:
                task.status = TaskStatus.PENDING
                task.error = None

    def _reconcile_property(self, case: Case) -> None:
        land = case.tasks.get("land_record")
        registration = case.tasks.get("registration_record")
        if not land or not registration or not land.result or not registration.result:
            return
        if land.result.get("area") != registration.result.get("area"):
            exception = {
                "type": "record_conflict",
                "severity": "high",
                "message": "Property area differs between land and registration records.",
                "evidence": {
                    "land_area": land.result.get("area"),
                    "registration_area": registration.result.get("area"),
                },
            }
            case.exceptions.append(exception)
            legal = case.tasks.get("legal_review")
            if legal and legal.status in {TaskStatus.PENDING, TaskStatus.READY}:
                legal.status = TaskStatus.HUMAN_REVIEW
                case.human_actions.append({
                    "task_id": "legal_review",
                    "task": "Review material exceptions",
                    "reason": "Aether detected conflicting property records.",
                    "created_at": now_iso(),
                })
                self._checkpoint_task(case, legal)
                self._emit(case, "exception.escalated", "aether.risk_engine", exception)

    def _reconcile_restaurant(self, case: Case) -> None:
        if not case.inputs.get("premises_verified", True):
            case.exceptions.append({
                "type": "premises_exception",
                "severity": "medium",
                "message": "Premises verification needs human review.",
            })

    @staticmethod
    def _operation_for(task_id: str) -> str:
        return {
            "identity_check": "identity",
            "land_record": "land_record",
            "registration_record": "registration_record",
            "court_search": "court_search",
            "tax_dues": "tax_dues",
            "tax_check": "tax_dues",
            "premises_check": "land_record",
            "zoning_check": "zoning",
            "business_check": "business",
            "food_application": "food",
            "food_review": "food",
            "fire_application": "fire",
            "fire_review": "fire",
            "municipal_application": "municipal",
            "municipal_review": "municipal",
            "zoning": "zoning",
            "building": "building",
            "fire": "fire",
            "environment": "environment",
            "rera": "rera",
            "utility": "utility",
            "document_intake": "document",
            "encumbrance": "registration_record",
            "inspection": "inspection",
            "risk_reconciliation": "reconciliation",
            "cross_record_reconciliation": "reconciliation",
            "reconciliation": "reconciliation",
            "verification": "reconciliation",
            "department_processing": "service_processing",
            "decision_package": "decision_package",
            "evidence_package": "decision_package",
            "outcome": "outcome",
            "record_update": "record_update",
            "certificate": "certificate",
        }.get(task_id, "generic")

    def complete_human_task(
        self, case_id: str, task_id: str, decision: str, note: str = "",
        actor_id: str = "authorised_human", actor_role: str = "authorised_officer",
    ) -> Case:
        case = self.get_case(case_id)
        with self._lock_for(case_id):
            if task_id not in case.tasks:
                raise KeyError(task_id)
            task = case.tasks[task_id]
            if task.status != TaskStatus.HUMAN_REVIEW:
                raise ValueError(f"Task {task_id} is not awaiting human action")

            approved = decision.lower() in {
                "approve", "approved", "pass", "passed", "accept", "accepted"
            }
            if not approved:
                task.status = TaskStatus.EXCEPTION
                task.error = note or "Human authority rejected the action."
                case.exceptions.append({
                    "task_id": task_id,
                    "error": task.error,
                    "timestamp": now_iso(),
                })
                self._checkpoint_task(case, task)
                self._emit(case, "human_action.rejected", actor_id, {
                    "task_id": task_id,
                    "note": note,
                })
            else:
                task.result = {
                    "decision": "approved",
                    "note": note,
                    "authority": actor_id,
                    "role": actor_role,
                }
                task.evidence.append({
                    "source": "authorised_human",
                    "decision": "approved",
                    "note": note,
                    "timestamp": now_iso(),
                })
                task.status = TaskStatus.COMPLETED
                task.completed_at = now_iso()
                self._checkpoint_task(case, task)
                self._emit(case, "human_action.approved", actor_id, {
                    "task_id": task_id,
                    "note": note,
                })

            case.human_actions = [
                action for action in case.human_actions
                if action.get("task_id") != task_id
            ]
            case.updated_at = now_iso()
            self.store.put(case)

        return self.execute_until_pause(case_id)

    def _emit(
        self,
        case: Case,
        action: str,
        actor: str,
        data: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        with self._event_lock:
            previous_hash = (
                case.execution_events[-1].get("event_hash")
                if case.execution_events
                else None
            )
            if not self.audit.for_case(case.case_id):
                self.audit.seed_case(case.case_id, previous_hash)

            entry = {
                "sequence": len(case.execution_events) + 1,
                "timestamp": now_iso(),
                "action": action,
                "actor": actor,
                "data": data or {},
            }
            audit_entry = self.audit.record(action, actor, case.case_id, data)
            entry["previous_hash"] = audit_entry.get("previous_hash")
            entry["event_hash"] = audit_entry.get("event_hash")
            case.execution_events.append(entry)
            self.store.append_event(
                case.case_id,
                action,
                actor,
                data,
                previous_hash=audit_entry.get("previous_hash"),
                event_hash=audit_entry.get("event_hash"),
                sequence=entry["sequence"],
            )
            return entry


engine = AetherExecutionEngine()
