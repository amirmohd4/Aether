from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus
from aether_core.government_process_kernel import infer_process_profile


def test_process_kernel_assigns_deep_employee_work():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to open a restaurant",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document",
            "lease_or_ownership",
            "business_registration",
        ]},
    )

    expected = {
        "internal_assignment",
        "internal_form_prep",
        "internal_case_notes",
        "internal_deficiency",
        "internal_sla_snapshot",
        "internal_decision_brief",
        "internal_post_decision",
        "internal_case_closeout",
    }
    assert expected.issubset(case.tasks.keys())
    assert infer_process_profile(engine.services.get("food_business_license")).key == "food_license"


def test_deep_employee_work_executes_before_statutory_boundary():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to build a commercial project",
        customer_type="developer",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document",
            "business_registration",
            "site_plan",
            "building_plan",
        ]},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_assignment"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_form_prep"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_case_notes"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_deficiency"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_decision_brief"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_inspection_packet"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_post_decision"].status != TaskStatus.COMPLETED
