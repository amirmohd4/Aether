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
    """Recalculates task availability without globally pausing the case."""

    def refresh(self, case: Case) -> DependencySnapshot:
        ready: List[str] = []
        waiting: List[str] = []
        blocked: List[str] = []

        for task in case.tasks.values():
            if task.status in {TaskStatus.COMPLETED, TaskStatus.RUNNING, TaskStatus.EXCEPTION, TaskStatus.HUMAN_REVIEW}:
                continue

            dependencies = [
                case.tasks[dependency_id]
                for dependency_id in task.definition.dependencies
                if dependency_id in case.tasks
            ]

            if any(dep.status == TaskStatus.EXCEPTION for dep in dependencies):
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
