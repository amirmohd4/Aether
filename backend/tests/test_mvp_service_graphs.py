from aether_core.service_registry import ServiceRegistry
from aether_core.templates import generic_tasks


def _assert_acyclic(task_map):
    visiting = set()
    visited = set()

    def visit(task_id):
        if task_id in visiting:
            raise AssertionError(f"cycle detected at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in task_map[task_id].dependencies:
            assert dependency in task_map, f"{task_id} depends on missing task {dependency}"
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in task_map:
        visit(task_id)


def test_every_mvp_service_has_an_executable_baseline_graph():
    registry = ServiceRegistry()

    assert len(registry.all()) >= 34

    for service in registry.all():
        tasks = generic_tasks(service)
        task_map = {task.id: task for task in tasks}

        assert "document_intake" in task_map
        assert "identity_check" in task_map
        assert "decision_package" in task_map
        assert "outcome" in task_map

        _assert_acyclic(task_map)

        # Outcome must remain downstream of the final decision boundary:
        # directly or through the authorised human step.
        outcome_dependencies = set(task_map["outcome"].dependencies)
        assert outcome_dependencies & {"decision_package", "final_approval"}

        if service.human_authority_required:
            assert "final_approval" in task_map
            assert task_map["final_approval"].authority_required
            assert "decision_package" in task_map["final_approval"].dependencies


def test_service_document_defaults_do_not_cross_domain_boundaries():
    registry = ServiceRegistry()

    company_docs = registry.get("company_registration").documents()
    rera_docs = registry.get("rera_registration").documents()
    property_docs = registry.get("property_registration").documents()

    assert "property_record" not in company_docs
    assert "property_record" not in rera_docs
    assert "property_record" in property_docs


def test_customer_type_limits_service_resolution():
    registry = ServiceRegistry()

    assert registry.resolve("I want a new passport", "citizen").id == "passport"
    assert registry.resolve("I want to incorporate a company", "business").id == "company_registration"
    assert registry.resolve("I need a scholarship", "citizen").id == "scholarship"
    assert registry.resolve("I need a scholarship", "business") is None
