from fastapi import HTTPException
from fastapi.requests import Request

from aether_core.security import Principal, require_principal
from aether_core.understanding import ObjectiveUnderstandingEngine


def _request(headers=None):
    return Request({
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
    })


def test_production_auth_fails_closed_without_configuration(monkeypatch):
    monkeypatch.setenv("AETHER_ENV", "production")
    monkeypatch.setenv("AETHER_AUTH_MODE", "none")
    try:
        require_principal(_request())
    except HTTPException as exc:
        assert exc.status_code == 500
        assert "authentication" in exc.detail.lower()
    else:
        raise AssertionError("production must not allow anonymous Aether auth")


def test_understanding_exposes_ranked_candidates_for_review():
    result = ObjectiveUnderstandingEngine().understand(
        "I want to get a passport application",
        "citizen",
        {"country": "India", "state": "Jammu and Kashmir"},
    )
    assert result.service_id == "passport"
    assert result.candidates
    assert result.candidates[0]["service_id"] == "passport"
