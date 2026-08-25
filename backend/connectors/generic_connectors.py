import random
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from .base_connector import BaseConnector


class AadhaarConnector(BaseConnector):
    """Aadhaar API Connector for identity verification"""

    def verify_identity(self, aadhaar_number: str, name: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()

        # Simulate Aadhaar verification
        is_valid = len(aadhaar_number) == 12 and aadhaar_number.isdigit()

        return {
            "source": "Aadhaar",
            "aadhaar_number": aadhaar_number[-4:],
            "name": name,
            "verified": is_valid,
            "timestamp": datetime.now().isoformat()
        }


class DigiLockerConnector(BaseConnector):
    """DigiLocker API Connector for document retrieval"""

    def fetch_document(self, document_id: str, user_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()

        # Simulate document fetch
        return {
            "source": "DigiLocker",
            "document_id": document_id,
            "user_id": user_id,
            "document_name": f"document_{document_id}.pdf",
            "size_kb": random.randint(100, 5000),
            "fetched_at": datetime.now().isoformat()
        }
