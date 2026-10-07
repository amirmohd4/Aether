from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import hmac
import os
from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import Depends, HTTPException, Request
from sqlalchemy import text

from backend.database import SessionLocal
from .persistence_models import AetherApiKeyRecord


@dataclass(frozen=True)
class Principal:
    subject: str
    role: str
    tenant_id: Optional[str]
    auth_mode: str
    department: Optional[str] = None
    jurisdiction: dict = field(default_factory=dict)
    scopes: frozenset[str] = frozenset()


def auth_mode() -> str:
    return os.getenv("AETHER_AUTH_MODE", "none").strip().lower()


def _api_key_principal(request: Request) -> Principal:
    configured = os.getenv("AETHER_API_KEY")
    supplied = request.headers.get("X-Aether-API-Key")
    if not supplied:
        raise HTTPException(status_code=401, detail="Aether API key required")

    if configured and hmac.compare_digest(supplied, configured):
        return Principal(
            subject=os.getenv("AETHER_API_KEY_SUBJECT", "api-client"),
            role=os.getenv("AETHER_API_KEY_ROLE", "service"),
            tenant_id=os.getenv("AETHER_API_KEY_TENANT_ID"),
            auth_mode="api_key",
            scopes=frozenset(
                item.strip() for item in os.getenv("AETHER_API_KEY_SCOPES", "*").split(",") if item.strip()
            ),
        )

    key_hash = hashlib.sha256(supplied.encode("utf-8")).hexdigest()
    try:
        with SessionLocal() as db:
            row = db.query(AetherApiKeyRecord).filter_by(
                key_hash=key_hash,
                status="active",
            ).one_or_none()
            if not row:
                raise HTTPException(status_code=401, detail="Invalid or revoked Aether API key")
            if row.expires_at and row.expires_at <= datetime.now(timezone.utc).replace(tzinfo=None):
                row.status = "expired"
                db.commit()
                raise HTTPException(status_code=401, detail="Aether API key expired")
            row.last_used_at = datetime.utcnow()
            db.commit()
            return Principal(
                subject=f"api-key:{row.key_prefix}",
                role=row.role,
                tenant_id=row.tenant_id,
                auth_mode="api_key",
                scopes=frozenset(row.scopes or ["cases:read", "cases:write"]),
            )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="API key store unavailable") from exc


def _supabase_membership_for_subject(subject: str, tenant_id: str | None = None) -> dict:
    """Resolve one active membership without ever choosing an arbitrary tenant."""
    try:
        with SessionLocal() as db:
            if tenant_id:
                row = db.execute(
                    text(
                        "SELECT role, tenant_id, department, jurisdiction FROM public.aether_memberships "
                        "WHERE user_id = :user_id AND tenant_id = :tenant_id AND status = 'active' "
                        "LIMIT 1"
                    ),
                    {"user_id": subject, "tenant_id": tenant_id},
                ).mappings().first()
                if not row:
                    raise HTTPException(status_code=403, detail="Requested Aether tenant is not an active membership")
                return dict(row)

            rows = db.execute(
                text(
                    "SELECT role, tenant_id, department, jurisdiction FROM public.aether_memberships "
                    "WHERE user_id = :user_id AND status = 'active' "
                    "ORDER BY updated_at DESC, created_at DESC"
                ),
                {"user_id": subject},
            ).mappings().all()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Authorization membership store unavailable") from exc

    if not rows:
        raise HTTPException(status_code=403, detail="No active Aether membership")
    if len(rows) > 1:
        memberships = [{
            "tenant_id": str(row["tenant_id"]),
            "role": str(row["role"]),
            "department": str(row["department"]) if row["department"] else None,
            "jurisdiction": row["jurisdiction"] or {},
        } for row in rows]
        raise HTTPException(
            status_code=409,
            detail={
                "code": "multiple_active_memberships",
                "message": "Multiple active Aether memberships exist; select a tenant explicitly.",
                "memberships": memberships,
            },
        )
    return dict(rows[0])


def _supabase_principal(request: Request) -> Principal:
    authorization = request.headers.get("Authorization", "")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer access token required")

    token = authorization.split(" ", 1)[1].strip()
    base_url = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL")
    publishable_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY")
    if not base_url or not publishable_key:
        raise HTTPException(status_code=500, detail="Supabase authentication is not configured")

    try:
        response = httpx.get(
            f"{base_url.rstrip('/')}/auth/v1/user",
            headers={"apikey": publishable_key, "Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        user = response.json()
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Authentication service unavailable") from exc

    subject = str(user.get("id", ""))
    if not subject:
        raise HTTPException(status_code=401, detail="Authenticated user identity missing")

    # Authorization is server-controlled. Do not trust user-editable metadata
    # for role or tenant membership; resolve the active membership record on the
    # server before any case data is returned or mutated.
    membership = _supabase_membership_for_subject(
        subject,
        tenant_id=request.headers.get("X-Aether-Tenant-ID"),
    )

    return Principal(
        subject=subject,
        role=str(membership["role"]),
        tenant_id=str(membership["tenant_id"]) if membership["tenant_id"] is not None else None,
        auth_mode="supabase",
        department=str(membership["department"]) if membership["department"] else None,
        jurisdiction=membership["jurisdiction"] or {},
    )


def require_principal(request: Request) -> Principal:
    mode = auth_mode()
    if os.getenv("AETHER_ENV", "development").strip().lower() == "production" and mode == "none":
        raise HTTPException(status_code=500, detail="Production authentication is not configured")
    if mode == "none":
        return Principal(
            subject="demo",
            role="demo",
            tenant_id="demo",
            auth_mode="none",
        )
    if mode == "api_key":
        return _api_key_principal(request)
    if mode == "supabase":
        return _supabase_principal(request)
    raise HTTPException(status_code=500, detail=f"Unsupported Aether auth mode: {mode}")


def require_scope(scope: str):
    def dependency(principal: Principal = Depends(require_principal)) -> Principal:
        if principal.auth_mode != "api_key" or "*" in principal.scopes or scope in principal.scopes:
            return principal
        raise HTTPException(status_code=403, detail=f"Missing Aether API scope: {scope}")
    return dependency


def require_role(*allowed_roles: str):
    allowed = {role.lower() for role in allowed_roles}

    def dependency(principal: Principal = Depends(require_principal)) -> Principal:
        if principal.auth_mode == "none":
            return principal
        if principal.role.lower() not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient Aether role")
        return principal

    return dependency