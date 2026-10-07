from aether_core.requirements_engine import RequirementEngine


def test_restaurant_intake_identifies_missing_documents():
    engine = RequirementEngine()
    requirements = engine.discover(
        "I want to open a restaurant",
        "developer",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": ["identity_document"]},
    )
    request = engine.document_request(requirements)
    submitted = {"identity_document"}
    missing = [doc for doc in request["documents"] if doc not in submitted]
    assert "food_business_details" in missing
    assert "floor_plan" in missing


def test_complete_document_set_has_no_missing_intake():
    engine = RequirementEngine()
    requirements = engine.discover(
        "I want to open a restaurant",
        "developer",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {},
    )
    request = engine.document_request(requirements)
    submitted = set(request["documents"])
    assert not [doc for doc in request["documents"] if doc not in submitted]
