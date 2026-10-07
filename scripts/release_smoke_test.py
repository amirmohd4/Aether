#!/usr/bin/env python3
"""Release smoke test for the deployed Aether API.

Usage:
  AETHER_API_URL=https://backend.example.com python scripts/release_smoke_test.py
  AETHER_API_TOKEN=<supabase-access-token> ...   # when auth is required
"""

from __future__ import annotations

import os
import sys

import httpx


def main() -> int:
    base = os.getenv("AETHER_API_URL", "http://localhost:8081").rstrip("/")
    token = os.getenv("AETHER_API_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    checks = [
        ("health", "/health", 200),
        ("ready", "/ready", 200),
        ("service catalog", "/api/aether/v2/services", 200),
        ("rule readiness", "/api/aether/v2/rules/readiness", 200),
    ]

    failures = []
    with httpx.Client(timeout=15.0, follow_redirects=True) as client:
        for name, path, expected in checks:
            try:
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
