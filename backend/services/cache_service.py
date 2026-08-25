import json
import os
from typing import Dict, Any, List
from backend.connectors import (
    KaveriConnector,
    EAssthiConnector,
    BhoomiConnector,
    LRISConnector,
    AadhaarConnector,
    DigiLockerConnector
)
from backend.config import settings
from backend.services.cache_service import cache
import logging

logger = logging.getLogger(__name__)

class ConnectorService:
    """Service to manage state-specific connectors"""

    def __init__(self):
        self.active_state = settings.active_state
        self.mock_failure = settings.mock_failure
        self.state_config = self._load_state_config()

    def _load_state_config(self):
        """Load state-specific configuration"""
        return {
            "karnataka": {
                "kaveri": KaveriConnector(),
                "eassthi": EAssthiConnector(),
                "bhoomi": BhoomiConnector()
            },
            "jammu_kashmir": {
                "lris": LRISConnector()
            },
            "generic": {
                "aadhaar": AadhaarConnector(),
                "digilocker": DigiLockerConnector()
            }
        }

    def get_connector(self, state: str, service: str):
        """Get a specific connector by state and service"""
        state_config = self.state_config.get(state.lower(), {})
        return state_config.get(service.lower())

    def get_all_connectors_for_state(self, state: str):
        """Get all connectors for a given state"""
        return self.state_config.get(state.lower(), {})

# Singleton instance
connector_service = ConnectorService()
