from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_delivery_playbooks_returns_cross_department_workflows(monkeypatch):
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    response = client.get("/api/aether/v2/delivery-playbooks")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 3
    ids = {item["id"] for item in body["playbooks"]}
    assert "contractor-tender-to-payment" in ids
    assert "developer-project-readiness" in ids


def test_delivery_intelligence_unknown_case_is_not_found(monkeypatch):
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    response = client.get("/api/aether/v2/cases/NO-SUCH-CASE/delivery-intelligence")
    assert response.status_code == 404
