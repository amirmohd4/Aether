from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_start_case_enforces_document_intake_before_execution():
    response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "developer",
            "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
            "inputs": {"documents": ["identity_document"]},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "needs_documents"
    assert body["requirements"]
    assert "identity_document" in body["documents"]
    assert body["missing_documents"]
    assert "tasks" not in body


def test_start_case_exposes_service_identity_and_execution_state():
    response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "developer",
            "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
            "inputs": {
                "documents": [
                    "identity_document", "lease_or_ownership", "business_registration",
                    "food_business_details", "site_plan", "building_plan", "floor_plan",
                    "fire_safety_details", "legal_occupancy", "parking_plan",
                    "premises_photo", "rent_deed_or_affidavit", "employer_photo", "tax_details",
                ]
            },
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["case_id"].startswith("A-")
    assert body["summary"]["service_id"] == "food_business_license"
    assert body["summary"]["service_department"] == "Food Safety"
    assert body["requirements"]
    assert "identity_check" in body["tasks"]
    assert body["tasks"]["identity_check"]["status"] == "completed"
    assert body["summary"]["status"] in {"waiting_for_human", "completed", "executing"}
