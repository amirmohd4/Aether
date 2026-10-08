from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .connector_registry import ConnectorRegistry
from .connectors import GovernmentConnector
from .synthetic_government import SyntheticGovernmentSystem
from .document_intelligence import DocumentIntelligence
from .administrative_worker import AdministrativeWorker


@dataclass
class WorkerContext:
    case_id: str
    department: str
    operation: str
    payload: Dict[str, Any]


class DigitalWorker:
    name = "DigitalWorker"

    def __init__(
        self,
        government: SyntheticGovernmentSystem | None = None,
        connectors: ConnectorRegistry | None = None,
    ):
        self.connectors = connectors or ConnectorRegistry(government)

    def connector(self, department: str) -> GovernmentConnector:
        return self.connectors.get(department)

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        return self.connector(context.department).execute(
            context.operation,
            context.payload,
            context.payload.get("idempotency_key"),
        )


class DocumentWorker(DigitalWorker):
    name = "DocumentWorker"

    def __init__(self, government=None, connectors=None):
        super().__init__(government, connectors)
        self.intelligence = DocumentIntelligence()

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        documents = context.payload.get("documents") or []
        required = context.payload.get("required_documents") or []

        # The demo UI supplies document references (for example, "identity_document")
        # rather than file bytes/text. Keep those references valid in synthetic mode,
        # while real document payloads use the same deterministic extraction contract.
        if documents and all(isinstance(item, str) for item in documents):
            missing = sorted(set(required) - set(documents))
            inspection = {
                "mode": "reference_only_demo",
                "status": "complete" if not missing else "needs_attention",
                "missing": missing,
                "checks": [
                    {
                        "document_type": item,
                        "status": "valid" if item in set(documents) else "invalid",
                        "extracted": {},
                        "issues": [],
                    }
                    for item in documents
                ],
            }
        else:
            extractions = context.payload.get("document_extractions") or {}
            normalized = []
            for item in documents:
                record = dict(item) if isinstance(item, dict) else {"type": str(item)}
                if not record.get("text") and record.get("document_id"):
                    record["text"] = extractions.get(record["document_id"], "")
                normalized.append(record)
            inspection = self.intelligence.inspect(normalized, required)

        return {
            "request_id": f"DOC-{context.case_id}",
            "status": "completed",
            "result": {
                "documents_received": bool(documents),
                "documents_validated": inspection["status"] == "complete",
                "document_inspection": inspection,
                "document_count": len(documents),
                "source": "Aether Document Intelligence",
            },
        }


class ReconciliationWorker(DigitalWorker):
    name = "ReconciliationWorker"

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        results = context.payload.get("task_results") or {}
        findings = []
        comparable_fields = ("area", "owner", "parcel_id", "registration_id")
        for field in comparable_fields:
            values = {
                task_id: result.get(field)
                for task_id, result in results.items()
                if isinstance(result, dict) and result.get(field) is not None
            }
            unique = {str(value) for value in values.values()}
            if len(unique) > 1:
                findings.append({
                    "code": f"RECORD-CONFLICT-{field.upper()}",
                    "severity": "high",
                    "field": field,
                    "values": values,
                })

        for task_id, result in results.items():
            if not isinstance(result, dict):
                continue
            if result.get("verified") is False or result.get("validated") is False:
                findings.append({
                    "code": "UNVERIFIED-SOURCE",
                    "severity": "high",
                    "task_id": task_id,
                })
            if result.get("status") in {"rejected", "query"}:
                findings.append({
                    "code": f"SOURCE-{str(result.get('status')).upper()}",
                    "severity": "high",
                    "task_id": task_id,
                })

        return {
            "request_id": f"RECON-{context.case_id}",
            "status": "completed",
            "result": {
                "reconciled": not findings,
                "findings": findings,
                "source_tasks": sorted(results.keys()),
                "source": "Aether Verification Engine",
            },
        }


class DecisionWorker(DigitalWorker):
    name = "DecisionWorker"

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        results = context.payload.get("task_results") or {}
        case_exceptions = context.payload.get("case_exceptions") or []
        evidence = []
        for task_id, result in results.items():
            if isinstance(result, dict):
                evidence.append({
                    "task_id": task_id,
                    "source": result.get("source", "Aether"),
                    "verified": result.get("verified", result.get("validated", True)),
                    "reference": result.get("reference") or result.get("registration_id") or result.get("certificate_reference"),
                })
        return {
            "request_id": f"DECISION-{context.case_id}",
            "status": "completed",
            "result": {
                "evidence_complete": bool(evidence),
                "evidence_count": len(evidence),
                "evidence": evidence,
                "exceptions_present": bool(case_exceptions),
                "exception_count": len(case_exceptions),
                "service_id": context.payload.get("service_id"),
                "service_outcome": context.payload.get("service_outcome"),
                "source": "Aether Decision Package Engine",
            },
        }


class OutcomeWorker(DigitalWorker):
    name = "OutcomeWorker"

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        outcome = context.payload.get("service_outcome") or "service_outcome"
        return {
            "request_id": f"OUTCOME-{context.case_id}",
            "status": "completed",
            "result": {
                "completed": True,
                "outcome": outcome,
                "outcome_reference": f"AETHER-{context.case_id}",
                "source": "Aether Outcome Engine",
            },
        }


class HumanAuthorityWorker(DigitalWorker):
    name = "HumanAuthorityWorker"


class WorkerRegistry:
    def __init__(
        self,
        government: SyntheticGovernmentSystem | None = None,
        connectors: ConnectorRegistry | None = None,
    ):
        self._connectors = connectors or ConnectorRegistry(government)
        self._workers: Dict[str, DigitalWorker] = {
            "DocumentWorker": DocumentWorker(government, self._connectors),
            "ReconciliationWorker": ReconciliationWorker(government, self._connectors),
            "DecisionWorker": DecisionWorker(government, self._connectors),
            "OutcomeWorker": OutcomeWorker(government, self._connectors),
            "HumanAuthorityWorker": HumanAuthorityWorker(government, self._connectors),
            "AdministrativeWorker": AdministrativeWorker(),
        }
        self._government = government

    def get(self, name: str) -> DigitalWorker:
        if name not in self._workers:
            self._workers[name] = DigitalWorker(self._government, self._connectors)
        return self._workers[name]

    def connector_catalog(self) -> list[dict]:
        return self._connectors.catalog()

    def production_connectors_configured(self) -> bool:
        return self._connectors.production_configured()

    def production_connector(self, department: str) -> bool:
        return self._connectors.is_production(department)
