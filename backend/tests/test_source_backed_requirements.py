from aether_core.requirements_engine import RequirementEngine


def test_jk_restaurant_requirements_are_source_backed():
    requirements = RequirementEngine().discover(
        "I want to open a restaurant",
        "business",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {},
    )
    by_id = {r.id: r for r in requirements}
    assert by_id["food"].source
    assert by_id["fire"].source
    assert by_id["municipal"].source
    assert by_id["shops_establishment"].source
    assert all(r.verified_at for r in requirements if r.source)
    assert all(r.authority_status == "source_backed" for r in requirements if r.source)


def test_non_jk_does_not_apply_jk_specific_rules():
    requirements = RequirementEngine().discover(
        "I want to open a restaurant",
        "business",
        {"country": "India", "state": "Maharashtra", "district": "Pune"},
        {},
    )
    ids = {r.id for r in requirements}
    assert "fire" not in ids
    assert "municipal" not in ids
    assert "shops_establishment" not in ids
