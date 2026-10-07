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
