from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.aether_core.engine import engine

router = APIRouter()


class CaseCreateRequest(BaseModel):
    objective: str = Field(min_length=3)
    customer_type: str = Field(default="citizen")
    jurisdiction: Dict[str, str] = Field(default_factory=dict)
    inputs: Dict[str, Any] = Field(default_factory=dict)


class HumanActionRequest(BaseModel):
    decision: str = Field(min_length=1)
    note: str = ""


@router.post("/cases")
def create_case(request: CaseCreateRequest):
    case = engine.create_case(
        objective=request.objective,
        customer_type=request.customer_type,
        jurisdiction=request.jurisdiction,
        inputs=request.inputs,
    )
    case = engine.execute_until_pause(case.case_id)
    return serialize_case(case)


@router.get("/cases/{case_id}")
def get_case(case_id: str):
    try:
        return serialize_case(engine.get_case(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/execute")
def execute_case(case_id: str):
    try:
        return serialize_case(engine.execute_until_pause(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/tasks/{task_id}/human-action")
def complete_human_action(case_id: str, task_id: str, request: HumanActionRequest):
    try:
        return serialize_case(engine.complete_human_task(case_id, task_id, request.decision, request.note))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case or task not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


def serialize_case(case):
    return {
        "summary": case.summary(),
        "requirements": case.requirements,
        "inputs": case.inputs,
        "exceptions": case.exceptions,
        "human_actions": case.human_actions,
        "evidence": case.evidence,
        "outcome": case.outcome,
        "tasks": [
            {
                "id": task.definition.id,
                "name": task.definition.name,
                "department": task.definition.department,
                "worker": task.definition.worker,
                "dependencies": task.definition.dependencies,
                "authority_required": task.definition.authority_required,
                "physical_action": task.definition.physical_action,
                "status": task.status.value,
                "result": task.result,
                "evidence": task.evidence,
                "error": task.error,
                "attempts": task.attempts,
            }
            for task in case.tasks.values()
        ],
    }
