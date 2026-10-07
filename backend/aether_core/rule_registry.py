from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass(frozen=True)
class RuleRecord:
    rule_id: str
    title: str
    jurisdiction: Dict[str, str]
    requirement: str
    authority_status: str
    source_url: Optional[str] = None
    source_title: Optional[str] = None
    verified_at: Optional[str] = None
    effective_date: Optional[str] = None
    notes: str = ""

    def as_dict(self) -> Dict:
        return asdict(self)


# Only rules for which Aether currently carries an explicit source reference
# are marked source_backed. The remaining service catalog is deliberately not
# presented as an authoritative legal rulebook.
SOURCE_BACKED_RULES = [
    RuleRecord(
        rule_id="JK-FOOD-001",
        title="Food business licensing/registration",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        requirement="food_business_details",
        authority_status="source_backed",
        source_url="https://www.fssai.gov.in/business/licensing",
        source_title="FSSAI — Business Licensing",
        verified_at="2026-10-07",
        notes="Source reference used for the restaurant MVP requirement gate.",
    ),
    RuleRecord(
        rule_id="JK-FIRE-001",
        title="Fire provisional NOC inputs",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        requirement="fire_safety_details",
        authority_status="source_backed",
        source_url="https://singlewindow.jk.gov.in/assets/services/procedurechecklist/12/procedurechecklist_file_0721931001649670909.pdf",
        source_title="J&K Fire & Emergency Services — Provisional NOC checklist",
        verified_at="2026-10-07",
        notes="Source reference used for the restaurant MVP requirement gate.",
    ),
    RuleRecord(
        rule_id="JK-MUNI-001",
        title="Commercial-establishment municipal inputs",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        requirement="municipal_commercial_establishment",
        authority_status="source_backed",
        source_url="https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=16810006",
        source_title="J&K municipal commercial-establishment service",
        verified_at="2026-10-07",
        notes="Source reference used for the restaurant MVP requirement gate.",
    ),
    RuleRecord(
        rule_id="JK-LAB-001",
        title="Shops & Establishments registration inputs",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        requirement="shops_establishment_registration",
        authority_status="source_backed",
        source_url="https://singlewindow.jk.gov.in/assets/services/sop_file/8/sop_file_0304369001648350632.pdf",
        source_title="J&K Labour & Employment — Shops & Establishments registration",
        verified_at="2026-10-07",
        notes="Source reference used for the restaurant MVP requirement gate.",
    ),
]


class RuleRegistry:
    """Versionable rule/provenance registry.

    A rule is not treated as law merely because it exists in service metadata.
    Production execution should require an authoritative source and effective
    dates where applicable.
    """

    def __init__(self, records: List[RuleRecord] | None = None):
        self._records = records or SOURCE_BACKED_RULES

    def for_jurisdiction(self, jurisdiction: Dict[str, str]) -> List[RuleRecord]:
        return [
            record
            for record in self._records
            if all(
                jurisdiction.get(key) == value
                for key, value in record.jurisdiction.items()
            )
        ]

    def for_requirement(
        self,
        requirement: str,
        jurisdiction: Dict[str, str] | None = None,
    ) -> List[RuleRecord]:
        records = [r for r in self._records if r.requirement == requirement]
        if not jurisdiction:
            return records
        return [
            r for r in records
            if all(jurisdiction.get(k) == v for k, v in r.jurisdiction.items())
        ]

    def all(self) -> List[Dict]:
        return [record.as_dict() for record in self._records]
