from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from database import SessionLocal
from models.database_models import WorkflowState

router = APIRouter(prefix="/officer", tags=["Officer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- File Noting ---
@router.post("/note")
async def add_note(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Officer adds a file note to an application.
    """
    application_id = data.get("application_id")
    note_text = data.get("note_text")
    officer_id = data.get("officer_id", "OFFICER-DEMO")
    
    if not application_id or not note_text:
        raise HTTPException(status_code=400, detail="application_id and note_text required")
    
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == application_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    if "notes" not in workflow.workflow_metadata:
        workflow.workflow_metadata["notes"] = []
    note_entry = {
        "note_id": f"NOTE-{uuid.uuid4().hex[:8].upper()}",
        "officer_id": officer_id,
        "timestamp": datetime.utcnow().isoformat(),
        "text": note_text
    }
    workflow.workflow_metadata["notes"].append(note_entry)
    db.commit()
    
    return {
        "status": "success",
        "note_id": note_entry["note_id"],
        "message": "Note added successfully"
    }

# --- Digital Signature Integration (Placeholder) ---
@router.post("/sign")
async def digital_sign(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Officer signs an application using DSC/eSign.
    """
    application_id = data.get("application_id")
    officer_id = data.get("officer_id", "OFFICER-DEMO")
    signature_data = data.get("signature_data")  # Base64 encoded signature
    
    if not application_id:
        raise HTTPException(status_code=400, detail="application_id required")
    
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == application_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    workflow.workflow_metadata["digital_signature"] = {
        "officer_id": officer_id,
        "signed_at": datetime.utcnow().isoformat(),
        "signature": signature_data or "demo-signature"
    }
    db.commit()
    
    return {
        "status": "signed",
        "message": "Document signed digitally",
        "application_id": application_id
    }

# --- Document Verification ---
@router.post("/verify-document")
async def verify_document(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Officer marks a document as verified or rejected.
    """
    application_id = data.get("application_id")
    document_type = data.get("document_type")
    verification_status = data.get("verification_status")  # "verified" or "rejected"
    officer_id = data.get("officer_id", "OFFICER-DEMO")
    
    if not application_id or not document_type or not verification_status:
        raise HTTPException(status_code=400, detail="application_id, document_type, verification_status required")
    
    workflow = db.query(WorkflowState).filter(WorkflowState.workflow_id == application_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not workflow.workflow_metadata:
        workflow.workflow_metadata = {}
    if "documents" not in workflow.workflow_metadata:
        workflow.workflow_metadata["documents"] = []
    
    workflow.workflow_metadata["documents"].append({
        "document_type": document_type,
        "verification_status": verification_status,
        "officer_id": officer_id,
        "verified_at": datetime.utcnow().isoformat()
    })
    db.commit()
    
    return {
        "status": "success",
        "message": f"Document {document_type} marked as {verification_status}"
    }
