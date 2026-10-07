from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .domain import Case, TaskState, TaskStatus


@dataclass(frozen=True)
class DependencySnapshot:
    ready: List[str]
    waiting: List[str]
    blocked: List[str]


class DependencyEngine:
    """Recalculates task availability without globally pausing the case.

    A normal digital task remains pending behind a human/physical prerequisite.
    A statutory-authority task is marked blocked when its unresolved dependency
    chain contains a human/physical action, making the authority boundary
    visible without treating the case itself as failed.
    """

    def refresh(self, case: Case) -> DependencySnapshot:
        ready: List[str] = []
        waiting: List[str] = []
        blocked: List[str] = []

        def has_unresolved_authority_ancestor(task_id: str, seen: set[str] | None = None) -> bool:
            seen = seen or set()
            if task_id in seen or task_id not in case.tasks:
                return False
            seen.add(task_id)
            current = case.tasks[task_id]
            if current.status == TaskStatus.HUMAN_REVIEW:
                return True
            for dependency_id in current.definition.dependencies:
                dependency = case.tasks.get(dependency_id)
                if not dependency:
                    continue
                if dependency.definition.authority_required or dependency.definition.physical_action:
                    if dependency.status == TaskStatus.HUMAN_REVIEW:
                        return True
                if dependency.status in {TaskStatus.PENDING, TaskStatus.BLOCKED} and has_unresolved_authority_ancestor(dependency_id, seen):
                    return True
            return False

        for task in case.tasks.values():
            if task.status in {
                TaskStatus.COMPLETED,
                TaskStatus.RUNNING,
                TaskStatus.EXCEPTION,
                TaskStatus.HUMAN_REVIEW,
            }:
                continue

            dependencies = [
                case.tasks[dependency_id]
                for dependency_id in task.definition.dependencies
                if dependency_id in case.tasks
            ]

            if any(dep.status == TaskStatus.EXCEPTION for dep in dependencies):
                task.status = TaskStatus.BLOCKED
                blocked.append(task.definition.id)
            elif task.definition.authority_required and has_unresolved_authority_ancestor(task.definition.id):
                task.status = TaskStatus.BLOCKED
                blocked.append(task.definition.id)
            elif all(dep.status == TaskStatus.COMPLETED for dep in dependencies):
                task.status = TaskStatus.READY
                ready.append(task.definition.id)
            else:
                # Unfinished prerequisites are a wait state, not a failure.
                task.status = TaskStatus.PENDING
                waiting.append(task.definition.id)

        return DependencySnapshot(ready=ready, waiting=waiting, blocked=blocked)

    @staticmethod
    def ready_tasks(case: Case) -> Iterable[TaskState]:
        return (task for task in case.tasks.values() if task.status == TaskStatus.READY)

    @staticmethod
    def executable_tasks(case: Case) -> List[TaskState]:
        return [
            task for task in case.tasks.values()
            if task.status == TaskStatus.READY
            and not task.definition.authority_required
            and not task.definition.physical_action
        ]
