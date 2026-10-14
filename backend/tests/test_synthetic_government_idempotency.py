from aether_core.synthetic_government import SyntheticGovernmentSystem


def test_repeated_submission_with_same_idempotency_key_creates_one_request():
    system = SyntheticGovernmentSystem()

    first = system.submit(
        "Revenue",
        "land_record",
        {"parcel_id": "P-001"},
        idempotency_key="case-1:land-record",
    )
    duplicate = system.submit(
        "Revenue",
        "land_record",
        {"parcel_id": "P-001"},
        idempotency_key="case-1:land-record",
    )

    assert duplicate == first
    assert system.request_count == 1
    assert system.result(first)["parcel_id"] == "P-001"
