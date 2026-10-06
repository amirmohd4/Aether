from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DocumentCheck:
    document_type: str
    status: str
    extracted: Dict[str, Any]
    issues: List[str]


class DocumentIntelligence:
    """MVP document intake layer.

    This is deliberately deterministic for the demo. A production implementation
    can swap in OCR/vision/LLM extraction while keeping the same contract.
    """

    FIELD_PATTERNS = {
        "owner_name": r"(?:owner|applicant)\s*[:\-]\s*([A-Za-z .'-]+)",
        "parcel_id": r"(?:parcel|plot|survey)\s*(?:id|no)?\s*[:\-]\s*([A-Za-z0-9\-/]+)",
        "area": r"(?:area)\s*[:\-]\s*([0-9.]+)\s*(acres?|ha|sq\.?\s*ft)?",
    }

    def inspect(self, documents: List[Dict[str, Any]], required_types: List[str]) -> Dict[str, Any]:
        by_type = {d.get("type"): d for d in documents}
        checks: List[DocumentCheck] = []
        missing = []
        for required in required_types:
            doc = by_type.get(required)
            if not doc:
                missing.append(required)
                continue
            checks.append(self._inspect_one(doc))

        return {
            "status": "complete" if not missing and all(c.status == "valid" for c in checks) else "needs_attention",
            "missing": missing,
            "checks": [c.__dict__ for c in checks],
        }

    def _inspect_one(self, document: Dict[str, Any]) -> DocumentCheck:
        text = str(document.get("text", ""))
        extracted: Dict[str, Any] = {}
        issues: List[str] = []
        for field, pattern in self.FIELD_PATTERNS.items():
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
        if not text.strip():
            issues.append("Document contains no extractable text")
        return DocumentCheck(
            document_type=str(document.get("type", "unknown")),
            status="valid" if not issues else "invalid",
            extracted=extracted,
            issues=issues,
        )
