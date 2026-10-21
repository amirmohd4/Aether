from backend.aether_core.delivery_intelligence import assess_delivery_risks


def test_flags_over_budget_and_commitments():
    result = assess_delivery_risks({"budget": 100, "committed_cost": 120, "forecast_cost": 115})
    codes = {finding["code"] for finding in result["findings"]}
    assert "forecast_over_budget" in codes
    assert "commitments_exceed_budget" in codes
    assert result["summary"]["progress_blocker_count"] == 2


def test_missing_budget_is_unknown_not_safe():
    result = assess_delivery_risks({"forecast_cost": 500})
    codes = {finding["code"] for finding in result["findings"]}
    assert "budget_unknown" in codes
    assert result["mode"] == "advisory"


def test_flags_schedule_slip_and_unresolved_permit():
    result = assess_delivery_risks({"planned_finish": "2026-10-01", "forecast_finish": "2026-11-15", "permits": [{"name": "Building permit", "status": "pending"}]})
    codes = {finding["code"] for finding in result["findings"]}
    assert "forecast_schedule_slip" in codes
    assert "permit_not_cleared" in codes


def test_flags_payment_claim_without_evidence():
    result = assess_delivery_risks({"payment_claims": [{"amount": "25000", "evidence_complete": False}]})
    assert any(finding["code"] == "payment_claim_evidence_incomplete" for finding in result["findings"])


def test_empty_input_returns_clear_limitations_not_compliance_claim():
    result = assess_delivery_risks({})
    codes = {finding["code"] for finding in result["findings"]}
    assert "budget_unknown" in codes
    assert "forecast_unknown" in codes
    assert "not proof" in result["limitations"][-1]
