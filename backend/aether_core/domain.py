from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    EXCEPTION = "exception"
    HUMAN_REVIEW = "human_review"


@dataclass
class TaskDefinition:
    id: str
    name: str
    department: str
    worker: str
    dependencies: List[str] = field(default_factory=list)
    authority_required: bool = False
    physical_action: bool = False
    description: str = ""


@dataclass
class TaskState:
    definition: TaskDefinition
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    attempts: int = 0


@dataclass
class Case:
    case_id: str
    objective: str
    customer_type: str
    jurisdiction: Dict[str, str]
    inputs: Dict[str, Any]
    requirements: List[Dict[str, Any]]
    tasks: Dict[str, TaskState]
    status: str = "executing"
    human_actions: List[Dict[str, Any]] = field(default_factory=list)
    exceptions: List[Dict[str, Any]] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    outcome: Optional[Dict[str, Any]] = None
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    service_department: Optional[str] = None
    service_outcome: Optional[str] = None
    ontology: Dict[str, Any] = field(default_factory=dict)
    work_graph: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def summary(self) -> Dict[str, Any]:
        counts = {status.value: 0 for status in TaskStatus}
        for task in self.tasks.values():
            counts[task.status.value] += 1

        return {
            "case_id": self.case_id,
            "objective": self.objective,
            "customer_type": self.customer_type,
            "service_id": self.service_id,
            "service_name": self.service_name,
            "service_department": self.service_department,
            "service_outcome": self.service_outcome,
            "ontology": self.ontology,
            "work_graph": self.work_graph,
            "jurisdiction": self.jurisdiction,
            "status": self.status,
            "tasks_total": len(self.tasks),
            "tasks_completed": counts["completed"],
            "tasks_running": counts["running"],
            "tasks_waiting": counts["pending"] + counts["blocked"],
            "exceptions": counts["exception"],
            "human_actions": counts["human_review"],
            "ready": counts["ready"],
            "critical_path": self.critical_path(),
            "human_work_remaining": self.human_work_remaining(),
            "updated_at": self.updated_at,
        }

    def critical_path(self) -> List[str]:
        # MVP approximation: longest dependency chain among unfinished tasks.
        memo: Dict[str, List[str]] = {}

        def walk(task_id: str) -> List[str]:
            if task_id in memo:
                return memo[task_id]
            task = self.tasks[task_id]
            deps = [d for d in task.definition.dependencies if d in self.tasks]
            unfinished = task.status not in {TaskStatus.COMPLETED}
            if not deps:
                path = [task_id] if unfinished else []
            else:
                longest = max((walk(d) for d in deps), key=len, default=[])
                path = longest + ([task_id] if unfinished else [])
            memo[task_id] = path
            return path

        paths = [walk(tid) for tid in self.tasks]
        return max(paths, key=len, default=[])

    def human_work_remaining(self) -> int:
        # Demo estimate only; never presented as a real-world government SLA.
        return sum(
            15 if t.definition.authority_required else 0
            for t in self.tasks.values()
            if t.status not in {TaskStatus.COMPLETED}
        )


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class OntologyEntity:
    id: str
    type: str
    label: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OntologyRelationship:
    subject_id: str
    relation: str
    object_id: str


@dataclass
class GovernmentOntology:
    entities: Dict[str, OntologyEntity] = field(default_factory=dict)
    relationships: List[OntologyRelationship] = field(default_factory=list)

    def add_entity(self, entity: OntologyEntity) -> None:
        self.entities[entity.id] = entity

    def add_relationship(self, relationship: OntologyRelationship) -> None:
        if relationship.subject_id in self.entities and relationship.object_id in self.entities:
            self.relationships.append(relationship)

    def related(self, entity_id: str, relation: str | None = None) -> List[OntologyRelationship]:
        return [
            r for r in self.relationships
            if r.subject_id == entity_id or r.object_id == entity_id
            if relation is None or r.relation == relation
        ]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "entities": [
                {"id": e.id, "type": e.type, "label": e.label, "attributes": e.attributes}
                for e in self.entities.values()
            ],
            "relationships": [
                {"subject_id": r.subject_id, "relation": r.relation, "object_id": r.object_id}
                for r in self.relationships
            ],
        }


@dataclass(frozen=True)
class WorkNode:
    id: str
    task_id: str
    department: str
    worker: str
    action: str
    dependencies: List[str] = field(default_factory=list)
    authority_required: bool = False
    physical_action: bool = False
    reason: str = ""


@dataclass
class WorkGraph:
    nodes: Dict[str, WorkNode] = field(default_factory=dict)

    def add(self, node: WorkNode) -> None:
        self.nodes[node.id] = node

    def ready(self, completed: set[str]) -> List[WorkNode]:
        return [
            node for node in self.nodes.values()
            if node.id not in completed and all(dep in completed for dep in node.dependencies)
        ]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "task_id": n.task_id,
                    "department": n.department,
                    "worker": n.worker,
                    "action": n.action,
                    "dependencies": n.dependencies,
                    "authority_required": n.authority_required,
                    "physical_action": n.physical_action,
                    "reason": n.reason,
                }
                for n in self.nodes.values()
            ]
        }
