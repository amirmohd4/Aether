from .base_connector import BaseConnector
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class KaveriConnector(BaseConnector):
    """Karnataka Kaveri Online Services - Property Registration"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "kaveri_id": f"KAV-{property_id[-8:]}",
            "registration_status": random.choice(["registered", "pending", "rejected"]),
            "registration_date": (datetime.now() - timedelta(days=random.randint(30, 3650))).isoformat(),
            "document_number": f"DOC-KAR-{random.randint(10000, 99999)}",
            "sub_registrar_office": random.choice(["Bangalore North", "Bangalore South", "Mysore", "Hubli"]),
            "stamp_duty_paid": random.uniform(50000, 500000),
            "registration_fee": random.uniform(5000, 50000)
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        is_clear = random.random() > 0.15  # 85% clear titles
        
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "title_status": "clear" if is_clear else random.choice(["disputed", "encumbered"]),
            "verified_at": datetime.now().isoformat(),
            "verification_officer": f"Officer-{random.randint(1000, 9999)}",
            "issues": [] if is_clear else [
                random.choice([
                    "Pending litigation in civil court",
                    "Multiple ownership claims",
                    "Boundary dispute with neighbor"
                ])
            ]
        }
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        has_encumbrance = random.random() < 0.2  # 20% have encumbrances
        
        encumbrances = []
        if has_encumbrance:
            encumbrances.append({
                "type": random.choice(["mortgage", "loan", "lien"]),
                "amount": random.uniform(100000, 5000000),
                "creditor": random.choice(["SBI Bank", "HDFC Bank", "Canara Bank"]),
                "date": (datetime.now() - timedelta(days=random.randint(365, 1825))).isoformat()
            })
        
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "has_encumbrance": has_encumbrance,
            "encumbrances": encumbrances,
            "checked_at": datetime.now().isoformat()
        }


class EAasthiConnector(BaseConnector):
    """Karnataka eAasthi - Urban Property Tax System"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "eAasthi",
            "property_id": property_id,
            "e_aasthi_id": f"EA-{property_id[-8:]}",
            "property_tax_id": f"TAX-{random.randint(100000, 999999)}",
            "annual_tax": random.uniform(5000, 50000),
            "tax_arrears": random.uniform(0, 20000),
            "last_payment_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            "property_usage": random.choice(["Residential", "Commercial", "Mixed"]),
            "built_up_area_sqft": random.randint(500, 5000)
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "eAasthi",
            "property_id": property_id,
            "tax_compliance": random.choice(["compliant", "arrears"]),
            "verified_at": datetime.now().isoformat()
        }
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "eAasthi",
            "property_id": property_id,
            "tax_lien": random.random() < 0.1,  # 10% have tax liens
            "checked_at": datetime.now().isoformat()
        }


class BhoomiConnector(BaseConnector):
    """Karnataka Bhoomi - Rural Land Records"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "bhoomi_id": f"BH-{property_id[-8:]}",
            "survey_number": f"{random.randint(1, 500)}/{random.randint(1, 10)}",
            "hissa_number": f"{random.randint(1, 20)}",
            "land_type": random.choice(["Agricultural", "Non-Agricultural", "Dry", "Irrigated"]),
            "total_extent_acres": random.uniform(0.5, 50),
            "owner_name": f"Owner-{random.randint(1000, 9999)}",
            "village": random.choice(["Devanahalli", "Nelamangala", "Doddaballapur"]),
            "taluk": random.choice(["Bangalore North", "Bangalore Rural"]),
            "mutation_status": random.choice(["completed", "pending"])
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "title_status": random.choice(["clear", "disputed", "unclear"]),
            "pahani_verified": random.choice([True, False]),
            "verified_at": datetime.now().isoformat()
        }
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "has_encumbrance": random.random() < 0.15,
            "agricultural_loan": random.random() < 0.1,
            "checked_at": datetime.now().isoformat()
        }
