from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List
from threading import Lock
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from backend.database import SessionLocal, engine
from .domain import Case, TaskDefinition, TaskState, TaskStatus
from .persistence_models import (
    AetherCaseRecord,
    AetherExecutionEventRecord,
    AetherTaskQueueRecord,
    AetherTaskCheckpointRecord,
    AetherUsageRecord,
    AetherCaseLeaseRecord,
    AetherDocumentRecord,
    AetherNotificationRecord,
    AetherPaymentRecord,
    AetherApiKeyRecord,
)


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

            # PostgreSQL/Supabase is migration-managed. Runtime identities are
            # intentionally not granted CREATE privileges on the database/schema.
            # Never perform DDL from a request or worker process in staging/prod.
            if engine.dialect.name == "postgresql":
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    connection.commit()
                self._schema_ready = True
                return

            # SQLite is used for local development and CI, where runtime schema
            # bootstrap keeps the local developer experience self-contained.
            for model in (
                AetherCaseRecord,
                AetherExecutionEventRecord,
                AetherTaskQueueRecord,
                AetherTaskCheckpointRecord,
                AetherUsageRecord,
                AetherCaseLeaseRecord,
                AetherDocumentRecord,
                AetherNotificationRecord,
                AetherPaymentRecord,
                AetherApiKeyRecord,
            ):
                model.__table__.create(bind=engine, checkfirst=True)
            self._schema_ready = True

    def ensure_schema(self) -> None:
        self._ensure_schema()

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
            row.owner_user_id = case.owner_user_id
            row.tenant_id = case.tenant_id
            row.service_id = case.service_id
            row.updated_at = self._to_datetime(case.updated_at)
            row.payload = payload
            db.commit()
        return case

    def list(
        self,
        tenant_id: str | None = None,
        owner_user_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List durable cases with server-side ownership/tenant filtering."""
        self._ensure_schema()
        limit = max(1, min(limit, 100))
        with SessionLocal() as db:
            query = db.query(AetherCaseRecord)
            if tenant_id:
                query = query.filter(AetherCaseRecord.tenant_id == tenant_id)
            if owner_user_id:
                query = query.filter(AetherCaseRecord.owner_user_id == owner_user_id)
            if status:
                query = query.filter(AetherCaseRecord.status == status)
            rows = query.order_by(AetherCaseRecord.updated_at.desc()).limit(limit).all()
            return [
                self._deserialize_case(row.payload).summary()
                for row in rows
            ]

    def record_usage(
        self,
        tenant_id: str,
        event_type: str,
        units: int = 1,
        unit_type: str = "case",
        case_id: str | None = None,
        customer_type: str | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Record private operational/billable usage."""
        if not tenant_id:
            raise ValueError("tenant_id is required for usage metering")
        self._ensure_schema()
        with SessionLocal() as db:
            existing = None
            if case_id:
                existing = db.query(AetherUsageRecord).filter_by(
                    tenant_id=tenant_id,
                    case_id=case_id,
                    event_type=event_type,
                ).one_or_none()
            if existing is not None:
                return {
                    "id": existing.id,
                    "tenant_id": existing.tenant_id,
                    "case_id": existing.case_id,
                    "customer_type": existing.customer_type,
                    "event_type": existing.event_type,
                    "units": existing.units,
                    "unit_type": existing.unit_type,
                    "created_at": existing.created_at.isoformat(),
                    "metadata": existing.metadata_json or {},
                }

            row = AetherUsageRecord(
                tenant_id=tenant_id,
                case_id=case_id,
                customer_type=customer_type,
                event_type=event_type,
                units=max(0, int(units)),
                unit_type=unit_type,
                created_at=datetime.utcnow(),
                metadata_json=metadata or {},
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return {
                "id": row.id,
                "tenant_id": row.tenant_id,
                "case_id": row.case_id,
                "customer_type": row.customer_type,
                "event_type": row.event_type,
                "units": row.units,
                "unit_type": row.unit_type,
                "created_at": row.created_at.isoformat(),
                "metadata": row.metadata_json or {},
            }

    def usage_summary(
        self,
        tenant_id: str,
        event_type: str | None = None,
        unit_type: str | None = None,
    ) -> Dict[str, Any]:
        self._ensure_schema()
        from sqlalchemy import func
        with SessionLocal() as db:
            query = db.query(
                AetherUsageRecord.event_type,
                AetherUsageRecord.unit_type,
                func.sum(AetherUsageRecord.units).label("units"),
                func.count(AetherUsageRecord.id).label("events"),
            ).filter(AetherUsageRecord.tenant_id == tenant_id)
            if event_type:
                query = query.filter(AetherUsageRecord.event_type == event_type)
            if unit_type:
                query = query.filter(AetherUsageRecord.unit_type == unit_type)
            rows = query.group_by(
                AetherUsageRecord.event_type,
                AetherUsageRecord.unit_type,
            ).all()
            return {
                "tenant_id": tenant_id,
                "usage": [
                    {
                        "event_type": row.event_type,
                        "unit_type": row.unit_type,
                        "units": int(row.units or 0),
                        "events": int(row.events or 0),
                    }
                    for row in rows
                ],
            }

    def get(self, case_id: str) -> Case:
        self._ensure_schema()
        with SessionLocal() as db:
            row = db.get(AetherCaseRecord, case_id)
            if row is None:
                raise KeyError(case_id)
            return self._deserialize_case(row.payload)

    def put_document(self, document, owner_user_id: str | None = None) -> None:
        self._ensure_schema()
        with SessionLocal() as db:
            row = AetherDocumentRecord(
                document_id=document.document_id,
                case_id=document.case_id,
                tenant_id=document.tenant_id,
                owner_user_id=owner_user_id,
                document_type=document.document_type,
                filename=document.filename,
                mime_type=document.mime_type,
                size_bytes=document.size_bytes,
                sha256=document.sha256,
                storage_key=document.storage_key,
                extracted_text=self._protect_document_text(document.extracted_text),
                extraction_mode=document.extraction_mode,
                created_at=self._to_datetime(document.created_at),
            )
            db.add(row)
            db.commit()

    def documents_for(self, case_id: str, tenant_id: str | None = None) -> List[Dict[str, Any]]:
        self._ensure_schema()
        with SessionLocal() as db:
            query = db.query(AetherDocumentRecord).filter(AetherDocumentRecord.case_id == case_id)
            if tenant_id is not None:
                query = query.filter(AetherDocumentRecord.tenant_id == tenant_id)
            rows = query.order_by(AetherDocumentRecord.created_at.asc()).all()
            return [{
                "document_id": row.document_id,
                "case_id": row.case_id,
                "tenant_id": row.tenant_id,
                "owner_user_id": row.owner_user_id,
                "document_type": row.document_type,
                "filename": row.filename,
                "mime_type": row.mime_type,
                "size_bytes": row.size_bytes,
                "sha256": row.sha256,
                "extraction_mode": row.extraction_mode,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            } for row in rows]

    def document_texts(self, case_id: str, tenant_id: str | None = None) -> Dict[str, str]:
        """Return extracted document text to trusted workers only."""
        self._ensure_schema()
        with SessionLocal() as db:
            query = db.query(AetherDocumentRecord).filter(
                AetherDocumentRecord.case_id == case_id
            )
            if tenant_id is not None:
                query = query.filter(AetherDocumentRecord.tenant_id == tenant_id)
            rows = query.all()
            return {
                row.document_id: self._unprotect_document_text(row.extracted_text or "")
                for row in rows
                if row.extracted_text
            }

    def try_claim_case(self, case_id: str, worker_id: str, lease_seconds: int = 120) -> bool:
        """Claim a durable case lease so multiple worker processes do not execute the same case."""
        self._ensure_schema()
        now = datetime.utcnow()
        lease_until = now + timedelta(seconds=max(10, lease_seconds))
        with SessionLocal() as db:
            row = db.get(AetherCaseLeaseRecord, case_id)
            if row is None:
                row = AetherCaseLeaseRecord(
                    case_id=case_id,
                    locked_by=worker_id,
                    lease_until=lease_until,
                    heartbeat_at=now,
                )
                db.add(row)
                try:
                    db.commit()
                    return True
                except IntegrityError:
                    db.rollback()
                    return False

            if row.locked_by != worker_id and row.lease_until > now:
                return False

            row.locked_by = worker_id
            row.lease_until = lease_until
            row.heartbeat_at = now
            db.commit()
            return True

    def release_case(self, case_id: str, worker_id: str) -> None:
        self._ensure_schema()
        with SessionLocal() as db:
            row = db.get(AetherCaseLeaseRecord, case_id)
            if row and row.locked_by == worker_id:
                db.delete(row)
                db.commit()

    def heartbeat_case(self, case_id: str, worker_id: str, lease_seconds: int = 120) -> bool:
        self._ensure_schema()
        now = datetime.utcnow()
        with SessionLocal() as db:
            row = db.get(AetherCaseLeaseRecord, case_id)
            if not row or row.locked_by != worker_id:
                return False
            row.lease_until = now + timedelta(seconds=max(10, lease_seconds))
            row.heartbeat_at = now
            db.commit()
            return True

    def put_task_checkpoint(self, case_id: str, task: TaskState) -> None:
        """Persist the latest state of one task independently of the case blob.

        This prevents a worker crash between case-wide writes from losing a
        task's last durable checkpoint.
        """
        self._ensure_schema()
        with SessionLocal() as db:
            row = db.query(AetherTaskCheckpointRecord).filter_by(
                case_id=case_id,
                task_id=task.definition.id,
            ).one_or_none()
            if row is None:
                row = AetherTaskCheckpointRecord(
                    case_id=case_id,
                    task_id=task.definition.id,
                )
                db.add(row)
            row.status = task.status.value
            row.result = task.result
            row.evidence = task.evidence or []
            row.error = task.error
            row.started_at = self._to_optional_datetime(task.started_at)
            row.completed_at = self._to_optional_datetime(task.completed_at)
            row.attempts = task.attempts
            row.idempotency_key = task.idempotency_key
            row.updated_at = datetime.utcnow()
            db.commit()

    def task_checkpoints(self, case_id: str) -> Dict[str, Dict[str, Any]]:
        self._ensure_schema()
        with SessionLocal() as db:
            rows = db.query(AetherTaskCheckpointRecord).filter(
                AetherTaskCheckpointRecord.case_id == case_id
            ).all()
            return {
                row.task_id: {
                    "status": row.status,
                    "result": row.result,
                    "evidence": row.evidence or [],
                    "error": row.error,
                    "started_at": row.started_at.isoformat() if row.started_at else None,
                    "completed_at": row.completed_at.isoformat() if row.completed_at else None,
                    "attempts": row.attempts,
                    "idempotency_key": row.idempotency_key,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                }
                for row in rows
            }

    def append_event(
        self,
        case_id: str,
        action: str,
        actor: str,
        data: Dict[str, Any] | None = None,
        previous_hash: str | None = None,
        sequence: int | None = None,
        event_hash: str | None = None,
    ) -> Dict[str, Any]:
        self._ensure_schema()
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "actor": actor,
            "case_id": case_id,
            "data": data or {},
            "previous_hash": previous_hash,
            "event_hash": event_hash,
        }
        with SessionLocal() as db:
            row = AetherExecutionEventRecord(
                sequence=sequence,
                case_id=case_id,
                action=action,
                actor=actor,
                tenant_id=self._case_tenant(case_id),
                created_at=datetime.utcnow(),
                data=entry["data"],
                previous_hash=previous_hash,
                event_hash=event_hash or "",
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
                    "sequence": row.sequence if row.sequence is not None else row.id,
                    "timestamp": row.created_at.isoformat() if row.created_at else None,
                    "action": row.action,
                    "actor": row.actor,
                    "case_id": row.case_id,
                    "data": row.data or {},
                    "previous_hash": row.previous_hash,
                    "event_hash": row.event_hash,
                }
                for row in rows
            ]

    def _case_tenant(self, case_id: str) -> str | None:
        try:
            with SessionLocal() as db:
                row = db.get(AetherCaseRecord, case_id)
                return row.tenant_id if row else None
        except Exception:
            return None

    @staticmethod
    def _serialize_case(case: Case) -> Dict[str, Any]:
        return {
            "case_id": case.case_id,
            "objective": case.objective,
            "customer_type": case.customer_type,
            "owner_user_id": case.owner_user_id,
            "tenant_id": case.tenant_id,
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
            "process_profile_fingerprint": case.process_profile_fingerprint,
            "process_profile_snapshot": case.process_profile_snapshot,
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
                        "operation": state.definition.operation,
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
                    operation=definition.get("operation", ""),
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
            owner_user_id=payload.get("owner_user_id"),
            tenant_id=payload.get("tenant_id"),
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
            process_profile_fingerprint=payload.get("process_profile_fingerprint"),
            process_profile_snapshot=payload.get("process_profile_snapshot"),
            ontology=payload.get("ontology", {}),
            work_graph=payload.get("work_graph", {}),
            execution_events=payload.get("execution_events", []),
            created_at=payload.get("created_at") or datetime.utcnow().isoformat() + "Z",
            updated_at=payload.get("updated_at") or datetime.utcnow().isoformat() + "Z",
        )

    @staticmethod
    def _protect_document_text(value: str) -> str:
        from .document_crypto import encrypt_text
        return encrypt_text(value)

    @staticmethod
    def _unprotect_document_text(value: str) -> str:
        from .document_crypto import decrypt_text
        return decrypt_text(value)

    @staticmethod
    def _to_optional_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)

    @staticmethod
    def _to_datetime(value: str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)


InMemoryCaseStore = DatabaseCaseStore
