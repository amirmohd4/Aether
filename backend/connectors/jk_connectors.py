from .base_connector import BaseConnector
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class LRISConnector(BaseConnector):
    """J&K Land Records Information System"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "LRIS",
            "property_id": property_id,
            "lris_id": f"LRIS-{property_id[-8:]}",
            "khewat_number": f"KH-{random.randint(1000, 9999)}",
            "khasra_number": f"KS-{random.randint(100, 999)}",
            "land_type": random.choice(["Irrigated", "Barani (Rain-fed)", "Horticulture", "Forest"]),
            "total_kanals": random.uniform(1, 20),  # 1 kanal = 0.125 acres
            "total_marlas": random.randint(0, 19),  # 20 marlas = 1 kanal
            "owner_name": f"Owner-{random.randint(1000, 9999)}",
            "village": random.choice(["Srinagar", "Budgam", "Anantnag", "Baramulla"]),
            "tehsil": random.choice(["Srinagar", "Ganderbal", "Budgam"]),
            "district": "Srinagar",
            "mutation_status": random.choice(["sanctioned", "pending", "under_process"]),
            "jamabandi_year": random.randint(2020, 2024)
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        is_clear = random.random() > 0.18  # 82% clear titles
        
        return {
            "source": "LRIS",
            "property_id": property_id,
            "title_status": "clear" if is_clear else random.choice(["disputed", "state_land_dispute"]),
            "fard_verified": random.choice([True, False]),
            "verified_at": datetime.now().isoformat(),
            "verification_tehsildar": f"Tehsildar-{random.randint(100, 999)}",
            "issues": [] if is_clear else [
                random.choice([
                    "Shajra mismatch detected",
                    "Ownership documentation incomplete",
                    "Border dispute pending"
                ])
            ]
        }
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        has_encumbrance = random.random() < 0.22  # 22% have encumbrances
        
        encumbrances = []
        if has_encumbrance:
            encumbrances.append({
                "type": random.choice(["mortgage", "cooperative_loan", "revenue_arrears"]),
                "amount": random.uniform(50000, 2000000),
                "creditor": random.choice(["J&K Bank", "Cooperative Bank", "Revenue Department"]),
                "date": (datetime.now() - timedelta(days=random.randint(180, 1095))).isoformat()
            })
        
        return {
            "source": "LRIS",
            "property_id": property_id,
            "has_encumbrance": has_encumbrance,
            "encumbrances": encumbrances,
            "revenue_arrears": random.uniform(0, 10000),
            "checked_at": datetime.now().isoformat()
        }
