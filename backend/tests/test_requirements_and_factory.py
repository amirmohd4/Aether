from aether_core.factory import create_case


def test_restaurant_objective_creates_requirements_and_work_graph():
    case = create_case(
        "I want to open a restaurant",
        "developer",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": ["identity_document"]},
    )
    assert case.case_id.startswith("CASE-")
    assert any(r["id"] == "fire" for r in case.requirements)
    assert "final_approval" in case.tasks
    assert "food_application" in case.tasks


def test_bank_objective_gets_property_verification_requirements():
    case = create_case(
        "Verify this property for a bank loan",
        "bank",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {},
    )
    assert any(r["id"] == "property" for r in case.requirements)
    assert "court_search" in case.tasks
    assert "risk_reconciliation" in case.tasks
