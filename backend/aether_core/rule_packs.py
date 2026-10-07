from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List


class RulePackValidationError(ValueError):
    """Raised when an external Aether rule pack is malformed or unsafe."""


@dataclass(frozen=True)
class RulePack:
    pack_id: str
    version: str
    jurisdiction: Dict[str, str]
    authority_status: str
    source_document: str | None
    verified_at: str | None
    effective_from: str | None
    rules: List[Dict[str, Any]]

    @property
    def production_ready(self) -> bool:
        if self.authority_status != "source_backed":
            return False
        if not self.source_document or not self.verified_at or not self.effective_from:
            return False
        return all(_rule_is_authoritative(rule) for rule in self.rules)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "pack_id": self.pack_id,
            "version": self.version,
            "jurisdiction": dict(self.jurisdiction),
            "authority_status": self.authority_status,
            "source_document": self.source_document,
            "verified_at": self.verified_at,
            "effective_from": self.effective_from,
            "production_ready": self.production_ready,
            "rules": list(self.rules),
        }


def _valid_iso_date(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RulePackValidationError(f"{field} must be a non-empty ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise RulePackValidationError(f"{field} must use YYYY-MM-DD") from exc
    return value


def _rule_is_authoritative(rule: Dict[str, Any]) -> bool:
    return (
        rule.get("authority_status") == "source_backed"
        and bool(rule.get("source_url"))
        and bool(rule.get("source_title"))
        and bool(rule.get("verified_at"))
        and bool(rule.get("effective_date"))
    )


def validate_rule_pack(payload: Dict[str, Any]) -> RulePack:
    if not isinstance(payload, dict):
        raise RulePackValidationError("rule pack must be a JSON object")

    pack_id = payload.get("pack_id")
    version = payload.get("version")
    if not isinstance(pack_id, str) or not pack_id.strip():
        raise RulePackValidationError("pack_id is required")
    if not isinstance(version, str) or not version.strip():
        raise RulePackValidationError("version is required")

    jurisdiction = payload.get("jurisdiction") or {}
    if not isinstance(jurisdiction, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in jurisdiction.items()
    ):
        raise RulePackValidationError("jurisdiction must be an object of strings")

    authority_status = str(payload.get("authority_status") or "registry_baseline")
    if authority_status not in {"source_backed", "registry_baseline"}:
        raise RulePackValidationError("unsupported authority_status")

    source_document = payload.get("source_document")
    verified_at = payload.get("verified_at")
    effective_from = payload.get("effective_from")

    if authority_status == "source_backed":
        if not source_document:
            raise RulePackValidationError("source_document is required for source_backed packs")
        verified_at = _valid_iso_date(verified_at, "verified_at")
        effective_from = _valid_iso_date(effective_from, "effective_from")

    rules = payload.get("rules")
    if not isinstance(rules, list) or not rules:
        raise RulePackValidationError("rules must be a non-empty array")

    normalized_rules: List[Dict[str, Any]] = []
    seen_rule_ids: set[str] = set()

    for index, raw_rule in enumerate(rules):
        if not isinstance(raw_rule, dict):
            raise RulePackValidationError(f"rule[{index}] must be an object")
        rule = dict(raw_rule)
        rule_id = rule.get("rule_id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise RulePackValidationError(f"rule[{index}].rule_id is required")
        if rule_id in seen_rule_ids:
            raise RulePackValidationError(f"duplicate rule_id: {rule_id}")
        seen_rule_ids.add(rule_id)

        for required in ("title", "requirement", "authority_status"):
            if not isinstance(rule.get(required), str) or not rule[required].strip():
                raise RulePackValidationError(f"rule[{index}].{required} is required")

        if rule["authority_status"] not in {"source_backed", "registry_baseline"}:
            raise RulePackValidationError(f"rule[{index}] has unsupported authority_status")

        if rule["authority_status"] == "source_backed":
            if not rule.get("service_id"):
                raise RulePackValidationError(
                    f"rule[{index}] source_backed rules require service_id"
                )
            if not rule.get("source_url") or not rule.get("source_title"):
                raise RulePackValidationError(
                    f"rule[{index}] source_backed rules require source_url and source_title"
                )
            rule["verified_at"] = _valid_iso_date(rule.get("verified_at"), f"rule[{index}].verified_at")
            rule["effective_date"] = _valid_iso_date(
                rule.get("effective_date"), f"rule[{index}].effective_date"
            )

        rule.setdefault("jurisdiction", dict(jurisdiction))
        normalized_rules.append(rule)

    return RulePack(
        pack_id=pack_id.strip(),
        version=version.strip(),
        jurisdiction=dict(jurisdiction),
        authority_status=authority_status,
        source_document=str(source_document) if source_document else None,
        verified_at=str(verified_at) if verified_at else None,
        effective_from=str(effective_from) if effective_from else None,
        rules=normalized_rules,
    )


def load_rule_pack(path: str | os.PathLike[str]) -> RulePack:
    file_path = Path(path)
    if not file_path.is_file():
        raise RulePackValidationError(f"rule pack file not found: {file_path}")
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RulePackValidationError("rule pack must contain valid JSON") from exc
    return validate_rule_pack(payload)


def load_rule_pack_from_environment() -> RulePack | None:
    path = os.getenv("AETHER_RULE_PACK_PATH", "").strip()
    if not path:
        return None
    return load_rule_pack(path)


def rule_pack_records(pack: RulePack) -> Iterable[Dict[str, Any]]:
    for rule in pack.rules:
        record = dict(rule)
        record.setdefault("jurisdiction", dict(pack.jurisdiction))
        record.setdefault("verified_at", pack.verified_at)
        record.setdefault("effective_date", pack.effective_from)
        record.setdefault("authority_status", pack.authority_status)
        yield record
