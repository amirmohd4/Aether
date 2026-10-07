from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .templates import restaurant_requirements, property_loan_requirements


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

    A requirement is never treated as authoritative merely because a model
    inferred it. Production rules must carry an authoritative source and
    version/effective-date information before Aether can auto-submit regulated work.
    """

    def discover(self, objective: str, customer_type: str, jurisdiction: Dict[str, str], inputs: Dict[str, Any]) -> List[RequirementDecision]:
        text = f"{objective} {customer_type}".lower()
        if "restaurant" in text or "cafe" in text or "food" in text:
            raw = restaurant_requirements()
        elif any(x in text for x in ["loan", "bank", "mortgage"]):
            raw = property_loan_requirements()
        else:
            raw = []

        decisions: List[RequirementDecision] = []
        for req in raw:
            if not self._jurisdiction_matches(req, jurisdiction):
                continue
            decisions.append(RequirementDecision(
                id=req["id"], name=req["name"], status="identified",
                reason=req.get("reason", f"Candidate requirement for {jurisdiction.get('state', 'the selected jurisdiction')}"),
                documents=req.get("documents", []), jurisdiction=jurisdiction,
                source=req.get("source"), source_title=req.get("source_title"),
                effective_date=req.get("effective_date"), verified_at=req.get("verified_at"),
                confidence=req.get("confidence", "mvp"),
            ))
        return decisions

    @staticmethod
    def _jurisdiction_matches(req: Dict[str, Any], jurisdiction: Dict[str, str]) -> bool:
        allowed = req.get("states")
        return not allowed or jurisdiction.get("state") in allowed

    def document_request(self, requirements: List[RequirementDecision]) -> Dict[str, Any]:
        docs = []
        for req in requirements:
            for doc in req.documents:
                if doc not in docs:
                    docs.append(doc)
        return {"documents": docs, "count": len(docs)}
