from fastapi.testclient import TestClient

from main import app


def test_v2_me_returns_server_resolved_identity():
    client = TestClient(app)
    response = client.get("/api/aether/v2/me")
    assert response.status_code == 200
    body = response.json()
    assert body["subject"] == "demo"
    assert body["role"] == "demo"
    assert body["auth_mode"] == "none"


def test_v2_api_can_start_case_and_return_human_boundary():
    client = TestClient(app)
    response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "business",
            "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
            "inputs": {
                "owner_name": "Demo Owner",
                "parcel_id": "P-001",
                "area": 2.0,
                "documents": [
                    "identity_document", "lease_or_ownership", "business_registration",
                    "food_business_details", "site_plan", "building_plan", "floor_plan",
                    "fire_safety_details", "legal_occupancy", "parking_plan",
                    "premises_photo", "rent_deed_or_affidavit", "employer_photo", "tax_details",
                ],
            },
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["status"] == "waiting_for_human"
    assert body["tasks"]["inspection"]["status"] == "human_review"
    assert body["tasks"]["final_approval"]["status"] == "pending"


def test_missing_documents_create_durable_case_then_resume_after_upload():
    client = TestClient(app)
    response = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I need a title verification for a property loan",
            "customer_type": "bank",
            "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
            "inputs": {
                "documents": ["identity_document", "property_record"],
                "parcel_id": "P-900",
            },
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "needs_documents"
    case_id = body["summary"]["case_id"]
    assert "loan_application" in body["missing_documents"]

    response = client.post(
        f"/api/aether/v2/cases/{case_id}/documents",
        json={"documents": ["loan_application"]},
    )
    assert response.status_code == 200
    resumed = response.json()
    assert resumed["summary"]["case_id"] == case_id
    assert resumed["summary"]["tasks_total"] > 0



def test_upload_payment_analytics_and_notifications_mvp_surfaces(tmp_path, monkeypatch):
    monkeypatch.setenv("AETHER_DOCUMENT_ROOT", str(tmp_path))
    client = TestClient(app)

    create = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": "I want to open a restaurant",
            "customer_type": "business",
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
    assert create.status_code == 200
    case_id = create.json()["summary"]["case_id"]

    upload = client.post(
        f"/api/aether/v2/cases/{case_id}/documents/upload",
        params={"document_type": "identity_document"},
        files={"file": ("identity.txt", b"owner: Demo Owner\nparcel: P-100\narea: 2 acres", "text/plain")},
    )
    assert upload.status_code == 200
    body = upload.json()
    assert body["document"]["document_type"] == "identity_document"
    assert body["document"]["size_bytes"] > 0
    assert body["document"]["extraction_mode"] == "native-text"

    docs = client.get(f"/api/aether/v2/cases/{case_id}/documents")
    assert docs.status_code == 200
    assert docs.json()["documents"]

    payment = client.post(
        f"/api/aether/v2/cases/{case_id}/payments",
        params={"amount_minor": 1000, "currency": "INR", "idempotency_key": "PAY-CASE-1"},
    )
    assert payment.status_code == 200
    payment_again = client.post(
        f"/api/aether/v2/cases/{case_id}/payments",
        params={"amount_minor": 1000, "currency": "INR", "idempotency_key": "PAY-CASE-1"},
    )
    assert payment_again.status_code == 200
    assert payment_again.json()["payment_id"] == payment.json()["payment_id"]

    notifications = client.get("/api/aether/v2/notifications")
    assert notifications.status_code == 200
    assert notifications.json()["notifications"]

    analytics = client.get("/api/aether/v2/analytics")
    assert analytics.status_code == 200
    assert analytics.json()["case_count"] >= 1
