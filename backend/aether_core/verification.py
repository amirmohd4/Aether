from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass(frozen=True)
class VerificationFinding:
    code: str
    severity: str
    status: str
    message: str
    evidence: Dict[str, Any] | None = None


@dataclass(frozen=True)
class VerificationResult:
    status: str
    risk_level: str
    findings: List[VerificationFinding]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "risk_level": self.risk_level,
            "findings": [asdict(item) for item in self.findings],
        }


class VerificationEngine:
    """Deterministic evidence and risk checks for the MVP.

    This engine does not make the statutory decision. It determines whether
    Aether has consistent evidence and whether an exception should cross the
    human-authority boundary.
    """

    def verify_result(
        self,
        task_id: str,
        result: Dict[str, Any],
        required_documents: List[str] | None = None,
        submitted_documents: List[str] | None = None,
    ) -> VerificationResult:
        findings: List[VerificationFinding] = []
        submitted = set(submitted_documents or [])
        required = set(required_documents or [])

        missing = sorted(required - submitted)
        if missing:
            findings.append(VerificationFinding(
                code="DOC-MISSING",
                severity="high",
                status="fail",
                message="Required evidence is missing from the case intake.",
                evidence={"missing_documents": missing},
            ))

        if result.get("verified") is False or result.get("validated") is False:
            findings.append(VerificationFinding(
                code="SOURCE-UNVERIFIED",
                severity="high",
                status="fail",
                message=f"Source result for {task_id} was not verified.",
            ))

        if result.get("active_cases", 0) > 0:
            findings.append(VerificationFinding(
                code="LEGAL-ACTIVE-CASE",
                severity="high",
                status="exception",
                message="An active court case was returned by the simulated source.",
                evidence={"active_cases": result.get("active_cases")},
            ))

        if result.get("dues", 0) > 0:
            findings.append(VerificationFinding(
                code="DUES-OUTSTANDING",
                severity="medium",
                status="exception",
                message="Outstanding dues were returned by the simulated source.",
                evidence={"dues": result.get("dues")},
            ))

        risk = "low"
        status = "verified"
        if any(f.severity == "high" for f in findings):
            risk, status = "high", "exception"
        elif findings:
            risk, status = "medium", "exception"

        return VerificationResult(status=status, risk_level=risk, findings=findings)

    def reconcile(
        self,
        results: Dict[str, Dict[str, Any]],
    ) -> VerificationResult:
        findings: List[VerificationFinding] = []
        areas = {
            key: value.get("area")
            for key, value in results.items()
            if value.get("area") is not None
        }
        if len(set(areas.values())) > 1:
            findings.append(VerificationFinding(
                code="RECORD-CONFLICT",
                severity="high",
                status="exception",
                message="Government records disagree on a material property field.",
                evidence=areas,
            ))

        statuses = [value.get("status") for value in results.values()]
        if "rejected" in statuses:
            findings.append(VerificationFinding(
                code="SOURCE-REJECTED",
                severity="high",
                status="exception",
                message="At least one government source rejected an operation.",
            ))

        if not findings:
            return VerificationResult("verified", "low", [])
        risk = "high" if any(f.severity == "high" for f in findings) else "medium"
        return VerificationResult("exception", risk, findings)
