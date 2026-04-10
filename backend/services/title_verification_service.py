from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from models.database_models import Property
from connectors.court_connector import CourtRecordsConnector
from connectors.generic_connectors import AadhaarConnector
import uuid
import logging
import random

logger = logging.getLogger(__name__)

class TitleVerificationService:
    """
    Title Verification Workflow Service
    Steps: fetch ownership chain → check pending disputes → verify owner identity → generate title report with risk score
    """
    
    def __init__(self):
        self.court_connector = CourtRecordsConnector(config={}, mock_failure=False)
        self.aadhaar_connector = AadhaarConnector(config={}, mock_failure=False)
        self.steps = [
            {"step_name": "fetch_ownership_chain", "display_name": "Fetch Ownership Chain"},
            {"step_name": "check_disputes", "display_name": "Check Court Disputes"},
            {"step_name": "verify_identity", "display_name": "Verify Owner Identity"},
            {"step_name": "generate_report", "display_name": "Generate Title Report"}
        ]
    
    def verify_title(self, db: Session, property_id: str, owner_aadhaar: str = None) -> Dict[str, Any]:
        """Verify property title"""
        
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        verification_id = f"TITLE-{uuid.uuid4().hex[:12].upper()}"
        
        workflow_data = {
            "verification_id": verification_id,
            "property_id": property_id,
            "status": "in_progress",
            "current_step": "fetch_ownership_chain",
            "steps": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Process workflow
        result = self._process_workflow(db, property, workflow_data, owner_aadhaar)
        
        # Update property title verification history
        if not property.state_specific_data:
            property.state_specific_data = {}
        
        if 'title_verifications' not in property.state_specific_data:
            property.state_specific_data['title_verifications'] = []
        
        property.state_specific_data['title_verifications'].append(result)
        db.commit()
        
        logger.info(f"✅ Title verification {verification_id} completed for property {property_id}")
        
        return result
    
    def _process_workflow(self, db: Session, property: Property, workflow_data: Dict[str, Any], owner_aadhaar: str) -> Dict[str, Any]:
        """Process all workflow steps"""
        
        ownership_chain = None
        disputes_data = None
        identity_data = None
        
        for step in self.steps:
            step_name = step['step_name']
            
            try:
                if step_name == 'fetch_ownership_chain':
                    result = self._fetch_ownership_chain(property)
                    ownership_chain = result
                elif step_name == 'check_disputes':
                    result = self._check_disputes(property)
                    disputes_data = result
                elif step_name == 'verify_identity':
                    result = self._verify_identity(property, owner_aadhaar)
                    identity_data = result
                elif step_name == 'generate_report':
                    result = self._generate_title_report(
                        property,
                        ownership_chain,
                        disputes_data,
                        identity_data
                    )
                    workflow_data['title_report'] = result
                
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
                logger.error(f"Title verification workflow step {step_name} failed: {e}")
                return workflow_data
        
        workflow_data['status'] = 'completed'
        workflow_data['completed_at'] = datetime.now().isoformat()
        
        return workflow_data
    
    def _fetch_ownership_chain(self, property: Property) -> Dict[str, Any]:
        """Fetch 30-year ownership chain"""
        return self.court_connector.get_ownership_chain(property.property_id, years=30)
    
    def _check_disputes(self, property: Property) -> Dict[str, Any]:
        """Check for pending court disputes"""
        return self.court_connector.get_dispute_status(property.property_id)
    
    def _verify_identity(self, property: Property, aadhaar_number: str = None) -> Dict[str, Any]:
        """Verify owner identity via Aadhaar"""
        
        if not aadhaar_number:
            # Generate mock Aadhaar for testing
            aadhaar_number = f"{random.randint(100000000000, 999999999999)}"
        
        return self.aadhaar_connector.verify_citizen(aadhaar_number)
    
    def _generate_title_report(self, property: Property, ownership_chain: Dict, disputes_data: Dict, identity_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive title report with risk score"""
        
        # Calculate risk score
        risk_score = 0
        risk_factors = []
        
        # Check ownership chain
        if not ownership_chain.get('chain_complete'):
            risk_score += 20
            risk_factors.append("Incomplete ownership chain")
        
        if ownership_chain.get('gaps_found'):
            risk_score += 15
            risk_factors.append("Gaps found in ownership history")
        
        # Check disputes
        dispute_risk = disputes_data.get('risk_score', 0)
        risk_score += dispute_risk * 0.5  # 50% weight
        
        if disputes_data.get('has_disputes'):
            risk_factors.append(f"{disputes_data.get('total_cases', 0)} court cases found")
        
        # Check identity verification
        if not identity_data.get('is_valid'):
            risk_score += 30
            risk_factors.append("Owner identity verification failed")
        
        # Check property title status
        if property.title_status == 'disputed':
            risk_score += 40
            risk_factors.append("Property title is disputed")
        elif property.title_status == 'encumbered':
            risk_score += 20
            risk_factors.append("Property has encumbrances")
        
        # Cap at 100
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score < 20:
            risk_level = "Very Low"
            recommendation = "Title is clear and safe for transaction"
        elif risk_score < 40:
            risk_level = "Low"
            recommendation = "Minor concerns, proceed with caution"
        elif risk_score < 60:
            risk_level = "Medium"
            recommendation = "Moderate risk, legal advice recommended"
        elif risk_score < 80:
            risk_level = "High"
            recommendation = "Significant risk, thorough due diligence required"
        else:
            risk_level = "Critical"
            recommendation = "High risk, avoid transaction without resolving issues"
        
        return {
            "report_id": f"TR-{uuid.uuid4().hex[:12].upper()}",
            "property_id": property.property_id,
            "report_date": datetime.now().isoformat(),
            "title_status": property.title_status,
            "current_owner": property.owner,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "ownership_chain_summary": {
                "years_covered": 30,
                "transfers": len(ownership_chain.get('ownership_chain', [])),
                "chain_complete": ownership_chain.get('chain_complete'),
                "gaps_found": ownership_chain.get('gaps_found')
            },
            "dispute_summary": {
                "has_disputes": disputes_data.get('has_disputes'),
                "total_cases": disputes_data.get('total_cases', 0),
                "active_cases": disputes_data.get('active_cases', 0),
                "dispute_risk_score": disputes_data.get('risk_score', 0)
            },
            "identity_verification": {
                "verified": identity_data.get('is_valid', False),
                "verification_method": "Aadhaar"
            },
            "validity": "90 days",
            "issued_by": "Aether GovOS Title Verification Service"
        }
    
    def get_verification(self, db: Session, verification_id: str) -> Dict[str, Any]:
        """Get title verification by ID"""
        properties = db.query(Property).all()
        
        for property in properties:
            if property.state_specific_data and 'title_verifications' in property.state_specific_data:
                for verification in property.state_specific_data['title_verifications']:
                    if verification.get('verification_id') == verification_id:
                        return verification
        
        raise ValueError(f"Title verification {verification_id} not found")

title_service = TitleVerificationService()
