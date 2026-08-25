import random
from datetime import datetime
from typing import Dict, Any
from backend.connectors.base_connector import BaseConnector


class LRISConnector(BaseConnector):
    """Jammu & Kashmir LRIS - Land Records Information System"""

    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "LRIS",
            "property_id": property_id,
            "title_verified": True,
            "verified_at": datetime.now().isoformat()
        }

    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "LRIS",
            "property_id": property_id,
            "lris_id": f"LR-{random.randint(10000, 99999)}",
            "land_category": random.choice(["Urban", "Rural"]),
            "accession_number": f"ACC-{random.randint(1000, 9999)}",
            "fetched_at": datetime.now().isoformat()
        }

    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "LRIS",
            "property_id": property_id,
            "has_encumbrance": random.choice([True, False]),
            "checked_at": datetime.now().isoformat()
        }
