from fastapi import HTTPException

from aether_core.domain import Case
from aether_core.security import Principal
from aether_core.routes import _authorize_case


def _case(owner="user-1", tenant="tenant-1"):
    return Case(
        case_id="A-TEST",
        objective="Test",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        inputs={},
        service_department="Revenue",
        requirements=[],
        tasks={},
        owner_user_id=owner,
        tenant_id=tenant,
    )


def test_owner_can_access_own_case():
    _authorize_case(_case(), Principal("user-1", "user", "tenant-1", "supabase"))


def test_same_tenant_officer_can_access_case():
    _authorize_case(_case(), Principal("officer-1", "officer", "tenant-1", "supabase", "Revenue", {"country": "India", "state": "Jammu and Kashmir"}))


def test_cross_tenant_user_cannot_access_case():
    try:
        _authorize_case(_case(), Principal("user-2", "user", "tenant-2", "supabase"))
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("cross-tenant access should be rejected")


def test_admin_can_access_case_within_own_tenant():
    _authorize_case(_case(), Principal("admin-1", "admin", "tenant-1", "supabase"))


def test_admin_cannot_access_case_in_another_tenant():
    try:
        _authorize_case(_case(), Principal("admin-1", "admin", "tenant-x", "supabase"))
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("tenant admin must not access another tenant's case")


def test_officer_cannot_access_case_outside_authorized_department():
    try:
        _authorize_case(
            _case(),
            Principal("officer-2", "officer", "tenant-1", "supabase", "Health", {"country": "India"}),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("cross-department officer access should be rejected")


def test_officer_cannot_access_case_outside_authorized_jurisdiction():
    try:
        _authorize_case(
            _case(),
            Principal("officer-3", "officer", "tenant-1", "supabase", "Revenue", {"country": "India", "state": "Maharashtra"}),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("cross-jurisdiction officer access should be rejected")



def test_officer_case_listing_filters_department_and_jurisdiction(monkeypatch):
    from aether_core.routes import _list_visible_cases

    allowed = _case()
    hidden_department = _case()
    hidden_department.case_id = "A-HIDDEN-DEPT"
    hidden_department.service_department = "Health"

    hidden_jurisdiction = _case()
    hidden_jurisdiction.case_id = "A-HIDDEN-JURIS"
    hidden_jurisdiction.jurisdiction = {
        "country": "India",
        "state": "Maharashtra",
        "district": "Mumbai",
    }

    cases = {
        allowed.case_id: allowed,
        hidden_department.case_id: hidden_department,
        hidden_jurisdiction.case_id: hidden_jurisdiction,
    }

    monkeypatch.setattr(
        "aether_core.routes.engine.store.list",
        lambda **_: [{"case_id": case_id} for case_id in cases],
    )
    monkeypatch.setattr(
        "aether_core.routes.engine.get_case",
        lambda case_id: cases[case_id],
    )

    visible = _list_visible_cases(
        Principal(
            "officer-1",
            "officer",
            "tenant-1",
            "supabase",
            "Revenue",
            {"country": "India", "state": "Jammu and Kashmir"},
        ),
        status="waiting_for_human",
        limit=10,
    )

    assert [item["case_id"] for item in visible] == [allowed.case_id]



def test_officer_without_department_is_denied():
    try:
        _authorize_case(_case(), Principal("officer-1", "officer", "tenant-1", "supabase"))
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("officer without a department assignment must be denied")


def test_officer_without_required_jurisdiction_is_denied():
    try:
        _authorize_case(
            _case(),
            Principal("officer-1", "officer", "tenant-1", "supabase", "Revenue", {"state": "Jammu and Kashmir", "district": "Srinagar"}),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("case outside the assigned jurisdiction must be denied")


def test_api_key_human_decision_requires_explicit_scope():
    from aether_core.security import require_human_authority

    principal = Principal("api-key:test", "officer", "tenant-1", "api_key", scopes=frozenset({"cases:read", "cases:write"}))
    try:
        require_human_authority(principal)
    except HTTPException as exc:
        assert exc.status_code == 403
    else:
        raise AssertionError("API key must have human:decide scope")


def test_api_key_human_decision_allows_explicit_scope():
    from aether_core.security import require_human_authority

    principal = Principal("api-key:test", "officer", "tenant-1", "api_key", scopes=frozenset({"human:decide"}))
    assert require_human_authority(principal) == principal



def test_admin_case_listing_is_tenant_scoped(monkeypatch):
    from aether_core.routes import _list_visible_cases

    monkeypatch.setattr(
        "aether_core.routes.engine.store.list",
        lambda **kwargs: kwargs,
    )
    result = _list_visible_cases(
        Principal("admin-1", "admin", "tenant-1", "supabase"),
        status="waiting_for_human",
        limit=10,
    )
    assert result["tenant_id"] == "tenant-1"
    assert result["status"] == "waiting_for_human"
    assert result["limit"] == 10



def _request(headers=None):
    from starlette.requests import Request

    return Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": headers or [],
        "client": ("127.0.0.1", 1234),
        "server": ("testserver", 80),
        "scheme": "http",
        "query_string": b"",
    })


def test_public_demo_requires_explicit_safe_configuration(monkeypatch):
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_PUBLIC_DEMO", "true")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "false")

    principal = require_principal(_request([(b"x-aether-demo-session", b"550e8400-e29b-41d4-a716-446655440000")]))
    assert principal.auth_mode == "public_demo"
    assert principal.tenant_id.startswith("public-demo:")
    assert principal.role == "demo"


def test_public_demo_rejects_production_environment(monkeypatch):
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_ENV", "production")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_PUBLIC_DEMO", "true")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "false")

    try:
        require_principal(_request())
    except HTTPException as exc:
        assert exc.status_code == 500
    else:
        raise AssertionError("public demo must never run in production")


def test_public_demo_rejects_enabled_government_connectors(monkeypatch):
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_PUBLIC_DEMO", "true")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "true")

    try:
        require_principal(_request())
    except HTTPException as exc:
        assert exc.status_code == 500
    else:
        raise AssertionError("public demo must reject live connector configuration")



def test_public_demo_rejects_missing_session(monkeypatch):
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_PUBLIC_DEMO", "true")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "false")

    try:
        require_principal(_request())
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("public demo must require a session identifier")



def test_public_demo_sessions_are_isolated(monkeypatch):
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    monkeypatch.setenv("AETHER_PUBLIC_DEMO", "true")
    monkeypatch.setenv("AETHER_ENABLE_PRODUCTION_CONNECTORS", "false")

    first = require_principal(_request([(b"x-aether-demo-session", b"550e8400-e29b-41d4-a716-446655440000")]))
    second = require_principal(_request([(b"x-aether-demo-session", b"550e8400-e29b-41d4-a716-446655440001")]))
    assert first.tenant_id != second.tenant_id
    assert first.subject != second.subject
