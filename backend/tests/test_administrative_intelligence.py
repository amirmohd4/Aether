from backend.aether_core.administrative_intelligence import AdministrativeIntelligence


def test_india_admin_intelligence_exposes_department_profiles():
    intelligence = AdministrativeIntelligence()
    departments = intelligence.departments()
    assert len(departments) >= 20
    assert any(item["id"] == "revenue" for item in departments)
    assert all("legal_completeness" in item for item in departments)


def test_journey_edges_never_claim_unverified_statutory_prerequisites():
    intelligence = AdministrativeIntelligence()
    journeys = intelligence.journeys()
    assert {item["id"] for item in journeys} >= {
        "establish_hotel", "set_up_manufacturing_unit", "develop_real_estate_project"
    }
    for journey in journeys:
        assert journey["status"] == "illustrative_planning_template"
        for edge in journey["edges"]:
            assert edge["legal_basis_status"] == "not_verified"
            assert edge["is_statutory_prerequisite"] is None


def test_journey_steps_reference_registered_services_only():
    intelligence = AdministrativeIntelligence()
    for journey in intelligence.journeys():
        for step in journey["steps"]:
            assert step["service_id"] in intelligence.by_id


def test_department_matching_uses_word_boundaries_and_rejects_empty_labels():
    from backend.aether_core.administrative_intelligence import DEPARTMENT_PROFILES

    revenue = next(item for item in DEPARTMENT_PROFILES if item["id"] == "revenue")
    assert AdministrativeIntelligence._matches(revenue, "Revenue Department")
    assert not AdministrativeIntelligence._matches(revenue, "")
    assert not AdministrativeIntelligence._matches(revenue, "PreRevenue Services")
