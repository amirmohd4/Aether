from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .api_models import HumanDecisionRequest, StartCaseRequest
from .case_store import InMemoryCaseStore
from .engine import ExecutionEngine
from .factory import create_case

router = APIRouter(prefix="/api/aether/v2", tags=["Aether V2"])
store = InMemoryCaseStore()
engine = ExecutionEngine()


def serialize(case):
    return {
        "summary": case.summary(),
        "requirements": case.requirements,
        "tasks": {
            task_id: {
                "name": state.definition.name,
                "department": state.definition.department,
                "worker": state.definition.worker,
                "dependencies": state.definition.dependencies,
                "status": state.status.value,
                "authority_required": state.definition.authority_required,
                "physical_action": state.definition.physical_action,
                "result": state.result,
                "error": state.error,
                "evidence": state.evidence,
            }
            for task_id, state in case.tasks.items()
        },
        "human_actions": case.human_actions,
        "exceptions": case.exceptions,
        "evidence": case.evidence,
        "outcome": case.outcome,
    }


@router.post("/cases")
def start_case(request: StartCaseRequest):
    case = create_case(request.objective, request.customer_type, request.jurisdiction, request.inputs)
    store.put(case)
    engine.execute(case)
    store.put(case)
    return serialize(case)


@router.get("/cases/{case_id}")
def get_case(case_id: str):
    try:
        return serialize(store.get(case_id))
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")


@router.post("/cases/{case_id}/human/{task_id}")
def human_decision(case_id: str, task_id: str, request: HumanDecisionRequest):
    try:
        case = store.get(case_id)
        case = engine.complete_human_task(case, task_id, request.approved, request.note or "")
        store.put(case)
        return serialize(case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case or task not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
