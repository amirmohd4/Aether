from aether_core.engine import AetherExecutionEngine
from aether_core.domain import TaskStatus


def test_every_resolvable_case_gets_internal_admin_lane():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": ["identity_document"]},
    )

    assert case.tasks["internal_case_triage"].definition.worker == "AdministrativeWorker"
    assert case.tasks["internal_case_file"].definition.dependencies == ["internal_case_triage"]
    assert case.tasks["internal_data_normalization"].definition.worker == "AdministrativeWorker"
    assert case.tasks["internal_correspondence"].definition.operation == "correspondence"
    assert case.tasks["internal_followup_plan"].definition.operation == "followup_plan"
    assert case.tasks["internal_case_closeout"].definition.operation == "case_closeout"


def test_internal_admin_work_executes_automatically():
    engine = AetherExecutionEngine()
    case = engine.create_case(
        objective="I want to register a company",
        customer_type="business",
        jurisdiction={"country": "India", "state": "Jammu and Kashmir"},
        inputs={"documents": [
            "identity_document",
            "address_proof",
            "business_registration",
        ], "owner_user_id": "admin-test", "tenant_id": "tenant-test"},
    )
    case = engine.execute_until_pause(case.case_id)

    assert case.tasks["internal_case_triage"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_case_file"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_data_normalization"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_correspondence"].status == TaskStatus.COMPLETED
    assert case.tasks["internal_followup_plan"].status == TaskStatus.COMPLETED
