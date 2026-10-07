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


def test_admin_can_access_case():
    _authorize_case(_case(), Principal("admin-1", "admin", "tenant-x", "supabase"))


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
