#!/usr/bin/env python3
"""Release smoke test for the Aether controlled-MVP or production API."""

from __future__ import annotations

import os
import sys

import httpx


def main() -> int:
    base = os.getenv("AETHER_API_URL", "http://localhost:8081").rstrip("/")
    bearer = os.getenv("AETHER_API_TOKEN", "").strip()
    api_key = os.getenv("AETHER_API_KEY", "").strip()

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
        ("release readiness", "/api/aether/v2/release/readiness", 200, False),
    ]

    failures = []
    with httpx.Client(timeout=15.0, follow_redirects=True) as client:
        for name, path, expected, auth_required in checks:
            try:
                if auth_required and not (bearer or api_key):
                    print(f"SKIP {name}: credentials not supplied")
                    continue
                response = client.get(base + path, headers=headers)
                ok = response.status_code == expected
                print(f"{'PASS' if ok else 'FAIL'} {name}: HTTP {response.status_code}")
                if not ok:
                    failures.append(name)
            except Exception as exc:
                print(f"FAIL {name}: {type(exc).__name__}: {exc}")
                failures.append(name)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
