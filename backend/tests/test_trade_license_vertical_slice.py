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
    assert case.process_profile_snapshot is not None
    assert case.process_profile_snapshot["status"] == "ready"

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

    assert case.requirements[0]["confidence"] == "source-backed"
    assert case.requirements[1]["confidence"] == "source-backed"
    assert case.requirements[2]["confidence"] == "authority-confirmation-required"


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


def test_trade_license_preflight_uses_source_backed_jk_requirements():
    from aether_core.requirements_engine import RequirementEngine

    requirements = RequirementEngine().discover(
        "I want to open a retail shop and apply for a municipal trade licence",
        "business",
        {"country": "India", "state": "Jammu and Kashmir", "district": "Jammu"},
        {"documents": []},
    )

    by_id = {item.id: item for item in requirements}
    assert {"business_identity", "premises", "activity"}.issubset(by_id)
    assert by_id["business_identity"].authority_status == "source_backed"
    assert by_id["premises"].authority_status == "source_backed"
    assert by_id["activity"].authority_status == "unverified"


def test_trade_license_requirements_do_not_claim_jk_rules_for_other_states():
    from aether_core.requirements_engine import RequirementEngine

    requirements = RequirementEngine().discover(
        "I want to open a retail shop and apply for a municipal trade licence",
        "business",
        {"country": "India", "state": "Punjab", "district": "Gurdaspur"},
        {"documents": []},
    )

    assert len(requirements) == 1
    assert requirements[0].id == "service_intake"
    assert requirements[0].authority_status == "registry_baseline"
    assert requirements[0].confidence == "service-registry-mvp"
