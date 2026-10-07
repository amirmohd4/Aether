from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .synthetic_government import SyntheticGovernmentSystem


class GovernmentConnector(ABC):
    """Stable contract shared by synthetic and authorised production adapters."""

    def authenticate(self) -> Dict[str, Any]:
        return {"status": "not_required"}

    @abstractmethod
    def submit(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_status(self, request_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_result(self, request_id: str) -> Dict[str, Any]:
        response = self.get_status(request_id)
        return response.get("result") or {}

    def normalize(self, response: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "request_id": response.get("request_id"),
            "status": response.get("status"),
            "result": response.get("result"),
            "source": response.get("source"),
        }

    def retry(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        return self.execute(operation, payload, idempotency_key)

    def execute(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        submitted = self.submit(operation, payload, idempotency_key)
        status = self.get_status(submitted["request_id"])
        return self.normalize(status)


class SyntheticConnector(GovernmentConnector):
    def __init__(
        self,
        department: str,
        system: SyntheticGovernmentSystem | None = None,
    ):
        self.department = department
        self.system = system or SyntheticGovernmentSystem()
        self._requests: Dict[str, str] = {}

    def submit(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        if idempotency_key and idempotency_key in self._requests:
            request_id = self._requests[idempotency_key]
        else:
            request_id = self.system.submit(
                self.department,
                operation,
                payload,
                idempotency_key=idempotency_key,
            )
            if idempotency_key:
                self._requests[idempotency_key] = request_id
        return {"request_id": request_id, "status": self.system.status(request_id)}

    def execute(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        result = self.system.execute(
            self.department,
            operation,
            payload,
            idempotency_key=idempotency_key,
        )
        result["result"] = result.get("result") or {}
        result["result"].setdefault("source", f"Synthetic {self.department} System")
        return self.normalize(result)

    def get_status(self, request_id: str) -> Dict[str, Any]:
        status = self.system.status(request_id)
        result = self.system.result(request_id) if status == "completed" else None
        return {
            "request_id": request_id,
            "status": status,
            "result": result,
            "source": f"Synthetic {self.department} System",
        }

    def get_result(self, request_id: str) -> Dict[str, Any]:
        return self.system.result(request_id)

    def normalize(self, response: Dict[str, Any]) -> Dict[str, Any]:
        result = super().normalize(response)
        result["department"] = self.department
        return result
