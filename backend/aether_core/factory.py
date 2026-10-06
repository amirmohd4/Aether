from __future__ import annotations

import uuid
from typing import Any, Dict

from .domain import Case, TaskState
from .requirements_engine import RequirementEngine
from .templates import TEMPLATES, infer_template


def create_case(objective: str, customer_type: str, jurisdiction: Dict[str, str], inputs: Dict[str, Any]) -> Case:
    template_name = infer_template(objective, customer_type)
    requirement_fn, task_fn = TEMPLATES[template_name]
    requirements = RequirementEngine().discover(objective, customer_type, jurisdiction, inputs)
    task_defs = task_fn()
    tasks = {d.id: TaskState(definition=d) for d in task_defs}
    return Case(
        case_id=f"CASE-{uuid.uuid4().hex[:10].upper()}",
        objective=objective,
        customer_type=customer_type,
        jurisdiction=jurisdiction,
        inputs=inputs,
        requirements=[r.__dict__ for r in requirements],
        tasks=tasks,
    )
