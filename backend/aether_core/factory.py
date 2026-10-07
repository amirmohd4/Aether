from __future__ import annotations

import uuid
from typing import Any, Dict

from .domain import Case, TaskState
from .requirements_engine import RequirementEngine
from .service_registry import ServiceRegistry
from .templates import TEMPLATES, generic_tasks, infer_template


def create_case(
    objective: str,
    customer_type: str,
    jurisdiction: Dict[str, str],
    inputs: Dict[str, Any],
) -> Case:
    """Backward-compatible factory using the same registry as the V2 engine."""
    registry = ServiceRegistry()
    service = registry.resolve(objective, customer_type)
    template_name = infer_template(objective, customer_type, service)

    if template_name in TEMPLATES:
        requirement_fn, task_fn = TEMPLATES[template_name]
        task_defs = task_fn()
    elif service:
        task_defs = generic_tasks(service)
    else:
        requirement_fn = None
        task_defs = []

    requirements = RequirementEngine(registry).discover(
        objective, customer_type, jurisdiction, inputs
    )
    tasks = {definition.id: TaskState(definition=definition) for definition in task_defs}

    return Case(
        case_id=f"CASE-{uuid.uuid4().hex[:10].upper()}",
        objective=objective,
        customer_type=customer_type,
        jurisdiction=jurisdiction,
        inputs=inputs,
        requirements=[r.__dict__ for r in requirements],
        tasks=tasks,
        service_id=service.id if service else None,
        service_name=service.name if service else None,
        service_department=service.department if service else None,
        service_outcome=service.outcome if service else None,
    )
