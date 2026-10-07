from pathlib import Path

import pytest

from aether_core.connector_registry import ConnectorRegistry
from aether_core.connectors import ConfiguredHTTPConnector
from aether_core.rule_packs import RulePackValidationError, load_rule_pack, validate_rule_pack


def test_example_rule_pack_validates_as_non_authoritative():
    pack = load_rule_pack(
        Path("configs/rules/jk-restaurant-onboarding.example.json")
    )
    assert pack.pack_id == "jk-restaurant-onboarding-example"
    assert pack.version == "0.1.0"
    assert pack.production_ready is False
    assert len(pack.rules) == 2


def test_source_backed_rule_pack_requires_effective_dates_and_sources():
    payload = {
        "pack_id": "jk-production",
        "version": "1.0.0",
        "jurisdiction": {"country": "India", "state": "Jammu and Kashmir"},
        "authority_status": "source_backed",
        "source_document": "AUTHORIZED-SOURCE",
        "verified_at": "2026-10-07",
        "effective_from": "2026-10-01",
        "rules": [
            {
                "rule_id": "RULE-001",
                "title": "Authorized rule",
                "service_id": "passport",
                "requirement": "identity_document",
                "authority_status": "source_backed",
                "source_url": "https://gov.example/rule-001",
                "source_title": "Authorized Rule 001",
                "verified_at": "2026-10-07",
                "effective_date": "2026-10-01",
            }
        ],
    }
    pack = validate_rule_pack(payload)
    assert pack.production_ready is True


def test_source_backed_rule_pack_requires_service_binding():
    payload = {
        "pack_id": "missing-service-pack",
        "version": "1.0.0",
        "jurisdiction": {"country": "India"},
        "authority_status": "source_backed",
        "source_document": "AUTHORIZED-SOURCE",
        "verified_at": "2026-10-07",
        "effective_from": "2026-10-01",
        "rules": [
            {
                "rule_id": "RULE-001",
                "title": "Missing service binding",
                "requirement": "identity_document",
                "authority_status": "source_backed",
                "source_url": "https://gov.example/rule-001",
                "source_title": "Authorized Rule 001",
                "verified_at": "2026-10-07",
                "effective_date": "2026-10-01",
            }
        ],
    }
    with pytest.raises(RulePackValidationError, match="service_id"):
        validate_rule_pack(payload)


def test_source_backed_rule_pack_rejects_missing_effective_date():
    payload = {
        "pack_id": "invalid-pack",
        "version": "1.0.0",
        "jurisdiction": {"country": "India"},
        "authority_status": "source_backed",
        "source_document": "AUTHORIZED-SOURCE",
        "verified_at": "2026-10-07",
        "effective_from": "2026-10-01",
        "rules": [
            {
                "rule_id": "RULE-001",
                "title": "Missing effective date",
                "service_id": "passport",
                "requirement": "identity_document",
                "authority_status": "source_backed",
                "source_url": "https://gov.example/rule-001",
                "source_title": "Authorized Rule 001",
                "verified_at": "2026-10-07",
            }
        ],
    }
    with pytest.raises(RulePackValidationError, match="effective_date"):
        validate_rule_pack(payload)


def test_rule_pack_rejects_duplicate_rule_ids():
    payload = {
        "pack_id": "duplicate-pack",
        "version": "1.0.0",
        "jurisdiction": {"country": "India"},
        "authority_status": "registry_baseline",
        "rules": [
            {
                "rule_id": "DUPLICATE",
                "title": "One",
                "requirement": "identity_document",
                "authority_status": "registry_baseline",
            },
            {
                "rule_id": "DUPLICATE",
                "title": "Two",
                "requirement": "address_proof",
                "authority_status": "registry_baseline",
            },
        ],
    }
    with pytest.raises(RulePackValidationError, match="duplicate rule_id"):
        validate_rule_pack(payload)


def test_production_connector_requires_https_and_bearer_token(monkeypatch):
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "true")
    monkeypatch.setenv(
        "AETHER_PRODUCTION_CONNECTORS",
        '{"Land Records": {"base_url": "https://sandbox.gov.example"}}',
    )
    with pytest.raises(RuntimeError, match="bearer_token"):
        ConnectorRegistry()


def test_configured_http_connector_configuration_validation():
    valid = ConfiguredHTTPConnector(
        department="Land Records",
        base_url="https://sandbox.gov.example",
        bearer_token="sandbox-token",
    )
    assert valid.configuration_valid() is True
    assert valid.authenticate()["credential_present"] is True

    invalid_scheme = ConfiguredHTTPConnector(
        department="Land Records",
        base_url="http://sandbox.gov.example",
        bearer_token="sandbox-token",
    )
    assert invalid_scheme.configuration_valid() is False

    invalid_credential = ConfiguredHTTPConnector(
        department="Land Records",
        base_url="https://sandbox.gov.example",
        bearer_token=None,
    )
    assert invalid_credential.configuration_valid() is False
