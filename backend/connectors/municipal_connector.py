from .base_connector import BaseConnector
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class MunicipalZoningConnector(BaseConnector):
    """Municipal Zoning and Land Use Connector"""
    
    LAND_USE_TYPES = {
        'agricultural': ['agricultural', 'horticulture', 'farm_house'],
        'residential': ['residential', 'mixed_residential', 'apartment'],
        'commercial': ['commercial', 'retail', 'office', 'mixed_use'],
        'industrial': ['industrial', 'warehouse', 'manufacturing']
    }
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        current_use = random.choice(['agricultural', 'residential', 'commercial', 'industrial'])
        
        return {
            "source": "Municipal Zoning",
            "property_id": property_id,
            "municipal_id": f"MUN-{property_id[-8:]}",
            "current_land_use": current_use,
            "zoning_category": random.choice(['Zone-A', 'Zone-B', 'Zone-C', 'Special Economic Zone']),
            "master_plan_2035": random.choice(['Residential', 'Commercial', 'Mixed Use', 'Green Belt']),
            "fsi_allowed": random.uniform(1.0, 3.5),
            "height_restriction_meters": random.choice([12, 18, 24, 30, None]),
            "setback_requirements": {
                "front": random.randint(3, 10),
                "side": random.randint(2, 5),
                "rear": random.randint(3, 8)
            }
        }
    
    def get_allowed_conversions(self, property_id: str, current_use: str) -> Dict[str, Any]:
        """Get allowed land use conversions"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        # Get allowed conversions based on current use
        all_uses = ['agricultural', 'residential', 'commercial', 'industrial']
        current_category = current_use if current_use in all_uses else 'agricultural'
        
        # Some conversions are allowed, some aren't
        allowed = []
        for use in all_uses:
            if use != current_category:
                # Agricultural can convert to residential/commercial more easily
                if current_category == 'agricultural' and use in ['residential', 'commercial']:
                    allowed.append({
                        "target_use": use,
                        "allowed": True,
                        "conversion_fee_percentage": random.uniform(5, 15),
                        "approval_required": random.choice([True, False]),
                        "restrictions": []
                    })
                # Residential to commercial might have restrictions
                elif current_category == 'residential' and use == 'commercial':
                    allowed.append({
                        "target_use": use,
                        "allowed": random.choice([True, False]),
                        "conversion_fee_percentage": random.uniform(10, 25),
                        "approval_required": True,
                        "restrictions": ["Ground floor commercial only", "Parking requirements"]
                    })
                # Industrial conversions usually harder
                elif use == 'industrial':
                    allowed.append({
                        "target_use": use,
                        "allowed": random.choice([True, False]),
                        "conversion_fee_percentage": random.uniform(20, 40),
                        "approval_required": True,
                        "restrictions": ["Environmental clearance required", "Pollution control board approval"]
                    })
        
        return {
            "source": "Municipal Zoning",
            "property_id": property_id,
            "current_use": current_category,
            "allowed_conversions": allowed,
            "checked_at": datetime.now().isoformat()
        }
    
    def calculate_conversion_fee(self, property_id: str, property_value: float, conversion_type: str) -> Dict[str, Any]:
        """Calculate land use conversion fee"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        # Fee is percentage of property value
        fee_percentage = random.uniform(5, 25)
        base_fee = property_value * (fee_percentage / 100)
        
        # Additional charges
        processing_fee = random.uniform(5000, 20000)
        inspection_fee = random.uniform(3000, 10000)
        
        total_fee = base_fee + processing_fee + inspection_fee
        
        return {
            "source": "Municipal Zoning",
            "property_id": property_id,
            "conversion_type": conversion_type,
            "base_fee": base_fee,
            "processing_fee": processing_fee,
            "inspection_fee": inspection_fee,
            "total_fee": total_fee,
            "fee_breakdown": {
                "percentage_of_value": fee_percentage,
                "property_value": property_value
            },
            "calculated_at": datetime.now().isoformat()
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {}
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        return {}
