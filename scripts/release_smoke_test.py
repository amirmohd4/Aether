#!/usr/bin/env python3
"""Fail-closed release smoke test for the Aether controlled-MVP API."""

from __future__ import annotations

import os
import sys

import httpx


def main() -> int:
    base = os.getenv("AETHER_API_URL", "http://localhost:8081").rstrip("/")
    bearer = os.getenv("AETHER_API_TOKEN", "").strip()
    api_key = os.getenv("AETHER_API_KEY", "").strip()

    if not (bearer or api_key):
        print(
            "FAIL authenticated release smoke: AETHER_API_TOKEN or "
            "AETHER_API_KEY is required; refusing to report a partial pass"
        )
        return 2

    headers = {}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    if api_key:
        headers["X-Aether-API-Key"] = api_key

    checks = [
        ("health", "/health", 200, False),
        ("ready", "/ready", 200, False),
        ("service catalog", "/api/aether/v2/services", 200, True),
        ("marketplace", "/api/aether/v2/marketplace", 200, True),
        ("connector catalog", "/api/aether/v2/connectors", 200, True),
        ("rule readiness", "/api/aether/v2/rules/readiness", 200, True),
        ("India admin overview", "/api/aether/v2/admin-intelligence/overview", 200, True),
        ("India department catalog", "/api/aether/v2/admin-intelligence/departments", 200, True),
        ("India journey templates", "/api/aether/v2/admin-intelligence/journeys", 200, True),
        ("release readiness", "/api/aether/v2/release/readiness", 200, True),
    ]

    failures = []
    authenticated_checks = 0
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        for name, path, expected, auth_required in checks:
            try:
                response = client.get(base + path, headers=headers)
                ok = response.status_code == expected
                detail = ""
                if auth_required:
                    authenticated_checks += 1
                if ok and name == "ready":
                    payload = response.json()
                    ok = (
                        payload.get("status") == "ready"
                        and payload.get("database") == "ready"
                        and payload.get("database_role_valid") is True
                    )
                    if not ok:
                        detail = f" readiness_payload={payload}"
                if ok and name == "release readiness":
                    payload = response.json()
                    status_checks = payload.get("checks") or {}
                    blockers = payload.get("controlled_mvp_blockers") or []
                    required = {
                        "supabase_auth": True,
                        "encryption_key": True,
                        "private_document_storage": True,
                        "legacy_api_quarantined": True,
                        "worker_command_configured": True,
                        "synthetic_mode": True,
                    }
                    missing = [
                        key for key, value in required.items()
                        if status_checks.get(key) is not value
                    ]
                    ok = (
                        payload.get("ready_for_controlled_mvp") is True
                        and not blockers
                        and not missing
                    )
                    if blockers:
                        detail += f" blockers={blockers}"
                    if missing:
                        detail += f" failed_checks={missing}"
                print(f"{'PASS' if ok else 'FAIL'} {name}: HTTP {response.status_code}{detail}")
                if not ok:
                    failures.append(name)
            except Exception as exc:
                print(f"FAIL {name}: {type(exc).__name__}: {exc}")
                failures.append(name)

    expected_authenticated_checks = sum(1 for check in checks if check[3])
    if authenticated_checks != expected_authenticated_checks:
        print(
            "FAIL authenticated coverage: "
            f"ran {authenticated_checks}/{expected_authenticated_checks} checks"
        )
        failures.append("authenticated coverage")

    if failures:
        print(f"Release smoke failed: {', '.join(failures)}")
        return 1
    print(
        f"PASS complete release smoke: {authenticated_checks} authenticated "
        "product/release checks plus public health/readiness checks"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
