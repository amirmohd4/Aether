from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.database_models import WorkflowState

router = APIRouter(prefix="/construction", tags=["Construction"])

@router.post("/progress/{workflow_id}")
async def update_construction_progress(
    workflow_id: str,
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Update construction progress (plinth, structure, completion)
    """
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    progress = data.get("progress", {})  # { "plinth": "completed", "structure": "in_progress", "completion": "pending" }
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    workflow.workflow_metadata["construction_progress"] = progress
    db.commit()
    
    return {
        "workflow_id": workflow_id,
        "progress": progress,
        "updated_at": datetime.utcnow().isoformat()
    }

@router.post("/oc/{workflow_id}")
async def issue_occupancy_certificate(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Issue Occupancy Certificate (OC) if all construction stages completed.
    """
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    progress = workflow.workflow_metadata.get("construction_progress", {})
    required_stages = ["plinth", "structure", "completion"]
    all_done = all(progress.get(stage) == "completed" for stage in required_stages)
    
    if not all_done:
        return {
            "workflow_id": workflow_id,
            "oc_issued": False,
            "message": "Construction not fully completed. Pending: " + ", ".join([s for s in required_stages if progress.get(s) != "completed"])
        }
    
    # Issue OC
    oc_id = f"OC-{datetime.utcnow().strftime('%Y%m%d')}-{workflow_id[:4]}"
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    workflow.workflow_metadata["occupancy_certificate"] = {
        "oc_id": oc_id,
        "issued_at": datetime.utcnow().isoformat(),
        "status": "issued"
    }
    workflow.current_step = "Occupancy Certificate Issued"
    workflow.status = "completed"
    db.commit()
    
    return {
        "workflow_id": workflow_id,
        "oc_issued": True,
        "oc_id": oc_id,
        "issued_at": datetime.utcnow().isoformat()
    }
