from __future__ import annotations

from abc import ABC, abstractmethod
import os
from typing import Any, Dict

import httpx

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
            "source": response.get("source") or (response.get("result") or {}).get("source"),
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


class ConfiguredHTTPConnector(GovernmentConnector):
    """Authorized production REST adapter.

    The adapter is intentionally inert until explicitly configured. It expects
    a normalized REST contract:
      POST /requests -> {request_id, status?}
      GET  /requests/{request_id} -> {request_id, status, result?}
    Aether sends only case payloads and the stable idempotency key; credentials
    remain server-side environment configuration.
    """

    def __init__(
        self,
        department: str,
        base_url: str,
        bearer_token: str | None = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.department = department
        self.base_url = base_url.rstrip("/")
        self.bearer_token = bearer_token
        self.timeout_seconds = timeout_seconds

    def _headers(self, idempotency_key: str | None = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    def configuration_valid(self) -> bool:
        """Return whether this adapter has enough configuration to make calls safely."""
        return (
            self.base_url.startswith("https://")
            and bool(self.bearer_token)
        )

    def authenticate(self) -> Dict[str, Any]:
        # The upstream system may use a long-lived service credential or a
        # short-lived gateway token. Authentication is kept outside case logic.
        return {
            "status": "configured",
            "department": self.department,
            "base_url": self.base_url,
            "credential_present": bool(self.bearer_token),
            "configuration_valid": self.configuration_valid(),
        }

    def submit(
        self,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        body = {
            "operation": operation,
            "payload": payload,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/requests",
                json=body,
                headers=self._headers(idempotency_key),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise RuntimeError(f"Government connector submission failed for {self.department}") from exc

        request_id = data.get("request_id")
        if not request_id:
            raise RuntimeError(f"Government connector {self.department} returned no request_id")
        return {
            "request_id": request_id,
            "status": data.get("status", "submitted"),
        }

    def get_status(self, request_id: str) -> Dict[str, Any]:
        try:
            response = httpx.get(
                f"{self.base_url}/requests/{request_id}",
                headers=self._headers(),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise RuntimeError(f"Government connector status check failed for {self.department}") from exc

        return {
            "request_id": data.get("request_id", request_id),
            "status": data.get("status", "unknown"),
            "result": data.get("result") or {},
            "source": data.get("source") or f"Authorized {self.department} Connector",
        }

    def normalize(self, response: Dict[str, Any]) -> Dict[str, Any]:
        result = super().normalize(response)
        result["department"] = self.department
        result["mode"] = "production"
        return result
