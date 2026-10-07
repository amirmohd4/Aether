from aether_core.connector_registry import ConnectorRegistry
from aether_core.connectors import SyntheticConnector
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
