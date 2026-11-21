import pytest
from fastapi import HTTPException

from aether_core.routes import _validate_synthetic_document_upload


def _fixture(document_type: str = "identity_document") -> tuple[str, bytes]:
    safe_type = document_type
    filename = f"AETHER-SYNTHETIC-{safe_type}.txt"
    body = "\n".join([
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
    return filename, body


def test_synthetic_only_upload_accepts_exact_generated_fixture(monkeypatch):
    monkeypatch.setenv("AETHER_SYNTHETIC_ONLY_DOCUMENTS", "true")
    filename, content = _fixture()
    assert _validate_synthetic_document_upload(
        "identity_document", filename, "text/plain", content
    ) is None


@pytest.mark.parametrize(
    "filename,mime_type,content",
    [
        ("identity_document.pdf", "application/pdf", b"%PDF-1.7 fake"),
        ("AETHER-SYNTHETIC-identity_document.txt", "text/plain", b"Real applicant details"),
        ("AETHER-SYNTHETIC-identity_document.txt", "text/plain", b"AETHER SYNTHETIC SAMPLE"),
    ],
)
def test_synthetic_only_upload_rejects_non_fixture_documents(
    monkeypatch, filename, mime_type, content
):
    monkeypatch.setenv("AETHER_SYNTHETIC_ONLY_DOCUMENTS", "true")
    with pytest.raises(HTTPException) as error:
        _validate_synthetic_document_upload(
            "identity_document", filename, mime_type, content
        )
    assert error.value.status_code == 400


def test_synthetic_upload_guard_is_opt_in_for_non_preview_environments(monkeypatch):
    monkeypatch.setenv("AETHER_SYNTHETIC_ONLY_DOCUMENTS", "false")
    assert _validate_synthetic_document_upload(
        "identity_document", "any-file.txt", "text/plain", b"test"
    ) is None
