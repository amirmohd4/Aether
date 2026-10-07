from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict, List


@dataclass
class SyntheticRequest:
    request_id: str
    department: str
    operation: str
    payload: Dict[str, Any]
    status: str = "completed"
    result: Dict[str, Any] | None = None
    attempts: int = 0


class SyntheticGovernmentSystem:
    """Deterministic government-system simulator used by the MVP.

    It deliberately exposes the same request/status/result shape that a real
    authorized connector will use later. No real government system is touched.
    """

    def __init__(self) -> None:
        self._requests: Dict[str, SyntheticRequest] = {}
        self._idempotency: Dict[str, str] = {}
        self._failure_once_seen: set[str] = set()

    def submit(
        self,
        department: str,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> str:
        if idempotency_key and idempotency_key in self._idempotency:
            return self._idempotency[idempotency_key]

        seed = f"{department}|{operation}|{idempotency_key or len(self._requests) + 1}"
        request_id = f"SIM-{sha256(seed.encode()).hexdigest()[:12].upper()}"
        result = self._build_result(department, operation, payload)
        request = SyntheticRequest(
            request_id=request_id,
            department=department,
            operation=operation,
            payload=dict(payload),
            result=result,
        )
        self._requests[request_id] = request
        if idempotency_key:
            self._idempotency[idempotency_key] = request_id
        return request_id

    def status(self, request_id: str) -> str:
        request = self._requests.get(request_id)
        if not request:
            raise KeyError(request_id)
        return request.status

    def result(self, request_id: str) -> Dict[str, Any]:
        request = self._requests.get(request_id)
        if not request:
            raise KeyError(request_id)
        return dict(request.result or {})

    def execute(
        self,
        department: str,
        operation: str,
        payload: Dict[str, Any],
        idempotency_key: str | None = None,
    ) -> Dict[str, Any]:
        key = idempotency_key or f"auto:{department}:{operation}:{len(self._requests)}"
        if payload.get("simulate_failure_once") and key not in self._failure_once_seen:
            self._failure_once_seen.add(key)
            raise RuntimeError(f"Simulated transient failure for {department}/{operation}")

        request_id = self.submit(department, operation, payload, key)
        if payload.get("simulate_query") and operation not in {"document", "identity"}:
            result = self.result(request_id)
            result["query"] = "Simulated government query: additional evidence requested."
            result["status"] = "query"
            return {"request_id": request_id, "status": "query", "result": result}

        if payload.get("simulate_rejection"):
            result = self.result(request_id)
            result["decision"] = "rejected"
            result["reason"] = "Simulated rejection for demo/testing."
            result["status"] = "rejected"
            return {"request_id": request_id, "status": "rejected", "result": result}

        return {
            "request_id": request_id,
            "status": self.status(request_id),
            "result": self.result(request_id),
        }

    def _build_result(
        self,
        department: str,
        operation: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        source = f"Synthetic {department} System"
        result: Dict[str, Any] = {
            "source": source,
            "department": department,
            "operation": operation,
            "jurisdiction": payload.get("jurisdiction", {}),
        }

        defaults = {
            "identity": {"verified": True, "match_score": 0.99},
            "land_record": {
                "verified": True,
                "parcel_id": payload.get("parcel_id", "P-001"),
                "area": payload.get("land_area", 2.0),
                "owner": payload.get("owner_name", "Demo Applicant"),
            },
            "registration_record": {
                "verified": True,
                "registration_id": payload.get("registration_id", "REG-001"),
                "area": payload.get("registration_area", payload.get("land_area", 2.0)),
            },
            "court_search": {
                "verified": True,
                "active_cases": payload.get("active_cases", 0),
                "search_id": "COURT-SIM-001",
            },
            "tax_dues": {
                "verified": True,
                "dues": float(payload.get("tax_dues", 0)),
            },
            "zoning": {"verified": True, "permitted_use": payload.get("permitted_use", "commercial")},
            "business": {"verified": True, "business_status": "active"},
            "food": {"received": True, "licence_case": "FSSAI-SIM-001"},
            "fire": {"received": True, "noc_case": "FIRE-SIM-001"},
            "municipal": {"received": True, "case": "MUNI-SIM-001"},
            "building": {"received": True, "case": "BUILD-SIM-001"},
            "environment": {"received": True, "case": "ENV-SIM-001"},
            "rera": {"received": True, "case": "RERA-SIM-001"},
            "utility": {"received": True, "case": "UTILITY-SIM-001"},
            "inspection": {
                "status": "human_required",
                "physical_action": True,
                "message": "Physical inspection is outside Aether's autonomous boundary.",
            },
            "document": {
                "documents_received": bool(payload.get("documents")),
                "document_count": len(payload.get("documents", [])),
                "validated": True,
            },
            "reconciliation": {"status": "reconciled", "conflicts": []},
            "decision_package": {"evidence_complete": True},
            "record_update": {"updated": True, "record_reference": "SIM-REC-001"},
            "certificate": {"issued": True, "certificate_reference": "SIM-CERT-001"},
            "outcome": {"completed": True, "outcome_reference": "SIM-OUTCOME-001"},
        }
        result.update(defaults.get(operation, {
            "processed": True,
            "status": "completed",
            "reference": f"SIM-{operation.upper()}-001",
        }))
        return result
