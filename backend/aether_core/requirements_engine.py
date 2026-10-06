from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .templates import restaurant_requirements, property_loan_requirements


@dataclass
class RequirementDecision:
    id: str
    name: str
    status: str
    reason: str
    documents: List[str]
    jurisdiction: Dict[str, str]


class RequirementEngine:
    """MVP jurisdiction-aware requirement engine.

    Rules are intentionally explicit and auditable. It does not invent legal
    requirements; production rules will be backed by authoritative sources.
    """

    def discover(self, objective: str, customer_type: str, jurisdiction: Dict[str, str], inputs: Dict[str, Any]) -> List[RequirementDecision]:
        text = f"{objective} {customer_type}".lower()
        if "restaurant" in text or "cafe" in text or "food" in text:
            raw = restaurant_requirements()
        elif any(x in text for x in ["loan", "bank", "mortgage"]):
            raw = property_loan_requirements()
        else:
            raw = []

        decisions = []
        for req in raw:
            decisions.append(RequirementDecision(
                id=req["id"],
                name=req["name"],
                status="identified",
                reason=f"Applicable candidate for the stated objective in {jurisdiction.get('state', 'the selected jurisdiction')}",
                documents=req.get("documents", []),
                jurisdiction=jurisdiction,
            ))
        return decisions

    def document_request(self, requirements: List[RequirementDecision]) -> Dict[str, Any]:
        docs = []
        for req in requirements:
            for doc in req.documents:
                if doc not in docs:
                    docs.append(doc)
        return {"documents": docs, "count": len(docs)}
