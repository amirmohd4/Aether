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
