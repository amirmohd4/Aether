from fastapi import HTTPException
from fastapi.requests import Request

from aether_core.security import Principal, require_principal
from aether_core.understanding import ObjectiveUnderstandingEngine


def _request(headers=None):
    return Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
    })


def test_production_auth_fails_closed_without_configuration(monkeypatch):
    monkeypatch.setenv("AETHER_ENV", "production")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    try:
        require_principal(_request())
    except HTTPException as exc:
        assert exc.status_code == 500
        assert "authentication" in exc.detail.lower()
    else:
        raise AssertionError("production must not allow anonymous Aether auth")


def test_understanding_exposes_ranked_candidates_for_review():
    result = ObjectiveUnderstandingEngine().understand(
        "I want to get a passport application",
        "citizen",
        {"country": "India", "state": "Jammu and Kashmir"},
    )
    assert result.service_id == "passport"
    assert result.candidates
    assert result.candidates[0]["service_id"] == "passport"



def test_database_backed_api_key_is_tenant_scoped(monkeypatch):
    import hashlib
    from datetime import datetime
    from aether_core.security import _api_key_principal
    from aether_core.persistence_models import AetherApiKeyRecord
    from backend.database import SessionLocal
    from aether_core.case_store import DatabaseCaseStore

    monkeypatch.delenv("AETHER_API_KEY", raising=False)
    monkeypatch.setenv("AETHER_AUTH_MODE", "api_key")
    raw = "aether_test_database_key"
    DatabaseCaseStore()._ensure_schema()

    with SessionLocal() as db:
        existing = db.query(AetherApiKeyRecord).filter_by(key_prefix="aether_test_database").one_or_none()
        if existing:
            db.delete(existing)
            db.commit()
        db.add(AetherApiKeyRecord(
            tenant_id="tenant-db",
            key_prefix="aether_test_database",
            key_hash=hashlib.sha256(raw.encode()).hexdigest(),
            role="developer",
            scopes=["cases:read"],
            status="active",
            created_at=datetime.utcnow(),
        ))
        db.commit()

    principal = _api_key_principal(_request({"X-Aether-API-Key": raw}))
    assert principal.tenant_id == "tenant-db"
    assert principal.role == "developer"
    assert "cases:read" in principal.scopes

def test_supabase_auth_refuses_arbitrary_tenant_selection(monkeypatch):
    import aether_core.security as security

    class FakeResponse:
        status_code = 200
        def json(self):
            return {"id": "user-multi"}

    membership_rows = [
        {"role": "user", "tenant_id": "tenant-b", "department": None, "jurisdiction": {}},
        {"role": "user", "tenant_id": "tenant-a", "department": None, "jurisdiction": {}},
    ]

    class FakeResult:
        def __init__(self, rows):
            self.rows = rows
        def mappings(self):
            return self
        def all(self):
            return list(self.rows)
        def first(self):
            return self.rows[0] if self.rows else None

    class FakeDB:
        def __enter__(self):
            return self
        def __exit__(self, *_):
            return False
        def execute(self, *_args, **kwargs):
            params = kwargs.get("parameters") or (_args[1] if len(_args) > 1 else {})
            if params.get("tenant_id"):
                rows = [row for row in membership_rows if row["tenant_id"] == params["tenant_id"]]
            else:
                rows = membership_rows
            return FakeResult(rows)

    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "publishable-test-key")
    monkeypatch.setattr(security.httpx, "get", lambda *args, **kwargs: FakeResponse())
    monkeypatch.setattr(security, "SessionLocal", lambda: FakeDB())

    try:
        security._supabase_principal(_request({"Authorization": "Bearer test-token"}))
    except HTTPException as exc:
        assert exc.status_code == 409
        assert exc.detail["code"] == "multiple_active_memberships"
        assert {item["tenant_id"] for item in exc.detail["memberships"]} == {"tenant-a", "tenant-b"}
    else:
        raise AssertionError("ambiguous active memberships must require an explicit tenant")

    principal = security._supabase_principal(_request({
        "Authorization": "Bearer test-token",
        "X-Aether-Tenant-ID": "tenant-a",
    }))
    assert principal.tenant_id == "tenant-a"
