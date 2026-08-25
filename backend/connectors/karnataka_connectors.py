import random
from datetime import datetime, timedelta
from typing import Dict, Any
from backend.connectors.base_connector import BaseConnector


class KaveriConnector(BaseConnector):
    """Kaveri - Karnataka Land Records System"""

    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "title_verified": True,
            "verified_at": datetime.now().isoformat()
        }

    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "survey_number": f"SUR-{random.randint(1000, 9999)}",
            "owner_name": f"Owner_{random.randint(1, 100)}",
            "area_sqft": random.randint(1000, 10000),
            "fetched_at": datetime.now().isoformat()
        }

    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "Kaveri",
            "property_id": property_id,
            "has_encumbrance": random.choice([True, False]),
            "encumbrances": [],
            "checked_at": datetime.now().isoformat()
        }


class EAssthiConnector(BaseConnector):
    """Karnataka eAstshi - Urban Property Tax System"""

    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "eAstshi",
            "property_id": property_id,
            "title_verified": True,
            "verified_at": datetime.now().isoformat()
        }

    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "eAstshi",
            "property_id": property_id,
            "e_assthi_id": f"EA-{property_id[-8:]}",
            "property_tax_id": f"TAX-{random.randint(100000, 999999)}",
            "annual_tax": random.uniform(5000, 50000),
            "tax_arrears": random.uniform(0, 20000),
            "last_payment_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
        }

    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "eAstshi",
            "property_id": property_id,
            "has_encumbrance": random.choice([True, False]),
            "checked_at": datetime.now().isoformat()
        }


class BhoomiConnector(BaseConnector):
    """Bhoomi - Karnataka Land Records"""

    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "title_verified": True,
            "verified_at": datetime.now().isoformat()
        }

    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "land_use": random.choice(["Agricultural", "Residential", "Commercial"]),
            "soil_type": random.choice(["Black", "Red", "Alluvial"]),
            "fertility_score": random.uniform(0, 100),
            "fetched_at": datetime.now().isoformat()
        }

    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        return {
            "source": "Bhoomi",
            "property_id": property_id,
            "has_encumbrance": random.choice([True, False]),
            "checked_at": datetime.now().isoformat()
        }
