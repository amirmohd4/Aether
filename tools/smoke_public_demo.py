#!/usr/bin/env python3
"""Live smoke test for Aether's isolated, synthetic public demo service.

Uses only the Python standard library and fictional test data. This test creates
one temporary demo case, verifies per-session isolation, and checks that
sensitive operations remain disabled.
"""
from __future__ import annotations

import json
import os
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.getenv("AETHER_PUBLIC_DEMO_URL", "https://aether-public-demo.onrender.com").rstrip("/")
PREVIEW_ORIGIN = os.getenv("AETHER_PREVIEW_ORIGIN", "https://deploy-preview-10--aether-govos.netlify.app")


def request(path: str, method: str = "GET", headers: dict | None = None, body: bytes | None = None):
    req = Request(BASE_URL + path, data=body, headers=headers or {}, method=method)
    try:
        with urlopen(req, timeout=20) as response:
            return response.status, response.headers, response.read()
    except HTTPError as exc:
        return exc.code, exc.headers, exc.read()
    except (URLError, TimeoutError) as exc:
        return 0, {}, str(exc).encode("utf-8", "replace")


def wait_for_demo(session_id: str) -> None:
    headers = {"X-Aether-Demo-Session": session_id}
    last = (0, 0, 0)
    for _ in range(36):
        health_status, _, _ = request("/health")
        ready_status, _, _ = request("/ready")
        me_status, _, me_body = request("/api/aether/v2/me", headers=headers)
        last = (health_status, ready_status, me_status)
        if health_status == 200 and ready_status == 200 and me_status == 200:
            principal = json.loads(me_body)
            if principal.get("auth_mode") == "public_demo" and principal.get("tenant_id", "").startswith("public-demo:"):
                return
        time.sleep(10)
    raise RuntimeError(f"public demo did not become ready with session auth; HTTP statuses health/ready/me={last}")


def main() -> None:
    session_id = str(uuid.uuid4())
    other_session_id = str(uuid.uuid4())
    session_headers = {"X-Aether-Demo-Session": session_id}
    wait_for_demo(session_id)

    preflight_status, preflight_headers, _ = request(
        "/api/aether/v2/me",
        method="OPTIONS",
        headers={
            "Origin": PREVIEW_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "x-aether-demo-session",
        },
    )
    assert preflight_status in (200, 204), f"CORS preflight returned HTTP {preflight_status}"
    assert preflight_headers.get("Access-Control-Allow-Origin") == PREVIEW_ORIGIN, "preview origin is not allowed by CORS"

    case_payload = {
        "objective": "I want to open a restaurant",
        "customer_type": "business",
        "jurisdiction": {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        "inputs": {
            "owner_name": "Synthetic Smoke Applicant",
            "parcel_id": "SMOKE-TEST-ONLY",
            "area": 2.0,
            "documents": ["identity_document", "lease_or_ownership", "floor_plan"],
        },
    }
    status, _, body = request(
        "/api/aether/v2/cases",
        method="POST",
        headers={**session_headers, "Content-Type": "application/json"},
        body=json.dumps(case_payload).encode("utf-8"),
    )
    assert status == 200, f"synthetic case creation returned HTTP {status}: {body[:300]!r}"
    case = json.loads(body)
    case_id = (case.get("summary") or {}).get("case_id")
    assert case_id, f"case creation response did not include a case id: {body[:300]!r}"

    status, _, body = request(f"/api/aether/v2/cases/{case_id}", headers=session_headers)
    assert status == 200, f"same-session case read returned HTTP {status}"
    assert (json.loads(body).get("summary") or {}).get("case_id") == case_id

    status, _, _ = request(
        f"/api/aether/v2/cases/{case_id}",
        headers={"X-Aether-Demo-Session": other_session_id},
    )
    assert status == 404, f"another demo session could access the case (HTTP {status})"

    status, _, _ = request("/api/aether/v2/api-keys", headers=session_headers)
    assert status == 403, f"API-key management should be disabled (HTTP {status})"

    boundary = "----AetherPublicDemoSmokeBoundary"
    multipart = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="synthetic-only.txt"\r\n'
        "Content-Type: text/plain\r\n\r\n"
        "synthetic test content only\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    status, _, _ = request(
        f"/api/aether/v2/cases/{case_id}/documents/upload?document_type=identity_document",
        method="POST",
        headers={**session_headers, "Content-Type": f"multipart/form-data; boundary={boundary}"},
        body=multipart,
    )
    assert status == 403, f"real file uploads should be disabled in the public demo (HTTP {status})"

    print("PASS: health/readiness, CORS, case create/read, cross-session isolation, upload block, API-key block")


if __name__ == "__main__":
    main()
