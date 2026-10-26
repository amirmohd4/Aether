"""API-level end-to-end coverage for Aether's controlled synthetic workflow.

This test deliberately uses synthetic data and the no-auth test mode. It does
not contact a government service or represent an official decision.
"""
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_workflow_runs_from_objective_to_authorized_decision_and_audit(monkeypatch):
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_ENV", "development")

    objective = "I want to open a restaurant"
    jurisdiction = {
        "country": "India",
        "state": "Jammu and Kashmir",
        "district": "Jammu",
    }

    requirements_response = client.post(
        "/api/aether/v2/requirements",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {},
        },
    )
    assert requirements_response.status_code == 200
    required_documents = requirements_response.json()["documents"]
    assert required_documents

    start_response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {
                "owner_name": "Synthetic Test Owner",
                "parcel_id": "SYNTHETIC-PARCEL-001",
                "area": 2.0,
                "documents": required_documents,
            },
        },
    )
    assert start_response.status_code == 200
    case = start_response.json()
    case_id = case["summary"]["case_id"]

    assert case["execution_provenance"]["case_mode"] == "synthetic"
    assert case["execution_provenance"]["official_outcome_verified"] is False
    assert case["summary"]["status"] == "waiting_for_human"
    assert case["tasks"]["inspection"]["status"] == "human_review"
    assert case["tasks"]["final_approval"]["status"] in {"pending", "blocked"}

    audit_before = client.get(f"/api/aether/v2/cases/{case_id}/audit")
    assert audit_before.status_code == 200
    assert audit_before.json()["integrity"]["valid"] is True
    assert audit_before.json()["integrity"]["checked_events"] > 0

    inspection_response = client.post(
        f"/api/aether/v2/cases/{case_id}/human/inspection",
        json={"approved": True, "note": "Synthetic inspection test completed"},
    )
    assert inspection_response.status_code == 200
    after_inspection = inspection_response.json()
    assert after_inspection["tasks"]["inspection"]["status"] == "completed"
    assert after_inspection["summary"]["status"] == "waiting_for_human"
    assert after_inspection["tasks"]["final_approval"]["status"] == "human_review"

    approval_response = client.post(
        f"/api/aether/v2/cases/{case_id}/human/final_approval",
        json={"approved": True, "note": "Synthetic authorized-officer test decision"},
    )
    assert approval_response.status_code == 200
    completed = approval_response.json()

    assert completed["summary"]["status"] == "completed"
    assert completed["tasks"]["record_update"]["status"] == "completed"
    assert completed["tasks"]["certificate"]["status"] == "completed"
    # Even a simulated human action must never be represented as an official
    # government result or an external system-of-record confirmation.
    assert completed["execution_provenance"]["case_mode"] == "synthetic"
    assert completed["execution_provenance"]["official_outcome_verified"] is False

    audit_after = client.get(f"/api/aether/v2/cases/{case_id}/audit")
    assert audit_after.status_code == 200
    assert audit_after.json()["integrity"]["valid"] is True
    assert audit_after.json()["integrity"]["checked_events"] >= audit_before.json()["integrity"]["checked_events"]
