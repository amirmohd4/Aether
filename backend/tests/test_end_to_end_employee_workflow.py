"""End-to-end proof for citizen intake -> employee operations -> authorised outcome.

This test uses only fictional data and Aether's deterministic synthetic environment.
It is intentionally not a judicial/JusticeOS test and does not claim a live
government integration or real-world staff-time savings.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from main import app


BASE = "/api/aether/v2"


def _restaurant_payload():
    return {
        "objective": "I want to open a restaurant",
        "customer_type": "business",
        "jurisdiction": {
            "country": "India",
            "state": "Jammu and Kashmir",
            "district": "Jammu",
        },
        "inputs": {
            "owner_name": "Synthetic E2E Applicant",
            "parcel_id": "E2E-RESTAURANT-001",
            "area": 2.0,
            "documents": [
                "identity_document",
                "lease_or_ownership",
                "business_registration",
                "food_business_details",
                "site_plan",
                "building_plan",
                "floor_plan",
                "fire_safety_details",
                "legal_occupancy",
                "parking_plan",
                "premises_photo",
                "rent_deed_or_affidavit",
                "employer_photo",
                "tax_details",
            ],
        },
    }


def test_citizen_to_employee_processing_to_authorised_synthetic_outcome(monkeypatch):
    """Prove the engine does internal work and stops at authority boundaries."""
    monkeypatch.setenv("AETHER_ENV", "development")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    client = TestClient(app)

    created = client.post(f"{BASE}/cases", json=_restaurant_payload())
    assert created.status_code == 200, created.text
    body = created.json()
    case_id = body["summary"]["case_id"]
    assert body["summary"]["service_id"]
    assert body["tasks"]

    # EmployeeOS must actually execute repeatable internal work, not merely
    # create a citizen-facing application record.
    for task_id in (
        "internal_case_triage",
        "internal_case_file",
        "internal_data_normalization",
        "internal_correspondence",
        "internal_followup_plan",
    ):
        assert task_id in body["tasks"], f"missing internal employee task: {task_id}"
        assert body["tasks"][task_id]["status"] == "completed", (
            f"internal employee task did not execute: {task_id} "
            f"({body['tasks'][task_id]['status']})"
        )

    # The officer brief must expose both completed automation and work that
    # legitimately needs a human/physical action.
    brief_response = client.get(f"{BASE}/cases/{case_id}/operator-brief")
    assert brief_response.status_code == 200, brief_response.text
    brief = brief_response.json()
    assert brief["summary"]["automated_completed"] > 0
    assert brief["summary"]["human_or_physical_total"] > 0
    assert brief["process"]["execution_coverage"]

    # Only synthetic approvals are used here. Each authority boundary is
    # explicitly approved through the normal API; Aether must not self-approve.
    approved = []
    for _ in range(12):
        pending = [
            task_id for task_id, task in body["tasks"].items()
            if task["status"] == "human_review"
        ]
        if not pending:
            break
        task_id = pending[0]
        decision = client.post(
            f"{BASE}/cases/{case_id}/human/{task_id}",
            json={"approved": True, "note": "Synthetic E2E approval only; not an official decision."},
        )
        assert decision.status_code == 200, decision.text
        body = decision.json()
        assert body["tasks"][task_id]["status"] == "completed"
        approved.append(task_id)

    assert approved, "workflow should pause for at least one authorised human boundary"
    assert body["summary"]["status"] == "completed", {
        "status": body["summary"]["status"],
        "remaining_human": body["summary"]["human_actions"],
        "exceptions": body["summary"]["exceptions"],
        "pending": {
            task_id: task["status"]
            for task_id, task in body["tasks"].items()
            if task["status"] != "completed"
        },
    }
    assert body["outcome"]["status"] == "completed"
    assert all(task["status"] == "completed" for task in body["tasks"].values())

    events_response = client.get(f"{BASE}/cases/{case_id}/events")
    assert events_response.status_code == 200, events_response.text
    actions = [event["action"] for event in events_response.json()["events"]]
    assert "human_action.requested" in actions
    assert "human_action.approved" in actions
    assert "case.completed" in actions

    audit_response = client.get(f"{BASE}/cases/{case_id}/audit")
    assert audit_response.status_code == 200, audit_response.text
    assert audit_response.json()["integrity"], "case audit chain did not verify"
