from aether_core.engine import AetherExecutionEngine


def test_trade_license_uses_its_own_municipal_workflow_and_unverified_rule_boundary():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        "I want to open a retail shop and apply for a municipal trade licence",
        "business",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": ["identity_document", "business_registration", "lease_or_ownership"]},
    )

    assert case.service_id == "trade_license"
    assert case.service_name == "Trade License"
    assert case.process_profile_snapshot is None

    task_ids = set(case.tasks)
    assert {
        "entity_check",
        "premises_check",
        "activity_check",
        "applicable_clearance_screen",
        "case_reconciliation",
        "decision_package",
        "final_approval",
        "record_update",
        "licence_output",
    }.issubset(task_ids)
    assert "food_application" not in task_ids
    assert "fire_application" not in task_ids

    assert all(
        item.get("confidence") == "jurisdiction-verification-required"
        for item in case.requirements
    )


def test_trade_license_workflow_pauses_at_authorised_municipal_decision():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        "I want to open a retail shop and apply for a municipal trade licence",
        "business",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": ["identity_document", "business_registration", "lease_or_ownership"]},
    )

    paused = engine.execute_until_pause(case.case_id)
    assert paused.status == "waiting_for_human"
    assert any(action["task_id"] == "final_approval" for action in paused.human_actions)



def test_jk_trade_license_profile_is_source_backed_and_effective_dated():
    from aether_core.jurisdiction_process_profiles import JurisdictionProcessRegistry

    registry = JurisdictionProcessRegistry()
    readiness = registry.readiness(
        "trade_license",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
    )

    assert readiness["status"] == "ready"
    assert readiness["effective_date"] == "2022-10-29"
    assert readiness["verified_at"] == "2026-11-22"
    assert "singlewindow.jk.gov.in" in readiness["source_url"]
    assert len(readiness["required_documents"]) == 3
    assert readiness["service_level"]["days"] == 30
