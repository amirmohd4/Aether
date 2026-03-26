from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import WorkflowStartRequest, WorkflowResponse
from models.database_models import WorkflowState
from services import workflow_engine
from typing import List

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/start", response_model=dict)
async def start_workflow(
    request: WorkflowStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start a new property registration workflow
    """
    try:
        workflow = workflow_engine.start_workflow(
            db=db,
            property_id=request.property_id,
            citizen_id=request.citizen_id,
            workflow_type=request.workflow_type
        )
        
        return {
            "workflow_id": workflow.workflow_id,
            "property_id": workflow.property_id,
            "citizen_id": workflow.citizen_id,
            "workflow_type": workflow.workflow_type,
            "current_step": workflow.current_step,
            "status": workflow.status.value,
            "steps_completed": workflow.steps_completed,
            "steps_pending": workflow.steps_pending,
            "started_at": workflow.started_at.isoformat(),
            "message": "Workflow started successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{workflow_id}", response_model=dict)
async def get_workflow_status(workflow_id: str, db: Session = Depends(get_db)):
    """
    Get current status and progress of a workflow
    """
    try:
        workflow = workflow_engine.get_workflow_status(db, workflow_id)
        
        # Calculate progress percentage
        total_steps = len(workflow.steps_completed) + len(workflow.steps_pending)
        progress_percentage = (len(workflow.steps_completed) / total_steps * 100) if total_steps > 0 else 0
        
        return {
            "workflow_id": workflow.workflow_id,
            "property_id": workflow.property_id,
            "citizen_id": workflow.citizen_id,
            "workflow_type": workflow.workflow_type,
            "current_step": workflow.current_step,
            "status": workflow.status.value,
            "progress_percentage": round(progress_percentage, 2),
            "steps_completed": workflow.steps_completed,
            "steps_pending": workflow.steps_pending,
            "failure_reason": workflow.failure_reason,
            "started_at": workflow.started_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "metadata": workflow.workflow_metadata
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{workflow_id}/process-next")
async def process_next_step(workflow_id: str, db: Session = Depends(get_db)):
    """
    Manually trigger processing of next workflow step
    """
    try:
        result = workflow_engine.process_next_step(db, workflow_id)
        
        workflow = result["workflow"]
        
        return {
            "workflow_id": workflow.workflow_id,
            "status": result["status"],
            "current_step": workflow.current_step,
            "workflow_status": workflow.status.value,
            "steps_completed": workflow.steps_completed,
            "steps_pending": workflow.steps_pending,
            "message": f"Step processing: {result['status']}"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{workflow_id}/reject")
async def reject_workflow(
    workflow_id: str,
    reason: str,
    db: Session = Depends(get_db)
):
    """
    Reject a workflow
    """
    try:
        workflow_engine.reject_workflow(db, workflow_id, reason)
        
        return {
            "workflow_id": workflow_id,
            "status": "rejected",
            "reason": reason,
            "message": "Workflow rejected successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{workflow_id}/approve-manual-review")
async def approve_manual_review(workflow_id: str, db: Session = Depends(get_db)):
    """
    Approve a workflow that's in manual review and continue processing
    """
    try:
        result = workflow_engine.approve_manual_review(db, workflow_id)
        
        workflow = result["workflow"]
        
        return {
            "workflow_id": workflow.workflow_id,
            "status": workflow.status.value,
            "current_step": workflow.current_step,
            "message": "Workflow approved and resumed"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/by-property/{property_id}")
async def get_workflows_by_property(
    property_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all workflows for a property
    """
    try:
        workflows = db.query(WorkflowState).filter(
            WorkflowState.property_id == property_id
        ).all()
        
        result = []
        for workflow in workflows:
            result.append({
                "workflow_id": workflow.workflow_id,
                "workflow_type": workflow.workflow_type,
                "current_step": workflow.current_step,
                "status": workflow.status.value,
                "started_at": workflow.started_at.isoformat(),
                "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
