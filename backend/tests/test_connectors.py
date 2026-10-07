from aether_core.connector_registry import ConnectorRegistry
from aether_core.connectors import ConfiguredHTTPConnector, SyntheticConnector
from aether_core.synthetic_government import SyntheticGovernmentSystem


def test_connector_contract_normalizes_source_response():
    registry = ConnectorRegistry(SyntheticGovernmentSystem())
    connector = registry.get("Revenue")
    response = connector.execute(
        "land_record",
        {"parcel_id": "P-001", "land_area": 3.5},
        "case-connector:land",
    )
    assert response["status"] == "completed"
    assert response["request_id"]
    assert response["result"]["area"] == 3.5
    assert response["source"] == "Synthetic Revenue System"


def test_connector_registry_reuses_department_connector_and_shared_system():
    system = SyntheticGovernmentSystem()
    registry = ConnectorRegistry(system)
    first = registry.get("Revenue")
    second = registry.get("Revenue")
    assert first is second
    assert isinstance(first, SyntheticConnector)
    result = first.execute("land_record", {"parcel_id": "P-1"}, "same-key")
    assert second.get_result(result["request_id"])["parcel_id"] == "P-1"


def test_configured_http_connector_uses_stable_request_contract(monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    def fake_post(url, json, headers, timeout):
        calls.append(("post", url, json, headers, timeout))
        return FakeResponse({"request_id": "GOV-123", "status": "submitted"})

    def fake_get(url, headers, timeout):
        calls.append(("get", url, headers, timeout))
        return FakeResponse({
            "request_id": "GOV-123",
            "status": "completed",
            "result": {"verified": True, "source": "Authorized Revenue System"},
        })

    import httpx
    monkeypatch.setattr(httpx, "post", fake_post)
    monkeypatch.setattr(httpx, "get", fake_get)

    connector = ConfiguredHTTPConnector(
        "Revenue",
        "https://gov.example.test/api",
        bearer_token="server-secret",
    )
    result = connector.execute("land_record", {"parcel_id": "P-9"}, "case-1:land")

    assert result["status"] == "completed"
    assert result["department"] == "Revenue"
    assert result["mode"] == "production"
    assert calls[0][0] == "post"
    assert calls[0][3]["Authorization"] == "Bearer server-secret"
    assert calls[0][3]["Idempotency-Key"] == "case-1:land"
    assert calls[1][1].endswith("/requests/GOV-123")
