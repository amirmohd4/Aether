from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List
import json
import os


@dataclass(frozen=True)
class JurisdictionProcessProfile:
    service_id: str
    country: str
    state: str | None = None
    district: str | None = None
    authority: str | None = None
    receiving_portal: str | None = None
    official_form_reference: str | None = None
    source_url: str | None = None
    effective_date: str | None = None
    verified_at: str | None = None
    steps: List[Dict[str, Any]] = field(default_factory=list)
    required_documents: List[str] = field(default_factory=list)
    service_level: Dict[str, Any] = field(default_factory=dict)
    authority_matrix: List[Dict[str, Any]] = field(default_factory=list)

    def matches(self, jurisdiction: Dict[str, str]) -> bool:
        if self.country and self.country.lower() != str(jurisdiction.get("country", "")).lower():
            return False
        if self.state and self.state.lower() != str(jurisdiction.get("state", "")).lower():
            return False
        if self.district and self.district.lower() != str(jurisdiction.get("district", "")).lower():
            return False
        return True


class JurisdictionProcessRegistry:
    """Source-backed process-profile registry.

    Profiles may be loaded from JSON so exact State/UT/district implementations
    can be added without changing the execution engine.
    """

    def __init__(self, profiles: List[JurisdictionProcessProfile] | None = None):
        self._profiles = profiles or []
        path = os.getenv("AETHER_PROCESS_PROFILE_PATH", "").strip()
        if path:
            self._profiles.extend(self._load(Path(path)))

    @staticmethod
    def _load(path: Path) -> List[JurisdictionProcessProfile]:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("profiles") or []
        if not isinstance(data, list):
            raise ValueError("Process profile JSON must contain a profiles list")
        return [
            JurisdictionProcessProfile(
                service_id=str(item["service_id"]),
                country=str(item.get("country", "India")),
                state=item.get("state"),
                district=item.get("district"),
                authority=item.get("authority"),
                receiving_portal=item.get("receiving_portal"),
                official_form_reference=item.get("official_form_reference"),
                source_url=item.get("source_url"),
                effective_date=item.get("effective_date"),
                verified_at=item.get("verified_at"),
                steps=list(item.get("steps") or []),
                required_documents=[str(x) for x in item.get("required_documents") or []],
                service_level=dict(item.get("service_level") or {}),
                authority_matrix=list(item.get("authority_matrix") or []),
            )
            for item in data
            if isinstance(item, dict) and item.get("service_id")
        ]

    def add(self, profile: JurisdictionProcessProfile) -> None:
        self._profiles.append(profile)

    def resolve(self, service_id: str, jurisdiction: Dict[str, str]) -> JurisdictionProcessProfile | None:
        candidates = [
            profile for profile in self._profiles
            if profile.service_id == service_id and profile.matches(jurisdiction)
        ]
        if not candidates:
            return None

        def specificity(profile: JurisdictionProcessProfile) -> int:
            return int(bool(profile.state)) + int(bool(profile.district))

        return max(candidates, key=specificity)

    def all(self) -> List[JurisdictionProcessProfile]:
        return list(self._profiles)

    def readiness(self, service_id: str, jurisdiction: Dict[str, str]) -> Dict[str, Any]:
        profile = self.resolve(service_id, jurisdiction)
        if not profile:
            return {
                "status": "missing",
                "service_id": service_id,
                "jurisdiction": jurisdiction,
                "reason": "No jurisdiction-specific process profile is loaded.",
            }
        verified = bool(profile.source_url and profile.effective_date and profile.verified_at)
        return {
            "status": "ready" if verified else "incomplete",
            "service_id": service_id,
            "jurisdiction": jurisdiction,
            "authority": profile.authority,
            "receiving_portal": profile.receiving_portal,
            "source_url": profile.source_url,
            "effective_date": profile.effective_date,
            "verified_at": profile.verified_at,
            "steps": profile.steps,
            "required_documents": profile.required_documents,
            "authority_matrix": profile.authority_matrix,
            "service_level": profile.service_level,
        }
