from __future__ import annotations

from typing import Any, Dict, List

from .domain import Case, TaskState, TaskStatus
from .process_work_recipes import work_recipe, work_atom_metadata
from .government_process_kernel import infer_process_profile


class EmployeeAutomationService:
    """Translate an Aether case into an employee-facing work brief.

    The service deliberately separates administrative work Aether can automate
    from statutory/physical work that must remain with an authorised human.
    Time figures are planning estimates only and are intended to be replaced
    by observed customer telemetry in production pilots.
    """

    ADMIN_MINUTES: Dict[str, int] = {
        "DocumentWorker": 15,
        "ReconciliationWorker": 12,
        "DecisionWorker": 10,
        "OutcomeWorker": 5,
        "DigitalWorker": 8,
        "HumanAuthorityWorker": 15,
    }

    def brief(self, case: Case) -> Dict[str, Any]:
        tasks = list(case.tasks.values())
        completed_automations = [
            task for task in tasks
            if task.status == TaskStatus.COMPLETED
            and self._is_automatable(task)
        ]
        human_tasks = [
            task for task in tasks
            if task.status == TaskStatus.HUMAN_REVIEW
            or task.definition.authority_required
            or task.definition.physical_action
        ]
        exception_tasks = [task for task in tasks if task.status == TaskStatus.EXCEPTION]
        blocked_tasks = [task for task in tasks if task.status == TaskStatus.BLOCKED]
        ready_automations = [
            task for task in tasks
            if task.status == TaskStatus.READY and self._is_automatable(task)
        ]
        waiting_tasks = [task for task in tasks if task.status == TaskStatus.PENDING]

        current_admin_minutes = sum(
            self._current_minutes(task)
            for task in tasks
            if task.status == TaskStatus.COMPLETED and self._is_automatable(task)
        )
        estimated_aether_minutes = sum(
            self._aether_minutes(task)
            for task in completed_automations
        )
        minutes_saved = max(0, current_admin_minutes - estimated_aether_minutes)

        attention = self._attention_items(case, human_tasks, exception_tasks, blocked_tasks)
        next_actions = self._next_actions(case, ready_automations, human_tasks, exception_tasks, blocked_tasks)
        revenue_signals = self._revenue_signals(case)
        profile = infer_process_profile(
            None if not case.service_id else type("_ServiceRef", (), {
                "id": case.service_id,
                "department": case.service_department or "",
            })()
        )
        recipe = work_recipe(profile.key)

        return {
            "mode": "operator_intelligence",
            "case_id": case.case_id,
            "summary": {
                "automated_completed": len(completed_automations),
                "automation_eligible_total": sum(1 for task in tasks if self._is_automatable(task)),
                "human_or_physical_total": len(human_tasks),
                "exceptions": len(exception_tasks),
                "blocked": len(blocked_tasks),
                "waiting": len(waiting_tasks),
                "employee_attention_required": len(attention),
            },
            "time": {
                "estimated_admin_minutes_if_manual": current_admin_minutes,
                "estimated_aether_admin_minutes": estimated_aether_minutes,
                "estimated_minutes_saved": minutes_saved,
                "note": "Planning estimate based on task class; replace with observed pilot telemetry.",
            },
            "attention_items": attention[:12],
            "next_best_actions": next_actions[:12],
            "customer_actions": self._customer_actions(case),
            "revenue_signals": revenue_signals,
            "process": {
                "profile": profile.key,
                "label": profile.label,
                "employee_work_recipe": recipe,
                "work_atoms": {
                    atom: work_atom_metadata().get(atom)
                    for atom in recipe
                    if atom in work_atom_metadata()
                },
            },
        }

    def _is_automatable(self, task: TaskState) -> bool:
        return not task.definition.authority_required and not task.definition.physical_action

    def _current_minutes(self, task: TaskState) -> int:
        return self.ADMIN_MINUTES.get(task.definition.worker, 8)

    @staticmethod
    def _aether_minutes(task: TaskState) -> int:
        # Aether still incurs compute/oversight, but it should remove the
        # repetitive human coordination step. This is intentionally conservative.
        if task.definition.worker == "DocumentWorker":
            return 1
        if task.definition.worker == "ReconciliationWorker":
            return 1
        if task.definition.worker in {"DecisionWorker", "OutcomeWorker"}:
            return 1
        return 1

    def _attention_items(
        self,
        case: Case,
        human_tasks: List[TaskState],
        exception_tasks: List[TaskState],
        blocked_tasks: List[TaskState],
    ) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for task in exception_tasks:
            items.append({
                "priority": "high",
                "type": "exception",
                "task_id": task.definition.id,
                "title": task.definition.name,
                "action": task.error or "Resolve the exception and resume the affected branch.",
            })
        for task in human_tasks:
            items.append({
                "priority": "required",
                "type": "human_boundary",
                "task_id": task.definition.id,
                "title": task.definition.name,
                "action": (
                    "Complete the statutory decision."
                    if task.definition.authority_required
                    else "Complete the physical/inspection action."
                ),
            })
        for task in blocked_tasks:
            items.append({
                "priority": "blocked",
                "type": "blocked",
                "task_id": task.definition.id,
                "title": task.definition.name,
                "action": "Resolve the upstream exception before this work can continue.",
            })
        if not items and case.status == "completed":
            items.append({
                "priority": "done",
                "type": "completed",
                "task_id": None,
                "title": "No employee action required",
                "action": "Aether completed the digital work for this case.",
            })
        return items

    def _next_actions(
        self,
        case: Case,
        ready_automations: List[TaskState],
        human_tasks: List[TaskState],
        exception_tasks: List[TaskState],
        blocked_tasks: List[TaskState],
    ) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        for task in exception_tasks:
            actions.append({
                "priority": 1,
                "type": "exception",
                "task_id": task.definition.id,
                "owner": "employee",
                "action": task.error or "Resolve exception",
            })
        for task in human_tasks:
            actions.append({
                "priority": 2,
                "type": "human",
                "task_id": task.definition.id,
                "owner": task.definition.department,
                "action": (
                    "Review and record the statutory decision"
                    if task.definition.authority_required
                    else "Complete the required physical action"
                ),
            })
        for task in ready_automations:
            actions.append({
                "priority": 3,
                "type": "automated",
                "task_id": task.definition.id,
                "owner": "Aether",
                "action": f"Aether can execute: {task.definition.name}",
            })
        for task in blocked_tasks:
            actions.append({
                "priority": 4,
                "type": "blocked",
                "task_id": task.definition.id,
                "owner": "employee",
                "action": "Resolve upstream exception",
            })
        for task in self._pending_critical(case):
            actions.append({
                "priority": 5,
                "type": "waiting",
                "task_id": task.definition.id,
                "owner": task.definition.department,
                "action": "Waiting on prerequisite work",
            })
        return sorted(actions, key=lambda item: (item["priority"], item["task_id"] or ""))

    @staticmethod
    def _pending_critical(case: Case) -> List[TaskState]:
        critical = set(case.critical_path())
        return [
            task for task in case.tasks.values()
            if task.definition.id in critical and task.status == TaskStatus.PENDING
        ]

    @staticmethod
    def _customer_actions(case: Case) -> List[Dict[str, Any]]:
        required: List[str] = []
        for requirement in case.requirements:
            for document in requirement.get("documents", []):
                if document not in required:
                    required.append(document)

        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in case.inputs.get("documents", [])
        }
        return [
            {"type": "missing_document", "document": document, "action": "Upload this document to continue"}
            for document in required
            if document not in submitted
        ][:20]

    @staticmethod
    def _revenue_signals(case: Case) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []
        dues = []
        for task in case.tasks.values():
            result = task.result or {}
            if isinstance(result, dict) and result.get("dues"):
                dues.append({
                    "task_id": task.definition.id,
                    "dues": result.get("dues"),
                    "source": result.get("source", "government record"),
                })
        if dues:
            signals.append({
                "type": "outstanding_dues",
                "status": "attention",
                "items": dues,
                "action": "Reconcile dues before final outcome where applicable.",
            })
        if case.service_outcome:
            signals.append({
                "type": "fee_reconciliation",
                "status": "recommended",
                "action": "Reconcile applicable government fee, payment and outcome records.",
            })
        return signals
