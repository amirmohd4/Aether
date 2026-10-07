from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .connector_registry import ConnectorRegistry
from .connectors import GovernmentConnector
from .synthetic_government import SyntheticGovernmentSystem


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

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        return {
            "request_id": f"DOC-{context.case_id}",
            "status": "completed",
            "result": {
                "documents_received": bool(context.payload.get("documents")),
                "documents_validated": True,
                "extracted_fields": list(context.payload.keys()),
                "source": "Aether Document Intelligence",
            },
        }


class ReconciliationWorker(DigitalWorker):
    name = "ReconciliationWorker"


class OutcomeWorker(DigitalWorker):
    name = "OutcomeWorker"


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
            "OutcomeWorker": OutcomeWorker(government, self._connectors),
            "HumanAuthorityWorker": HumanAuthorityWorker(government, self._connectors),
        }
        self._government = government

    def get(self, name: str) -> DigitalWorker:
        if name not in self._workers:
            self._workers[name] = DigitalWorker(self._government, self._connectors)
        return self._workers[name]

    def connector_catalog(self) -> list[dict]:
        return self._connectors.catalog()
