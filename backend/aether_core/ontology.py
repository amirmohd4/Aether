from __future__ import annotations

from typing import Any, Dict, List

from .domain import GovernmentOntology, OntologyEntity, OntologyRelationship, WorkGraph, WorkNode
from .service_registry import ServiceDefinition


ENTITY_TYPES = [
    "Person", "Property", "LandParcel", "Company", "Project", "Vehicle",
    "License", "Certificate", "Application", "Document", "Payment",
    "Department", "Officer", "Location", "CourtCase", "TaxRecord", "Transaction",
]


class GovernmentOntologyBuilder:
    """Builds a deterministic case ontology from structured inputs."""

    def build(self, inputs: Dict[str, Any], objective: str, service: ServiceDefinition | None = None) -> GovernmentOntology:
        ontology = GovernmentOntology()
        subject_id = "subject"
        customer_type = inputs.get("customer_type", "unknown")
        ontology.add_entity(OntologyEntity(subject_id, "Person" if customer_type == "citizen" else "Company", "Case subject", {"customer_type": customer_type}))

        for key, value in inputs.items():
            if key in {"customer_type", "documents"} or value in (None, ""):
                continue
            if key in {"property_id", "property", "land_parcel", "parcel_id"}:
                eid = "property"
                ontology.add_entity(OntologyEntity(eid, "Property", str(value), {"source_field": key}))
                ontology.add_relationship(OntologyRelationship(subject_id, "owns_or_controls", eid))
            elif key in {"company_id", "company"}:
                eid = "company"
                ontology.add_entity(OntologyEntity(eid, "Company", str(value), {"source_field": key}))
                ontology.add_relationship(OntologyRelationship(subject_id, "represents", eid))
            elif key in {"project_id", "project"}:
                eid = "project"
                ontology.add_entity(OntologyEntity(eid, "Project", str(value), {"source_field": key}))
                ontology.add_relationship(OntologyRelationship(subject_id, "owns_or_develops", eid))
            elif key in {"vehicle_id", "vehicle"}:
                eid = "vehicle"
                ontology.add_entity(OntologyEntity(eid, "Vehicle", str(value), {"source_field": key}))
                ontology.add_relationship(OntologyRelationship(subject_id, "owns", eid))
            elif key in {"location", "district", "state"}:
                eid = f"location_{key}"
                ontology.add_entity(OntologyEntity(eid, "Location", str(value), {"source_field": key}))
                ontology.add_relationship(OntologyRelationship(subject_id, "located_in", eid))

        ontology.add_entity(OntologyEntity("application", "Application", objective, {"service_id": service.id if service else None}))
        ontology.add_relationship(OntologyRelationship(subject_id, "initiates", "application"))
        return ontology


class WorkGraphBuilder:
    """Converts service task definitions into an explicit executable graph."""

    def build(self, service: ServiceDefinition | None, task_definitions: List[Any]) -> WorkGraph:
        graph = WorkGraph()
        for task in task_definitions:
            graph.add(WorkNode(
                id=task.id,
                task_id=task.id,
                department=task.department,
                worker=task.worker,
                action=task.name,
                dependencies=list(task.dependencies),
                authority_required=task.authority_required,
                physical_action=task.physical_action,
                reason=f"Required by service {service.id}" if service else "Required by selected process",
            ))
        return graph
