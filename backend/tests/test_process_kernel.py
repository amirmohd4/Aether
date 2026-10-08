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


def test_india_service_family_catalog_expanded():
    engine = AetherExecutionEngine()
    catalog = engine.services.catalog()

    assert len(catalog) >= 100
    ids = {item["id"] for item in catalog}
    assert {"gst_return_filing", "property_tax_payment", "fire_noc", "old_age_pension", "rtI_application"}.issubset(ids)

    assert engine.services.resolve("I need a property tax receipt", "citizen").id == "property_tax_payment"
    assert engine.services.resolve("I need a fire NOC for my building", "business").id == "fire_noc"


def test_process_kernel_falls_back_by_department_for_new_family():
    engine = AetherExecutionEngine()
    service = engine.services.get("property_tax_payment")
    profile = infer_process_profile(service)

    assert profile.key == "municipal_license"
    assert profile.payment_sensitive is True


def test_external_service_catalog_loader_json(tmp_path):
    from aether_core.service_catalog_loader import load_records

    path = tmp_path / "services.json"
    path.write_text(
        '{"services":[{"id":"example_service","name":"Example Service","department":"Revenue","customer_types":["citizen"],"keywords":["example"]}]}',
        encoding="utf-8",
    )
    rows = load_records(path)

    assert rows[0][0] == "example_service"
    assert rows[0][1] == "Example Service"
    assert rows[0][3] == ["citizen"]
