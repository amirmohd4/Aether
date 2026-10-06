from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_start_case_exposes_real_execution_state():
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
    assert body["summary"]["case_id"].startswith("CASE-")
    assert body["requirements"]
    assert "identity_check" in body["tasks"]
    assert body["tasks"]["identity_check"]["status"] == "completed"
    assert body["summary"]["status"] in {"waiting_human", "completed", "executing"}
