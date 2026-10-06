from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .synthetic_government import SyntheticGovernmentSystem


class GovernmentConnector(ABC):
    """Stable connector contract for authorised government integrations."""

    @abstractmethod
    def submit(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_status(self, request_id: str) -> Dict[str, Any]:
        raise NotImplementedError


class SyntheticConnector(GovernmentConnector):
    def __init__(self, department: str):
        self.department = department
        self.system = SyntheticGovernmentSystem()

    def submit(self, operation: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        request_id = self.system.submit(self.department, operation, payload)
        return {"request_id": request_id, "status": self.system.status(request_id)}

    def get_status(self, request_id: str) -> Dict[str, Any]:
        status = self.system.status(request_id)
        result = self.system.result(request_id) if status == "completed" else None
        return {"request_id": request_id, "status": status, "result": result}
