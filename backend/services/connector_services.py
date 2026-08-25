import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConnectorService:
    """Service to manage state-specific connectors - SIMPLIFIED VERSION"""

    def __init__(self):
        # Don't instantiate connectors in __init__ to avoid abstract class errors
        self.active_state = "karnataka"
        self.mock_failure = False
        logger.info("ConnectorService initialized with lazy loading")

    def get_connector(self, state: str, service: str):
        """Get a specific connector by state and service - Lazy loaded"""
        try:
            # Import connectors only when needed (lazy loading)
            from backend.connectors import (
                KaveriConnector, EAssthiConnector, BhoomiConnector,
                LRISConnector, AadhaarConnector, DigiLockerConnector
            )
            
            # Map state and service to connector class
            connector_map = {
                ("karnataka", "kaveri"): KaveriConnector,
                ("karnataka", "eassthi"): EAssthiConnector,
                ("karnataka", "bhoomi"): BhoomiConnector,
                ("jammu_kashmir", "lris"): LRISConnector,
                ("generic", "aadhaar"): AadhaarConnector,
                ("generic", "digilocker"): DigiLockerConnector
            }
            
            connector_class = connector_map.get((state.lower(), service.lower()))
            if connector_class:
                # Return an instance with empty config
                return connector_class(config={})
            return None
        except Exception as e:
            logger.error(f"Error getting connector: {e}")
            return None

    def get_all_connectors_for_state(self, state: str) -> Dict[str, Any]:
        """Get all connectors for a given state - Lazy loaded"""
        try:
            # Import connectors only when needed
            from backend.connectors import (
                KaveriConnector, EAssthiConnector, BhoomiConnector,
                LRISConnector, AadhaarConnector, DigiLockerConnector
            )
            
            state_connectors = {
                "karnataka": {
                    "kaveri": KaveriConnector(config={}),
                    "eassthi": EAssthiConnector(config={}),
                    "bhoomi": BhoomiConnector(config={})
                },
                "jammu_kashmir": {
                    "lris": LRISConnector(config={})
                },
                "generic": {
                    "aadhaar": AadhaarConnector(config={}),
                    "digilocker": DigiLockerConnector(config={})
                }
            }
            return state_connectors.get(state.lower(), {})
        except Exception as e:
            logger.error(f"Error loading state connectors: {e}")
            return {}

# Singleton instance
connector_service = ConnectorService()
