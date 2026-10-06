from __future__ import annotations

from typing import Any, Dict, List


class RuleEngine:
    """Auditable MVP rule layer. Every decision carries its rule id and source label."""

    def check(self, objective: str, jurisdiction: Dict[str, str], extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
        rules = []
        state = jurisdiction.get("state", "unknown")
        text = objective.lower()
        if any(x in text for x in ["restaurant", "cafe", "food"]):
            rules.extend([
                {"rule_id": "REST-DOC-001", "status": "candidate", "requirement": "food_business_details", "source": f"jurisdiction rule set: {state}"},
                {"rule_id": "REST-FIRE-001", "status": "candidate", "requirement": "fire_safety_evidence", "source": f"jurisdiction rule set: {state}"},
                {"rule_id": "REST-PREM-001", "status": "candidate", "requirement": "premises_evidence", "source": f"jurisdiction rule set: {state}"},
            ])
        return rules
