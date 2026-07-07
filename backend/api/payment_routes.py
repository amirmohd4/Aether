from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import get_db
from models.database_models import WorkflowState

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/upi")
async def process_upi_payment(data: dict, db: Session = Depends(get_db)):
    """
    Mock UPI payment gateway.
    """
    workflow_id = data.get("workflow_id")
    amount = data.get("amount")
    upi_id = data.get("upi_id")
    
    if not workflow_id or not amount:
        raise HTTPException(status_code=400, detail="workflow_id and amount required")
    
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Simulate UPI payment processing
    payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
    success = True  # Always success for demo
    
    if success:
        if not workflow.workflow_metadata:
            workflow.workflow_metadata = {}
        workflow.workflow_metadata["payment"] = {
            "payment_id": payment_id,
            "amount": amount,
            "status": "success",
            "upi_id": upi_id,
            "paid_at": datetime.utcnow().isoformat()
        }
        workflow.current_step = "Payment Completed"
        db.commit()
    
    return {
        "payment_id": payment_id,
        "workflow_id": workflow_id,
        "status": "success" if success else "failed",
        "amount": amount,
        "message": "Payment successful" if success else "Payment failed"
    }
