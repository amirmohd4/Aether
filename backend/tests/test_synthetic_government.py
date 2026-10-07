from aether_core.synthetic_government import SyntheticGovernmentSystem


def test_synthetic_environment_is_deterministic_and_idempotent():
    government = SyntheticGovernmentSystem()
    payload = {"parcel_id": "P-001", "land_area": 4.2}
    first = government.execute("Revenue", "land_record", payload, "case-1:land")
    second = government.execute("Revenue", "land_record", payload, "case-1:land")
    assert first["request_id"] == second["request_id"]
    assert first["result"]["area"] == 4.2


def test_synthetic_environment_can_model_query_without_touching_real_systems():
    government = SyntheticGovernmentSystem()
    result = government.execute(
        "Municipal",
        "building",
        {"simulate_query": True},
        "case-2:building",
    )
    assert result["status"] == "query"
    assert "query" in result["result"]
