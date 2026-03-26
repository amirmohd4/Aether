from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.database_models import WorkflowState, WorkflowStatusEnum, Property
from services.connector_service import connector_service
import uuid
import logging

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """
    Workflow engine for property registration
    Steps: title verification → encumbrance check → stamp duty → payment → registration → mutation
    """
    
    def __init__(self):
        self.workflow_steps = connector_service.get_workflow_steps()
        self.state_info = connector_service.get_state_info()
    
    def start_workflow(
        self,
        db: Session,
        property_id: str,
        citizen_id: str,
        workflow_type: str = "property_registration"
    ) -> WorkflowState:
        """Start a new workflow"""
        
        # Verify property exists
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        workflow_id = f"WF-{str(uuid.uuid4())[:8].upper()}"
        
        # Prepare workflow steps
        steps_pending = [
            {
                "step_name": step["step_name"],
                "display_name": step["display_name"],
                "required_days": step["required_days"],
                "status": "pending"
            }
            for step in self.workflow_steps
        ]
        
        workflow = WorkflowState(
            workflow_id=workflow_id,
            property_id=property_id,
            citizen_id=citizen_id,
            workflow_type=workflow_type,
            current_step=self.workflow_steps[0]["step_name"],
            status=WorkflowStatusEnum.in_progress,
            steps_completed=[],
            steps_pending=steps_pending,
            workflow_metadata={
                "state": self.state_info["state"],
                "started_by": citizen_id,
                "estimated_completion": (
                    datetime.now() + timedelta(days=self.state_info["processing_days"])
                ).isoformat()
            }
        )
        
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        
        logger.info(f"✅ Started workflow {workflow_id} for property {property_id}")
        
        # Automatically process first step
        self.process_next_step(db, workflow_id)
        
        return workflow
    
    def process_next_step(self, db: Session, workflow_id: str) -> Dict[str, Any]:
        """Process the next step in the workflow"""
        
        workflow = db.query(WorkflowState).filter(
            WorkflowState.workflow_id == workflow_id
        ).first()
        
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status == WorkflowStatusEnum.completed:
            return {"status": "already_completed", "workflow": workflow}
        
        if workflow.status == WorkflowStatusEnum.rejected:
            return {"status": "rejected", "workflow": workflow}
        
        current_step_name = workflow.current_step
        current_step_config = next(
            (s for s in self.workflow_steps if s["step_name"] == current_step_name),
            None
        )
        
        if not current_step_config:
            raise ValueError(f"Step {current_step_name} not found in configuration")
        
        try:
            # Execute step based on type
            step_result = self._execute_step(
                workflow.property_id,
                current_step_name,
                current_step_config
            )
            
            if step_result["success"]:
                # Mark step as completed
                workflow.steps_completed.append({
                    "step_name": current_step_name,
                    "display_name": current_step_config["display_name"],
                    "completed_at": datetime.now().isoformat(),
                    "result": step_result.get("data", {}),
                    "status": "completed"
                })
                
                # Update steps_pending
                workflow.steps_pending = [
                    s for s in workflow.steps_pending 
                    if s["step_name"] != current_step_name
                ]
                
                # Move to next step or complete
                if workflow.steps_pending:
                    workflow.current_step = workflow.steps_pending[0]["step_name"]
                    workflow.status = WorkflowStatusEnum.in_progress
                else:
                    workflow.status = WorkflowStatusEnum.completed
                    workflow.completed_at = datetime.now()
                    logger.info(f"✅ Workflow {workflow_id} completed")
                
                db.commit()
                db.refresh(workflow)
                
                return {"status": "step_completed", "workflow": workflow}
            
            else:
                # Step failed - enter manual review
                workflow.status = WorkflowStatusEnum.manual_review
                workflow.failure_reason = step_result.get("error", "Unknown error")
                
                workflow.steps_completed.append({
                    "step_name": current_step_name,
                    "display_name": current_step_config["display_name"],
                    "completed_at": datetime.now().isoformat(),
                    "status": "failed",
                    "error": step_result.get("error")
                })
                
                db.commit()
                db.refresh(workflow)
                
                logger.warning(f"⚠️  Workflow {workflow_id} entered manual review")
                
                return {"status": "manual_review_required", "workflow": workflow}
        
        except Exception as e:
            logger.error(f"Error processing workflow step: {e}")
            workflow.status = WorkflowStatusEnum.manual_review
            workflow.failure_reason = str(e)
            db.commit()
            raise
    
    def _execute_step(
        self,
        property_id: str,
        step_name: str,
        step_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a specific workflow step"""
        
        try:
            if step_name == "title_verification":
                result = connector_service.verify_title(property_id)
                
                if result.get('overall_status') == 'disputed':
                    return {
                        "success": False,
                        "error": "Title is disputed - requires manual review"
                    }
                
                return {"success": True, "data": result}
            
            elif step_name == "encumbrance_check":
                result = connector_service.check_encumbrance(property_id)
                
                # Check if encumbrance amount is too high
                if result.get('total_encumbrance_amount', 0) > 5000000:
                    return {
                        "success": False,
                        "error": f"High encumbrance amount: ₹{result['total_encumbrance_amount']}"
                    }
                
                return {"success": True, "data": result}
            
            elif step_name == "stamp_duty_calculation":
                # Calculate stamp duty based on property value
                property_data = connector_service.fetch_property_unified(property_id)
                
                # This would fetch from DB in real scenario
                property_value = 1000000  # Mock value
                stamp_duty = property_value * self.state_info["stamp_duty_rate"]
                registration_fee = property_value * self.state_info["registration_fee_rate"]
                
                result = {
                    "property_value": property_value,
                    "stamp_duty": stamp_duty,
                    "registration_fee": registration_fee,
                    "total_payable": stamp_duty + registration_fee
                }
                
                return {"success": True, "data": result}
            
            elif step_name == "payment":
                # Mock payment processing
                import random
                payment_success = random.random() > 0.05  # 95% success rate
                
                if not payment_success:
                    return {
                        "success": False,
                        "error": "Payment gateway failure - please retry"
                    }
                
                result = {
                    "payment_id": f"PAY-{uuid.uuid4().hex[:12].upper()}",
                    "payment_status": "success",
                    "payment_method": "online",
                    "timestamp": datetime.now().isoformat()
                }
                
                return {"success": True, "data": result}
            
            elif step_name == "registration":
                # Mock registration process
                result = {
                    "registration_number": f"REG-{uuid.uuid4().hex[:12].upper()}",
                    "registration_date": datetime.now().isoformat(),
                    "registrar_office": "Mock Sub-Registrar Office",
                    "status": "registered"
                }
                
                return {"success": True, "data": result}
            
            elif step_name == "mutation":
                # Mock mutation process
                result = {
                    "mutation_number": f"MUT-{uuid.uuid4().hex[:12].upper()}",
                    "mutation_date": datetime.now().isoformat(),
                    "tehsil_office": "Mock Tehsil Office",
                    "status": "mutated"
                }
                
                return {"success": True, "data": result}
            
            else:
                # Unknown step - mark as success for MVP
                logger.warning(f"Unknown step: {step_name}, marking as success")
                return {"success": True, "data": {"step": step_name, "status": "completed"}}
        
        except Exception as e:
            logger.error(f"Error executing step {step_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def get_workflow_status(self, db: Session, workflow_id: str) -> WorkflowState:
        """Get current status of a workflow"""
        workflow = db.query(WorkflowState).filter(
            WorkflowState.workflow_id == workflow_id
        ).first()
        
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        return workflow
    
    def reject_workflow(self, db: Session, workflow_id: str, reason: str):
        """Reject a workflow"""
        workflow = db.query(WorkflowState).filter(
            WorkflowState.workflow_id == workflow_id
        ).first()
        
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = WorkflowStatusEnum.rejected
        workflow.failure_reason = reason
        workflow.completed_at = datetime.now()
        
        db.commit()
        logger.info(f"❌ Workflow {workflow_id} rejected: {reason}")
    
    def approve_manual_review(self, db: Session, workflow_id: str):
        """Approve a workflow in manual review and continue processing"""
        workflow = db.query(WorkflowState).filter(
            WorkflowState.workflow_id == workflow_id
        ).first()
        
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status != WorkflowStatusEnum.manual_review:
            raise ValueError(f"Workflow {workflow_id} is not in manual review")
        
        workflow.status = WorkflowStatusEnum.in_progress
        workflow.failure_reason = None
        db.commit()
        
        logger.info(f"✅ Workflow {workflow_id} approved from manual review")
        
        # Continue processing
        return self.process_next_step(db, workflow_id)

# Global workflow engine instance
workflow_engine = WorkflowEngine()
