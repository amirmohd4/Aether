from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .synthetic_government import SyntheticGovernmentSystem


@dataclass
class WorkerContext:
    case_id: str
    department: str
    operation: str
    payload: Dict[str, Any]


class DigitalWorker:
    name = "DigitalWorker"

    def __init__(self, government: SyntheticGovernmentSystem):
        self.government = government

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        return self.government.execute(context.department, context.operation, context.payload)


class DocumentWorker(DigitalWorker):
    name = "DocumentWorker"

    def execute(self, context: WorkerContext) -> Dict[str, Any]:
        return {
            "request_id": f"DOC-{context.case_id}",
            "status": "completed",
            "result": {
                "documents_received": True,
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
    def __init__(self, government: SyntheticGovernmentSystem):
        self._workers = {
            "DocumentWorker": DocumentWorker(government),
            "ReconciliationWorker": ReconciliationWorker(government),
            "OutcomeWorker": OutcomeWorker(government),
            "HumanAuthorityWorker": HumanAuthorityWorker(government),
        }
        self._government = government

    def get(self, name: str) -> DigitalWorker:
        if name not in self._workers:
            self._workers[name] = DigitalWorker(self._government)
        return self._workers[name]
