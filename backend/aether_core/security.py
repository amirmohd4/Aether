from __future__ import annotations

from dataclasses import dataclass
import hmac
import os
from typing import Optional

import httpx
from fastapi import Depends, HTTPException, Request


@dataclass(frozen=True)
class Principal:
    subject: str
    role: str
    tenant_id: Optional[str]
    auth_mode: str


def auth_mode() -> str:
    return os.getenv("AETHER_AUTH_MODE", "none").strip().lower()


def _api_key_principal(request: Request) -> Principal:
    configured = os.getenv("AETHER_API_KEY")
    supplied = request.headers.get("X-Aether-API-Key")
    if not configured or not supplied or not hmac.compare_digest(supplied, configured):
        raise HTTPException(status_code=401, detail="Valid Aether API key required")
    return Principal(
        subject=os.getenv("AETHER_API_KEY_SUBJECT", "api-client"),
        role=os.getenv("AETHER_API_KEY_ROLE", "service"),
        tenant_id=os.getenv("AETHER_API_KEY_TENANT_ID"),
        auth_mode="api_key",
    )


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

    app_metadata = user.get("app_metadata") or {}
    return Principal(
        subject=user.get("id", ""),
        role=str(app_metadata.get("role", "user")),
        tenant_id=app_metadata.get("tenant_id"),
        auth_mode="supabase",
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


def require_role(*allowed_roles: str):
    allowed = {role.lower() for role in allowed_roles}

    def dependency(principal: Principal = Depends(require_principal)) -> Principal:
        if principal.auth_mode == "none":
            return principal
        if principal.role.lower() not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient Aether role")
        return principal

    return dependency
