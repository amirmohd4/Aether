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
    _authorize_case(_case(), Principal("officer-1", "officer", "tenant-1", "supabase"))


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


def test_admin_case_listing_is_limited_to_own_tenant(monkeypatch):
    from aether_core.routes import _list_visible_cases

    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return [{"case_id": "A-TENANT-1"}]

    monkeypatch.setattr("aether_core.routes.engine.store.list", fake_list)
    visible = _list_visible_cases(
        Principal("admin-1", "admin", "tenant-1", "supabase"),
        limit=10,
    )

    assert visible == [{"case_id": "A-TENANT-1"}]
    assert captured["tenant_id"] == "tenant-1"


def test_admin_without_tenant_cannot_list_cases(monkeypatch):
    from aether_core.routes import _list_visible_cases

    def forbidden_list(**kwargs):
        raise AssertionError("tenantless admin must not query cases")

    monkeypatch.setattr("aether_core.routes.engine.store.list", forbidden_list)
    assert _list_visible_cases(Principal("admin-1", "admin", None, "supabase")) == []


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
            Principal("officer-3", "officer", "tenant-1", "supabase", "business", {"country": "India", "state": "Maharashtra"}),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("cross-jurisdiction officer access should be rejected")


def test_officer_cannot_access_case_when_department_metadata_is_missing():
    case = _case()
    case.service_department = None
    try:
        _authorize_case(
            case,
            Principal("officer-4", "officer", "tenant-1", "supabase", "Revenue"),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing department metadata must fail closed")


def test_officer_cannot_access_case_when_scoped_jurisdiction_is_missing():
    case = _case()
    case.jurisdiction = {"country": "India"}
    try:
        _authorize_case(
            case,
            Principal("officer-5", "officer", "tenant-1", "supabase", "Revenue", {"country": "India", "state": "Jammu and Kashmir"}),
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing scoped jurisdiction must fail closed")



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


def test_staging_static_api_key_works_alongside_supabase_and_is_read_scoped(monkeypatch):
    from starlette.requests import Request
    from aether_core.security import require_principal

    monkeypatch.setenv("AETHER_AUTH_MODE", "supabase")
    monkeypatch.setenv("AETHER_ENV", "staging")
    monkeypatch.setenv("AETHER_ALLOW_STATIC_STAGING_API_KEY", "true")
    monkeypatch.setenv("AETHER_API_KEY", "staging-test-secret")
    monkeypatch.delenv("AETHER_API_KEY_SCOPES", raising=False)

    request = Request({
        "type": "http",
        "headers": [(b"x-aether-api-key", b"staging-test-secret")],
    })
    principal = require_principal(request)

    assert principal.auth_mode == "api_key"
    assert principal.role == "service"
    assert principal.subject == "staging-smoke"
    assert principal.scopes == frozenset({"cases:read"})


def test_static_staging_api_key_is_not_enabled_by_default(monkeypatch):
    from starlette.requests import Request
    import aether_core.security as security

    monkeypatch.setenv("AETHER_AUTH_MODE", "supabase")
    monkeypatch.setenv("AETHER_ENV", "production")
    monkeypatch.setenv("AETHER_ALLOW_STATIC_STAGING_API_KEY", "true")
    monkeypatch.setenv("AETHER_API_KEY", "staging-test-secret")

    called = {}
    def fake_api_key_principal(request, *, allow_static=False):
        called["allow_static"] = allow_static
        raise HTTPException(status_code=401, detail="invalid")

    monkeypatch.setattr(security, "_api_key_principal", fake_api_key_principal)
    request = Request({
        "type": "http",
        "headers": [(b"x-aether-api-key", b"staging-test-secret")],
    })
    try:
        security.require_principal(request)
    except HTTPException as exc:
        assert exc.status_code == 401
    else:
        raise AssertionError("production must not accept the static staging key")
    assert called["allow_static"] is False
