from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random
import time

class BaseConnector(ABC):
    """Base class for all government system connectors"""
    
    def __init__(self, config: Dict[str, Any], mock_failure: bool = False):
        self.config = config
        self.mock_failure = mock_failure
        self.name = self.__class__.__name__
    
    def _simulate_network_delay(self):
        """Simulate realistic network delay"""
        time.sleep(random.uniform(0.1, 0.5))
    
    def _check_mock_failure(self):
        """Simulate random failures when mock_failure is enabled"""
        if self.mock_failure and random.random() < 0.2:  # 20% failure rate
            raise ConnectionError(f"{self.name}: Simulated connection failure")
    
    @abstractmethod
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        """Fetch property data from the system"""
        pass
    
    @abstractmethod
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        """Verify property title"""
        pass
    
    @abstractmethod
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        """Check property encumbrances"""
        pass
    
    def get_connector_status(self) -> Dict[str, Any]:
        """Get connector health status"""
        try:
            self._simulate_network_delay()
            self._check_mock_failure()
            return {
                "connector": self.name,
                "status": "online",
                "response_time_ms": random.randint(100, 500)
            }
        except Exception as e:
            return {
                "connector": self.name,
                "status": "offline",
                "error": str(e)
            }
