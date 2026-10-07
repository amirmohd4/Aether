from cryptography.fernet import Fernet

from backend.database import SessionLocal
from aether_core.case_store import DatabaseCaseStore
from aether_core.document_store import DocumentStore
from aether_core.notifications import NotificationService
from aether_core.persistence_models import AetherDocumentRecord
from aether_core.engine import AetherExecutionEngine
from aether_core.worker_runtime import AetherWorkerRuntime
from aether_core.marketplace import marketplace_catalog
from aether_core.service_registry import ServiceRegistry


def test_document_text_is_encrypted_at_rest_and_decrypted_for_trusted_workers(tmp_path, monkeypatch):
    monkeypatch.setenv("AETHER_DOCUMENT_ROOT", str(tmp_path))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    monkeypatch.setenv("AETHER_ENCRYPTION_KEY", Fernet.generate_key().decode())

    content = b"owner: Confidential Owner\nparcel: P-123\narea: 2.5 acres"
    document = DocumentStore().save(
        "case-security",
        "tenant-security",
        "property_record",
        "record.txt",
        content,
        "text/plain",
    )

    store = DatabaseCaseStore()
    store.put_document(document, owner_user_id="user-security")

    with SessionLocal() as db:
        row = db.get(AetherDocumentRecord, document.document_id)
        assert row is not None
        assert row.extracted_text != document.extracted_text
        assert "Confidential Owner" not in row.extracted_text

    texts = store.document_texts("case-security", "tenant-security")
    assert texts[document.document_id] == document.extracted_text


def test_notification_enqueue_is_idempotent_and_in_app_dispatches():
    service = NotificationService(SessionLocal)
    first = service.enqueue(
        "tenant-notify-hardening",
        "user-1",
        "case-notify-hardening",
        "case.started",
        idempotency_key="case-notify-hardening:started",
    )
    second = service.enqueue(
        "tenant-notify-hardening",
        "user-1",
        "case-notify-hardening",
        "case.started",
        idempotency_key="case-notify-hardening:started",
    )
    assert first["id"] == second["id"]

    result = service.dispatch_queued()
    assert result["delivered"] >= 1

    rows = service.list_for_tenant(
        "tenant-notify-hardening",
        "case-notify-hardening",
    )
    assert rows[0]["status"] == "sent"
    assert rows[0]["attempts"] >= 1


def test_worker_runtime_uses_a_durable_case_lease():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document", "business_registration"]},
        owner_user_id="worker-user",
        tenant_id="worker-tenant",
    )
    store = engine.store
    assert store.try_claim_case(case.case_id, "worker-a", lease_seconds=120) is True
    assert store.try_claim_case(case.case_id, "worker-b", lease_seconds=120) is False
    store.release_case(case.case_id, "worker-a")
    assert store.try_claim_case(case.case_id, "worker-b", lease_seconds=120) is True
    store.release_case(case.case_id, "worker-b")


def test_worker_runtime_processes_cases_and_notification_outbox():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document", "business_registration"]},
        owner_user_id="runtime-user",
        tenant_id="runtime-tenant",
    )
    runtime = AetherWorkerRuntime(engine)
    result = runtime.run_once()
    assert result["count"] >= 1
    assert result["notifications"]["remaining"] >= 0


def test_marketplace_exposes_all_mvp_services_as_sandbox_contracts():
    catalog = marketplace_catalog(ServiceRegistry())
    assert catalog["count"] == 34
    assert all(item["sandbox"] is True for item in catalog["apis"])
    assert all(item["live_connector_required"] is True for item in catalog["apis"])



def test_document_store_rejects_mismatched_binary_signature(tmp_path, monkeypatch):
    from aether_core.document_store import DocumentStore

    monkeypatch.setenv("AETHER_DOCUMENT_ROOT", str(tmp_path))
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)

    try:
        DocumentStore().save(
            "case-signature",
            "tenant-signature",
            "passport_document",
            'bad"\nname.pdf',
            b"not a pdf",
            "application/pdf",
        )
    except ValueError as exc:
        assert "signature" in str(exc).lower()
    else:
        raise AssertionError("mismatched PDF signature must be rejected")
