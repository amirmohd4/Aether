from fastapi.testclient import TestClient

from main import app


def test_v2_api_can_start_case_and_return_human_boundary():
    client = TestClient(app)
    response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "business",
            "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
            "inputs": {"owner_name": "Demo Owner", "parcel_id": "P-001", "area": 2.0},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["status"] == "waiting_for_human"
    assert body["tasks"]["inspection"]["status"] == "human_review"
    assert body["tasks"]["final_approval"]["status"] == "blocked"
