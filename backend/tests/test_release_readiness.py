from cryptography.fernet import Fernet

from backend.aether_core import routes


def _configure_controlled_release(monkeypatch):
    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("DATABASE_URL", "postgresql://runtime:example@localhost:5432/aether")
    monkeypatch.setenv("AETHER_AUTH_MODE", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "test-only-service-key")
    monkeypatch.setenv("AETHER_ENCRYPTION_KEY", Fernet.generate_key().decode("ascii"))
    monkeypatch.setenv("AETHER_ENABLE_LEGACY_API", "false")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "false")
    monkeypatch.delenv("AETHER_WORKER_DISABLED", raising=False)
    monkeypatch.delenv("AETHER_EMBED_WORKER", raising=False)
    monkeypatch.delenv("AETHER_WORKER_COMMAND", raising=False)
    monkeypatch.setattr(routes.document_store, "storage_ready", lambda: True)


def test_release_readiness_requires_an_explicit_worker_configuration(monkeypatch):
    _configure_controlled_release(monkeypatch)

    result = routes.release_readiness()

    assert result["checks"]["private_document_storage"] is True
    assert result["checks"]["worker_command_configured"] is False
    assert result["ready_for_controlled_mvp"] is False
    assert "Durable worker command is not configured" in result["controlled_mvp_blockers"]


def test_release_readiness_accepts_configured_embedded_worker(monkeypatch):
    _configure_controlled_release(monkeypatch)
    monkeypatch.setenv("AETHER_EMBED_WORKER", "true")

    result = routes.release_readiness()

    assert result["checks"]["worker_command_configured"] is True
    assert result["checks"]["synthetic_mode"] is True
    assert result["ready_for_controlled_mvp"] is True
