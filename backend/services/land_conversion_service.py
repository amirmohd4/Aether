from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from models.database_models import Property
from connectors.municipal_connector import MunicipalZoningConnector
import uuid
import logging

logger = logging.getLogger(__name__)

class LandConversionWorkflowService:
    """
    Land Use Conversion Workflow Service
    Steps: fetch current land use → check zoning rules → calculate conversion fee → payment → update land use category
    """
    
    def __init__(self):
        self.municipal_connector = MunicipalZoningConnector(config={}, mock_failure=False)
        self.steps = [
            {"step_name": "fetch_current_use", "display_name": "Fetch Current Land Use"},
            {"step_name": "check_zoning", "display_name": "Check Zoning Rules"},
            {"step_name": "calculate_fee", "display_name": "Calculate Conversion Fee"},
            {"step_name": "payment", "display_name": "Payment Processing"},
            {"step_name": "update_land_use", "display_name": "Update Land Use Category"}
        ]
    
    def start_conversion(self, db: Session, property_id: str, target_use: str) -> Dict[str, Any]:
        """Start land use conversion workflow"""
        
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        conversion_id = f"CONV-{uuid.uuid4().hex[:12].upper()}"
        
        workflow_data = {
            "conversion_id": conversion_id,
            "property_id": property_id,
            "target_use": target_use,
            "status": "in_progress",
            "current_step": "fetch_current_use",
            "steps": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Process workflow
        result = self._process_workflow(db, property, workflow_data, target_use)
        
        # Update property conversion history
        if not property.state_specific_data:
            property.state_specific_data = {}
        
        if 'land_use_conversions' not in property.state_specific_data:
            property.state_specific_data['land_use_conversions'] = []
        
        property.state_specific_data['land_use_conversions'].append(result)
        db.commit()
        
        logger.info(f"✅ Land conversion workflow {conversion_id} started for property {property_id}")
        
        return result
    
    def _process_workflow(self, db: Session, property: Property, workflow_data: Dict[str, Any], target_use: str) -> Dict[str, Any]:
        """Process all workflow steps"""
        
        for step in self.steps:
            step_name = step['step_name']
            
            try:
                if step_name == 'fetch_current_use':
                    result = self._fetch_current_use(property)
                    workflow_data['current_use'] = result['current_land_use']
                elif step_name == 'check_zoning':
                    result = self._check_zoning_rules(property, workflow_data['current_use'], target_use)
                    if not result.get('allowed', True):
                        raise Exception(f"Conversion to {target_use} not allowed: {result.get('reason')}")
                elif step_name == 'calculate_fee':
                    result = self._calculate_conversion_fee(property, target_use)
                    workflow_data['conversion_fee'] = result['total_fee']
                elif step_name == 'payment':
                    result = self._process_payment(workflow_data['conversion_id'], workflow_data['conversion_fee'])
                elif step_name == 'update_land_use':
                    result = self._update_land_use(property, target_use)
                
                workflow_data['steps'].append({
                    "step_name": step_name,
                    "display_name": step['display_name'],
                    "status": "completed",
                    "completed_at": datetime.now().isoformat(),
                    "result": result
                })
                
            except Exception as e:
                workflow_data['status'] = 'failed'
                workflow_data['failure_reason'] = str(e)
                workflow_data['current_step'] = step_name
                logger.error(f"Land conversion workflow step {step_name} failed: {e}")
                return workflow_data
        
        workflow_data['status'] = 'completed'
        workflow_data['completed_at'] = datetime.now().isoformat()
        
        # Update property type
        property.property_type = target_use
        db.commit()
        
        return workflow_data
    
    def _fetch_current_use(self, property: Property) -> Dict[str, Any]:
        """Fetch current land use from municipal records"""
        return self.municipal_connector.fetch_property_data(property.property_id)
    
    def _check_zoning_rules(self, property: Property, current_use: str, target_use: str) -> Dict[str, Any]:
        """Check if conversion is allowed under zoning rules"""
        conversions_data = self.municipal_connector.get_allowed_conversions(property.property_id, current_use)
        
        allowed_conversions = conversions_data.get('allowed_conversions', [])
        
        for conversion in allowed_conversions:
            if conversion['target_use'] == target_use:
                return {
                    "allowed": conversion['allowed'],
                    "conversion_details": conversion,
                    "checked_at": datetime.now().isoformat()
                }
        
        # If not in allowed list, default to allowed with high fee
        return {
            "allowed": True,
            "conversion_details": {
                "target_use": target_use,
                "allowed": True,
                "conversion_fee_percentage": 20,
                "approval_required": True
            },
            "checked_at": datetime.now().isoformat()
        }
    
    def _calculate_conversion_fee(self, property: Property, target_use: str) -> Dict[str, Any]:
        """Calculate conversion fee"""
        return self.municipal_connector.calculate_conversion_fee(
            property.property_id,
            property.property_value,
            target_use
        )
    
    def _process_payment(self, conversion_id: str, amount: float) -> Dict[str, Any]:
        """Process conversion fee payment"""
        import random
        
        payment_success = random.random() > 0.05
        
        return {
            "payment_id": f"PAY-{uuid.uuid4().hex[:12].upper()}",
            "amount": amount,
            "status": "success" if payment_success else "failed",
            "timestamp": datetime.now().isoformat()
        }
    
    def _update_land_use(self, property: Property, target_use: str) -> Dict[str, Any]:
        """Update land use in records"""
        return {
            "record_updated": True,
            "previous_use": property.property_type,
            "new_use": target_use,
            "conversion_order_number": f"CO-{uuid.uuid4().hex[:8].upper()}",
            "updated_at": datetime.now().isoformat()
        }
    
    def get_status(self, db: Session, conversion_id: str) -> Dict[str, Any]:
        """Get conversion workflow status"""
        properties = db.query(Property).all()
        
        for property in properties:
            if property.state_specific_data and 'land_use_conversions' in property.state_specific_data:
                for conversion in property.state_specific_data['land_use_conversions']:
                    if conversion.get('conversion_id') == conversion_id:
                        return conversion
        
        raise ValueError(f"Conversion {conversion_id} not found")

land_conversion_service = LandConversionWorkflowService()
