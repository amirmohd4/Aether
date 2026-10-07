from aether_core.ontology import WorkGraphBuilder
from aether_core.service_registry import ServiceRegistry
from aether_core.templates import generic_tasks, infer_template


def test_service_registry_handles_plain_language_aliases():
    registry = ServiceRegistry()
    service = registry.resolve("I need to get a new water supply connection", "citizen")
    assert service is not None
    assert service.id == "water_connection"


def test_property_service_gets_cross_department_execution_graph():
    registry = ServiceRegistry()
    service = registry.get("title_verification")
    assert service is not None

    tasks = generic_tasks(service)
    by_id = {task.id: task for task in tasks}

    assert {"identity_check", "land_record", "registration_record", "court_search", "tax_dues"} <= set(by_id)
    assert by_id["court_search"].dependencies == ["document_intake"]
    assert by_id["registration_record"].dependencies == ["document_intake"]
    assert by_id["tax_dues"].dependencies == ["land_record"]
    assert by_id["decision_package"].dependencies == ["cross_record_reconciliation"]
    assert by_id["final_approval"].authority_required is True


def test_specialized_templates_are_not_selected_for_unrelated_single_services():
    registry = ServiceRegistry()
    trade = registry.get("trade_license")
    food = registry.get("food_business_license")
    property = registry.get("property_registration")

    assert trade is not None and infer_template("I need a municipal trade licence", "business", trade) == "generic"
    assert food is not None and infer_template("I want to open a restaurant", "business", food) == "restaurant"
    assert property is not None and infer_template("I want to register a property", "citizen", property) == "generic"


def test_generic_tasks_carry_explicit_connector_operations():
    registry = ServiceRegistry()
    service = registry.get("water_connection")
    assert service is not None

    tasks = generic_tasks(service)
    operations = {task.id: task.operation for task in tasks}

    assert operations["document_intake"] == "document"
    assert operations["identity_check"] == "identity"
    assert operations["department_processing"] == "service_processing"
    assert operations["verification"] == "reconciliation"
    assert operations["outcome"] == "outcome"


def test_work_graph_preserves_task_operation_metadata():
    registry = ServiceRegistry()
    service = registry.get("water_connection")
    assert service is not None

    tasks = generic_tasks(service)
    graph = WorkGraphBuilder().build(service, tasks)
    assert graph.nodes["department_processing"].operation == "service_processing"
    assert graph.nodes["verification"].operation == "reconciliation"
