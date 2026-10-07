from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from threading import Lock

from database import SessionLocal, engine
from .domain import Case, TaskDefinition, TaskState, TaskStatus
from .persistence_models import AetherCaseRecord, AetherExecutionEventRecord


class DatabaseCaseStore:
    """Durable V2 repository using PostgreSQL when configured, SQLite locally otherwise."""

    def __init__(self):
        self._schema_ready = False
        self._schema_lock = Lock()

    def _ensure_schema(self) -> None:
        if self._schema_ready:
            return
        with self._schema_lock:
            if self._schema_ready:
                return
            from database import Base
            Base.metadata.create_all(bind=engine)
            self._schema_ready = True

    def put(self, case: Case) -> Case:
        self._ensure_schema()
        payload = self._serialize_case(case)
        with SessionLocal() as db:
            row = db.get(AetherCaseRecord, case.case_id)
            if row is None:
                row = AetherCaseRecord(case_id=case.case_id)
                db.add(row)
            row.status = case.status
            row.objective = case.objective
            row.customer_type = case.customer_type
            row.service_id = case.service_id
            row.updated_at = self._to_datetime(case.updated_at)
            row.payload = payload
            db.commit()
        return case

    def get(self, case_id: str) -> Case:
        self._ensure_schema()
        with SessionLocal() as db:
            row = db.get(AetherCaseRecord, case_id)
            if row is None:
                raise KeyError(case_id)
            return self._deserialize_case(row.payload)

    def append_event(self, case_id: str, action: str, actor: str, data: Dict[str, Any] | None = None) -> Dict[str, Any]:
        self._ensure_schema()
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "actor": actor,
            "case_id": case_id,
            "data": data or {},
        }
        with SessionLocal() as db:
            row = AetherExecutionEventRecord(
                case_id=case_id,
                action=action,
                actor=actor,
                created_at=datetime.utcnow(),
                data=entry["data"],
            )
            db.add(row)
            db.flush()
            entry["sequence"] = row.id
            db.commit()
        return entry

    def events_for(self, case_id: str) -> List[Dict[str, Any]]:
        self._ensure_schema()
        with SessionLocal() as db:
            rows = db.query(AetherExecutionEventRecord).filter(
                AetherExecutionEventRecord.case_id == case_id
            ).order_by(AetherExecutionEventRecord.id.asc()).all()
            return [
                {
                    "sequence": row.id,
                    "timestamp": row.created_at.isoformat() if row.created_at else None,
                    "action": row.action,
                    "actor": row.actor,
                    "case_id": row.case_id,
                    "data": row.data or {},
                }
                for row in rows
            ]

    @staticmethod
    def _serialize_case(case: Case) -> Dict[str, Any]:
        return {
            "case_id": case.case_id,
            "objective": case.objective,
            "customer_type": case.customer_type,
            "jurisdiction": case.jurisdiction,
            "inputs": case.inputs,
            "requirements": case.requirements,
            "status": case.status,
            "human_actions": case.human_actions,
            "exceptions": case.exceptions,
            "evidence": case.evidence,
            "outcome": case.outcome,
            "service_id": case.service_id,
            "service_name": case.service_name,
            "service_department": case.service_department,
            "service_outcome": case.service_outcome,
            "ontology": case.ontology,
            "work_graph": case.work_graph,
            "execution_events": case.execution_events,
            "created_at": case.created_at,
            "updated_at": case.updated_at,
            "tasks": {
                task_id: {
                    "definition": {
                        "id": state.definition.id,
                        "name": state.definition.name,
                        "department": state.definition.department,
                        "worker": state.definition.worker,
                        "dependencies": state.definition.dependencies,
                        "authority_required": state.definition.authority_required,
                        "physical_action": state.definition.physical_action,
                        "description": state.definition.description,
                    },
                    "status": state.status.value,
                    "result": state.result,
                    "evidence": state.evidence,
                    "error": state.error,
                    "started_at": state.started_at,
                    "completed_at": state.completed_at,
                    "attempts": state.attempts,
                    "idempotency_key": state.idempotency_key,
                }
                for task_id, state in case.tasks.items()
            },
        }

    @staticmethod
    def _deserialize_case(payload: Dict[str, Any]) -> Case:
        tasks: Dict[str, TaskState] = {}
        for task_id, raw in payload.get("tasks", {}).items():
            definition = raw["definition"]
            tasks[task_id] = TaskState(
                definition=TaskDefinition(
                    id=definition["id"],
                    name=definition["name"],
                    department=definition["department"],
                    worker=definition["worker"],
                    dependencies=definition.get("dependencies", []),
                    authority_required=definition.get("authority_required", False),
                    physical_action=definition.get("physical_action", False),
                    description=definition.get("description", ""),
                ),
                status=TaskStatus(raw.get("status", TaskStatus.PENDING.value)),
                result=raw.get("result"),
                evidence=raw.get("evidence", []),
                error=raw.get("error"),
                started_at=raw.get("started_at"),
                completed_at=raw.get("completed_at"),
                attempts=raw.get("attempts", 0),
                idempotency_key=raw.get("idempotency_key"),
            )
        return Case(
            case_id=payload["case_id"],
            objective=payload["objective"],
            customer_type=payload["customer_type"],
            jurisdiction=payload.get("jurisdiction", {}),
            inputs=payload.get("inputs", {}),
            requirements=payload.get("requirements", []),
            tasks=tasks,
            status=payload.get("status", "waiting"),
            human_actions=payload.get("human_actions", []),
            exceptions=payload.get("exceptions", []),
            evidence=payload.get("evidence", []),
            outcome=payload.get("outcome"),
            service_id=payload.get("service_id"),
            service_name=payload.get("service_name"),
            service_department=payload.get("service_department"),
            service_outcome=payload.get("service_outcome"),
            ontology=payload.get("ontology", {}),
            work_graph=payload.get("work_graph", {}),
            execution_events=payload.get("execution_events", []),
            created_at=payload.get("created_at") or datetime.utcnow().isoformat() + "Z",
            updated_at=payload.get("updated_at") or datetime.utcnow().isoformat() + "Z",
        )

    @staticmethod
    def _to_datetime(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)


InMemoryCaseStore = DatabaseCaseStore
