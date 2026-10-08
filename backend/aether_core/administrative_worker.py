from __future__ import annotations

from typing import Any, Dict

from .notifications import NotificationService
from backend.database import SessionLocal


class AdministrativeWorker:
    """Automates repetitive internal case-administration work.

    The worker never makes a statutory decision. It prepares and executes
    administrative operations that normally require staff coordination.
    """

    name = "AdministrativeWorker"

    def execute(self, context) -> Dict[str, Any]:
        operation = context.operation
        if operation == "case_triage":
            return self._triage(context)
        if operation == "case_file_assembly":
            return self._file_assembly(context)
        if operation == "data_normalization":
            return self._normalize(context)
        if operation == "correspondence":
            return self._correspondence(context)
        if operation == "followup_plan":
            return self._followup(context)
        if operation == "case_closeout":
            return self._closeout(context)
        return {
            "request_id": f"ADMIN-{context.case_id}-{operation}",
            "status": "completed",
            "result": {
                "operation": operation,
                "completed": True,
                "source": "Aether Administrative Worker",
            },
        }

    @staticmethod
    def _triage(context) -> Dict[str, Any]:
        payload = context.payload
        objective = str(payload.get("objective") or "")
        customer_type = str(payload.get("customer_type") or "unknown")
        jurisdiction = payload.get("jurisdiction") or {}
        priority = "high" if any(
            token in objective.lower()
            for token in ("urgent", "deadline", "renewal", "inspection", "appeal")
        ) else "normal"
        return {
            "request_id": f"ADMIN-{context.case_id}-TRIAGE",
            "status": "completed",
            "result": {
                "operation": "case_triage",
                "priority": priority,
                "customer_type": customer_type,
                "jurisdiction": jurisdiction,
                "routing": {
                    "department": context.department,
                    "case_owner": payload.get("owner_user_id"),
                },
                "risk_flags": [],
                "source": "Aether Administrative Worker",
            },
        }

    @staticmethod
    def _file_assembly(context) -> Dict[str, Any]:
        payload = context.payload
        documents = payload.get("documents") or []
        required = payload.get("required_documents") or []
        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in documents
        }
        checklist = [
            {
                "document_type": document,
                "status": "received" if document in submitted else "missing",
            }
            for document in required
        ]
        return {
            "request_id": f"ADMIN-{context.case_id}-FILE",
            "status": "completed",
            "result": {
                "operation": "case_file_assembly",
                "case_file_ready": True,
                "document_checklist": checklist,
                "received_documents": len(submitted),
                "missing_documents": [item["document_type"] for item in checklist if item["status"] == "missing"],
                "source": "Aether Administrative Worker",
            },
        }

    @staticmethod
    def _normalize(context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        normalized: Dict[str, Any] = {}
        for key in ("owner_name", "company_id", "property_id", "parcel_id", "project_id"):
            if payload.get(key) is not None:
                normalized[key] = payload[key]
        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            for key in ("registration_id", "certificate_reference", "search_id", "record_reference"):
                if result.get(key) is not None:
                    normalized[key] = result[key]

        return {
            "request_id": f"ADMIN-{context.case_id}-NORMALIZE",
            "status": "completed",
            "result": {
                "operation": "data_normalization",
                "normalized_fields": normalized,
                "field_count": len(normalized),
                "source": "Aether Administrative Worker",
            },
        }

    def _correspondence(self, context) -> Dict[str, Any]:
        payload = context.payload
        results = payload.get("task_results") or {}
        required = payload.get("required_documents") or []
        documents = payload.get("documents") or []
        submitted = {
            str(item.get("type")) if isinstance(item, dict) else str(item)
            for item in documents
        }
        missing = [doc for doc in required if doc not in submitted]
        query_results = [
            task_id for task_id, result in results.items()
            if isinstance(result, dict) and (
                result.get("status") == "query" or result.get("query")
            )
        ]

        drafts = []
        if missing:
            drafts.append({
                "type": "missing_documents",
                "subject": "Additional documents required",
                "message": "Please provide: " + ", ".join(missing),
            })
        if query_results:
            drafts.append({
                "type": "government_query",
                "subject": "Government query requires review",
                "message": "Review the query returned for: " + ", ".join(sorted(query_results)),
            })
        if not drafts:
            drafts.append({
                "type": "progress_update",
                "subject": "Case processing update",
                "message": "Aether has completed the current administrative processing stage.",
            })

        notification_ids = []
        service = NotificationService(SessionLocal)
        tenant_id = payload.get("tenant_id")
        user_id = payload.get("owner_user_id")
        for index, draft in enumerate(drafts):
            item = service.enqueue(
                tenant_id=tenant_id,
                user_id=user_id,
                case_id=context.case_id,
                event_type="case.correspondence.prepared",
                channel="in_app",
                payload=draft,
                idempotency_key=f"{context.case_id}:correspondence:{index}:{draft['type']}",
            )
            notification_ids.append(item["id"])

        return {
            "request_id": f"ADMIN-{context.case_id}-CORRESPONDENCE",
            "status": "completed",
            "result": {
                "operation": "correspondence",
                "drafts": drafts,
                "notification_ids": notification_ids,
                "source": "Aether Administrative Worker",
            },
        }

    def _followup(self, context) -> Dict[str, Any]:
        results = context.payload.get("task_results") or {}
        pending = []
        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            if result.get("status") == "query" or result.get("needs_attention"):
                pending.append(task_id)

        return {
            "request_id": f"ADMIN-{context.case_id}-FOLLOWUP",
            "status": "completed",
            "result": {
                "operation": "followup_plan",
                "pending_followups": sorted(pending),
                "automatic_followup_enabled": True,
                "source": "Aether Administrative Worker",
            },
        }

    @staticmethod
    def _closeout(context) -> Dict[str, Any]:
        results = context.payload.get("task_results") or {}
        references = []
        for task_id, result in results.items():
            if isinstance(result, dict):
                ref = result.get("reference") or result.get("certificate_reference") or result.get("record_reference")
                if ref:
                    references.append({"task_id": task_id, "reference": ref})
        return {
            "request_id": f"ADMIN-{context.case_id}-CLOSEOUT",
            "status": "completed",
            "result": {
                "operation": "case_closeout",
                "case_file_references": references,
                "administrative_closeout_complete": True,
                "source": "Aether Administrative Worker",
            },
        }
