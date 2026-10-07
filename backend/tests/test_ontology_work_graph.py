from aether_core.ontology import GovernmentOntologyBuilder, WorkGraphBuilder
from aether_core.service_registry import ServiceRegistry
from aether_core.templates import restaurant_tasks


def test_ontology_links_case_subject_to_application_and_property():
    service = ServiceRegistry().resolve("open a restaurant", "business")
    ontology = GovernmentOntologyBuilder().build(
        {"customer_type": "business", "property_id": "P-100", "district": "Jammu"},
        "open a restaurant",
        service,
    )
    assert ontology.entities["application"].type == "Application"
    assert any(r.relation == "initiates" and r.object_id == "application" for r in ontology.relationships)
    assert any(r.relation == "owns_or_controls" and r.object_id == "property" for r in ontology.relationships)


def test_work_graph_preserves_dependencies_and_authority_boundary():
    service = ServiceRegistry().resolve("open a restaurant", "business")
    graph = WorkGraphBuilder().build(service, restaurant_tasks())
    assert graph.nodes["food_application"].dependencies == ["document_intake", "business_check"]
    assert graph.nodes["final_approval"].authority_required is True
    assert "inspection" in graph.nodes["decision_package"].dependencies
