from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Any, Dict, List

from .service_registry import ServiceDefinition, ServiceRegistry


@dataclass(frozen=True)
class UnderstandingResult:
    normalized_objective: str
    service_id: str | None
    service_name: str | None
    confidence: float
    matched_keywords: List[str]
    ambiguous: bool
    missing_context: List[str]
    customer_type: str
    jurisdiction: Dict[str, str]

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ObjectiveUnderstandingEngine:
    """Deterministic MVP objective-to-service understanding.

    This is intentionally model-independent. A future LLM/router can propose
    candidates, but the final service selection remains auditable and bounded.
    """

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()

    def understand(
        self,
        objective: str,
        customer_type: str = "business",
        jurisdiction: Dict[str, str] | None = None,
    ) -> UnderstandingResult:
        normalized = re.sub(r"\s+", " ", objective.strip().lower())
        service, score, matches, margin = self.registry.resolve_with_score(
            normalized, customer_type
        )
        confidence = min(0.99, 0.45 + 0.18 * score + 0.12 * max(margin, 0))
        ambiguous = service is None or (score > 0 and margin <= 0)
        missing: List[str] = []
        if not customer_type:
            missing.append("customer_type")
        if not jurisdiction or not jurisdiction.get("country"):
            missing.append("jurisdiction.country")
        if service is None:
            missing.append("specific government service or objective")

        return UnderstandingResult(
            normalized_objective=normalized,
            service_id=service.id if service else None,
            service_name=service.name if service else None,
            confidence=confidence if service else 0.0,
            matched_keywords=matches,
            ambiguous=ambiguous,
            missing_context=missing,
            customer_type=customer_type,
            jurisdiction=jurisdiction or {},
        )
