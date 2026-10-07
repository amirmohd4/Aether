from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .service_registry import ServiceRegistry
from .templates import generic_requirements, property_loan_requirements, restaurant_requirements


@dataclass
class RequirementDecision:
    id: str
    name: str
    status: str
    reason: str
    documents: List[str]
    jurisdiction: Dict[str, str]
    source: Optional[str] = None
    source_title: Optional[str] = None
    effective_date: Optional[str] = None
    verified_at: Optional[str] = None
    confidence: str = "mvp"


class RequirementEngine:
    """Auditable jurisdiction-aware requirement discovery.

    Source-backed rules are explicit. Unverified service metadata is treated as
    a baseline candidate and must not be mistaken for authoritative law.
    """

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()

    def discover(
        self,
        objective: str,
        customer_type: str,
        jurisdiction: Dict[str, str],
        inputs: Dict[str, Any],
    ) -> List[RequirementDecision]:
        service = self.registry.resolve(objective, customer_type)
        text = f"{objective} {customer_type}".lower()

        if "restaurant" in text or "cafe" in text or "food business" in text:
            raw = restaurant_requirements()
        elif any(x in text for x in ["loan", "bank", "mortgage", "property verification"]) and service:
            raw = property_loan_requirements()
        elif service:
            raw = generic_requirements(service)
        else:
            raw = [{
                "id": "objective_clarification",
                "name": "Objective clarification",
                "documents": [],
                "reason": "Aether could not map the objective to a known MVP service. Clarification is required before downstream execution.",
                "confidence": "needs-clarification",
            }]

        decisions: List[RequirementDecision] = []
        for req in raw:
            if not self._jurisdiction_matches(req, jurisdiction):
                continue
            decisions.append(RequirementDecision(
                id=req["id"],
                name=req["name"],
                status="identified",
                reason=req.get("reason", f"Candidate requirement for {jurisdiction.get('state', 'the selected jurisdiction')}"),
                documents=req.get("documents", []),
                jurisdiction=jurisdiction,
                source=req.get("source"),
                source_title=req.get("source_title"),
                effective_date=req.get("effective_date"),
                verified_at=req.get("verified_at"),
                confidence=req.get("confidence", "mvp"),
            ))
        return decisions

    @staticmethod
    def _jurisdiction_matches(req: Dict[str, Any], jurisdiction: Dict[str, str]) -> bool:
        allowed = req.get("states")
        return not allowed or jurisdiction.get("state") in allowed

    def document_request(self, requirements: List[RequirementDecision]) -> Dict[str, Any]:
        docs: List[str] = []
        for req in requirements:
            for doc in req.documents:
                if doc not in docs:
                    docs.append(doc)
        return {"documents": docs, "count": len(docs)}
