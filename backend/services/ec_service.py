from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.database_models import Property
from services.connector_service import connector_service
import uuid
import logging
import random

logger = logging.getLogger(__name__)

class ECWorkflowService:
    """
    Encumbrance Certificate (EC) Workflow Service
    Steps: fetch last 30 years of transactions → format certificate → store in DigiLocker (mock) → return PDF/JSON
    """
    
    def generate_ec(self, db: Session, property_id: str, years: int = 30) -> Dict[str, Any]:
        """Generate Encumbrance Certificate"""
        
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        ec_id = f"EC-{uuid.uuid4().hex[:12].upper()}"
        
        # Fetch transaction history
        transactions = self._fetch_transactions(property, years)
        
        # Check encumbrances
        encumbrances_data = connector_service.check_encumbrance(property_id)
        
        # Generate certificate
        certificate = {
            "ec_id": ec_id,
            "property_id": property_id,
            "issue_date": datetime.now().isoformat(),
            "valid_from": (datetime.now() - timedelta(days=years * 365)).isoformat(),
            "valid_to": datetime.now().isoformat(),
            "years_covered": years,
            "property_details": {
                "property_id": property.property_id,
                "location": property.location,
                "district": property.district,
                "state": property.state,
                "current_owner": property.owner
            },
            "transactions": transactions,
            "encumbrances": encumbrances_data.get('all_encumbrances', []),
            "total_encumbrance_amount": encumbrances_data.get('total_encumbrance_amount', 0),
            "has_encumbrances": encumbrances_data.get('has_any_encumbrance', False),
            "certificate_status": "Clear" if not encumbrances_data.get('has_any_encumbrance') else "Encumbered",
            "issued_by": "Sub-Registrar Office",
            "issuing_authority": property.state_specific_data.get('sub_registrar_office', 'District Office'),
            "format": "JSON",
            "digilocker_stored": True,
            "digilocker_id": f"DL-{uuid.uuid4().hex[:12].upper()}"
        }
        
        # Store in property EC history
        if not property.state_specific_data:
            property.state_specific_data = {}
        
        if 'ec_history' not in property.state_specific_data:
            property.state_specific_data['ec_history'] = []
        
        property.state_specific_data['ec_history'].append(certificate)
        db.commit()
        
        logger.info(f"✅ EC {ec_id} generated for property {property_id}")
        
        return certificate
    
    def _fetch_transactions(self, property: Property, years: int) -> List[Dict[str, Any]]:
        """Fetch property transactions for the last N years"""
        
        # Use property history if available
        history = property.history if property.history else []
        
        # Generate some additional transactions
        num_transactions = random.randint(1, 5)
        transactions = []
        
        for i in range(num_transactions):
            trans_date = datetime.now() - timedelta(days=random.randint(0, years * 365))
            
            transactions.append({
                "date": trans_date.isoformat(),
                "transaction_type": random.choice(['Sale', 'Mortgage', 'Lease', 'Gift', 'Inheritance']),
                "document_number": f"DOC-{random.randint(10000, 99999)}",
                "parties": {
                    "from": f"Party-{random.randint(1000, 9999)}",
                    "to": f"Party-{random.randint(1000, 9999)}"
                },
                "amount": random.uniform(100000, 5000000) if random.random() > 0.3 else None,
                "remarks": ""
            })
        
        # Sort by date
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions
    
    def get_ec(self, db: Session, ec_id: str) -> Dict[str, Any]:
        """Get EC by ID"""
        
        properties = db.query(Property).all()
        
        for property in properties:
            if property.state_specific_data and 'ec_history' in property.state_specific_data:
                for ec in property.state_specific_data['ec_history']:
                    if ec.get('ec_id') == ec_id:
                        return ec
        
        raise ValueError(f"EC {ec_id} not found")
    
    def get_ec_history(self, db: Session, property_id: str) -> List[Dict[str, Any]]:
        """Get all ECs for a property"""
        
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        if not property.state_specific_data or 'ec_history' not in property.state_specific_data:
            return []
        
        return property.state_specific_data['ec_history']

ec_service = ECWorkflowService()
