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
    assert body["execution_provenance"]["case_mode"] == "synthetic"
    assert body["execution_provenance"]["official_outcome_verified"] is False
    assert body["execution_provenance"]["task_modes"]["identity_check"] == "synthetic"
    assert body["requirements"]
    assert "identity_check" in body["tasks"]
    assert body["tasks"]["identity_check"]["status"] == "completed"
    assert body["summary"]["status"] in {"waiting_for_human", "completed", "executing"}


def test_final_document_upload_returns_resumed_execution_graph(tmp_path, monkeypatch):
    """A real uploaded file should resume the case and return its task graph."""
    from backend.aether_core import routes as v2_routes
    from backend.aether_core.document_store import DocumentStore

    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_ENV", "development")
    monkeypatch.setenv("AETHER_DOCUMENT_ROOT", str(tmp_path))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.setattr(v2_routes, "document_store", DocumentStore())

    jurisdiction = {
        "country": "India",
        "state": "Jammu and Kashmir",
        "district": "Jammu",
    }
    requirements = client.post(
        "/api/aether/v2/requirements",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {},
        },
    )
    assert requirements.status_code == 200
    required_documents = requirements.json()["documents"]
    assert len(required_documents) >= 2

    start = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {"documents": required_documents[:-1]},
        },
    )
    assert start.status_code == 200
    assert start.json()["status"] == "needs_documents"
    case_id = start.json()["summary"]["case_id"]

    upload = client.post(
        f"/api/aether/v2/cases/{case_id}/documents/upload",
        params={"document_type": required_documents[-1]},
        files={"file": ("evidence.txt", b"Synthetic test evidence", "text/plain")},
    )
    assert upload.status_code == 200
    body = upload.json()
    assert body["status"] == "uploaded_and_resumed"
    assert body["missing_documents"] == []
    assert body["case"]["summary"]["case_id"] == case_id
    assert body["case"]["tasks"]
    assert body["case"]["execution_provenance"]["case_mode"] == "synthetic"
    assert body["case"]["execution_provenance"]["official_outcome_verified"] is False
