from aether_core.verification import VerificationEngine


def test_verification_flags_missing_documents():
    result = VerificationEngine().verify_result(
        "document_intake",
        {"validated": True},
        ["identity_document", "property_record"],
        ["identity_document"],
    )
    assert result.status == "exception"
    assert result.risk_level == "high"
    assert any(f.code == "DOC-MISSING" for f in result.findings)


def test_reconciliation_flags_material_record_conflict():
    result = VerificationEngine().reconcile({
        "land_record": {"area": 10},
        "registration_record": {"area": 9.5},
    })
    assert result.status == "exception"
    assert result.risk_level == "high"
    assert any(f.code == "RECORD-CONFLICT" for f in result.findings)


def test_clean_results_are_verified():
    result = VerificationEngine().reconcile({
        "land_record": {"area": 10},
        "registration_record": {"area": 10},
        "court_search": {"active_cases": 0},
    })
    assert result.status == "verified"
    assert result.risk_level == "low"
    assert result.findings == []


def test_audit_chain_links_events():
    from aether_core.audit import AuditTrail

    audit = AuditTrail()
    first = audit.record("case.created", "aether", "CASE-A", {"value": 1})
    second = audit.record("task.completed", "worker", "CASE-A", {"value": 2})

    assert first["previous_hash"] is None
    assert first["event_hash"]
    assert second["previous_hash"] == first["event_hash"]
    assert second["event_hash"] != first["event_hash"]

    other_case = audit.record("case.created", "aether", "CASE-B", {})
    assert other_case["previous_hash"] is None
