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



def test_citizen_can_upload_list_and_download_exact_synthetic_document(monkeypatch, tmp_path):
    """Exercise the citizen evidence path with fictional data and local test storage."""
    import hashlib

    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_ENV", "development")
    monkeypatch.setenv("AETHER_SYNTHETIC_ONLY_DOCUMENTS", "true")
    monkeypatch.setenv("AETHER_DOCUMENT_ROOT", str(tmp_path / "documents"))

    objective = "I want to open a restaurant"
    jurisdiction = {
        "country": "India",
        "state": "Jammu and Kashmir",
        "district": "Jammu",
    }
    requirements = client.post(
        "/api/aether/v2/requirements",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {},
        },
    )
    assert requirements.status_code == 200
    required_documents = requirements.json()["documents"]
    assert required_documents
    document_type = required_documents[0]

    started = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {"owner_name": "Synthetic Citizen 001"},
        },
    )
    assert started.status_code == 200
    case_id = started.json()["summary"]["case_id"]

    content = "\\n".join([
        "AETHER SYNTHETIC SAMPLE — NOT VALID FOR OFFICIAL USE",
        "THIS FILE CONTAINS FICTIONAL TEST DATA ONLY.",
        "",
        f"Document type: {document_type}",
        "Applicant: Demo Person 001 (fictional)",
        "Organisation: Example Test Enterprise (fictional)",
        "Address: 1 Example Lane, Sample Nagar, Demo State, India (fictional)",
        "Reference: AETHER-DEMO-0001",
        "Issue date: 2026-01-15 (illustrative only)",
        "Status: TEST DATA — NO LEGAL OR GOVERNMENT EFFECT",
        "",
        "No real person, business, identity number, bank account, property, or government record is represented.",
        "Do not alter this file to impersonate an official document.",
    ]).encode("utf-8")
    filename = f"AETHER-SYNTHETIC-{document_type}.txt"

    uploaded = client.post(
        f"/api/aether/v2/cases/{case_id}/documents/upload",
        params={"document_type": document_type},
        files={"file": (filename, content, "text/plain")},
    )
    assert uploaded.status_code == 200, uploaded.text
    upload_result = uploaded.json()
    assert upload_result["status"] in {"uploaded", "uploaded_and_resumed"}
    document_id = upload_result["document"]["document_id"]
    assert upload_result["document"]["sha256"] == hashlib.sha256(content).hexdigest()

    listed = client.get(f"/api/aether/v2/cases/{case_id}/documents")
    assert listed.status_code == 200, listed.text
    assert any(item["document_id"] == document_id for item in listed.json()["documents"])

    downloaded = client.get(
        f"/api/aether/v2/cases/{case_id}/documents/{document_id}/download"
    )
    assert downloaded.status_code == 200, downloaded.text
    assert downloaded.content == content
    assert downloaded.headers.get("x-document-sha256") == hashlib.sha256(content).hexdigest()


def test_citizen_upload_rejects_real_or_modified_document_in_synthetic_preview(monkeypatch):
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_ENV", "development")
    monkeypatch.setenv("AETHER_SYNTHETIC_ONLY_DOCUMENTS", "true")

    objective = "I want to open a restaurant"
    jurisdiction = {
        "country": "India",
        "state": "Jammu and Kashmir",
        "district": "Jammu",
    }
    required = client.post(
        "/api/aether/v2/requirements",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {},
        },
    ).json()["documents"]
    started = client.post(
        "/api/aether/v2/cases",
        json={
            "objective": objective,
            "customer_type": "business",
            "jurisdiction": jurisdiction,
            "inputs": {},
        },
    )
    assert started.status_code == 200
    case_id = started.json()["summary"]["case_id"]

    rejected = client.post(
        f"/api/aether/v2/cases/{case_id}/documents/upload",
        params={"document_type": required[0]},
        files={"file": ("applicant.pdf", b"%PDF-1.7 fictional", "application/pdf")},
    )
    assert rejected.status_code == 400
    assert "exact in-app generated sample file" in rejected.json()["detail"]
