import json
import os
from typing import Dict, Any, List
from connectors import (
    KaveriConnector, EAasthiConnector, BhoomiConnector,
    LRISConnector, AadhaarConnector, DigiLockerConnector
)
from config import settings
from services.cache_service import cache
import logging

logger = logging.getLogger(__name__)

class ConnectorService:
    """Service to manage state-specific connectors"""
    
    def __init__(self):
        self.active_state = settings.active_state
        self.mock_failure = settings.mock_failure
        self.state_config = self._load_state_config()
        self.connectors = self._initialize_connectors()
    
    def _load_state_config(self) -> Dict[str, Any]:
        """Load configuration for active state"""
        config_path = f"/app/configs/{self.active_state}.json"
        
        if not os.path.exists(config_path):
            logger.warning(f"Config not found for state: {self.active_state}, using default")
            config_path = "/app/configs/karnataka.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        logger.info(f"✅ Loaded config for {config['state_name']}")
        return config
    
    def _initialize_connectors(self) -> Dict[str, Any]:
        """Initialize connectors based on state configuration"""
        connectors = {}
        connector_config = self.state_config.get('connectors', {})
        
        # Map connector names to classes
        connector_classes = {
            'KaveriConnector': KaveriConnector,
            'EAasthiConnector': EAasthiConnector,
            'BhoomiConnector': BhoomiConnector,
            'LRISConnector': LRISConnector,
            'AadhaarConnector': AadhaarConnector,
            'DigiLockerConnector': DigiLockerConnector
        }
        
        for service_type, connector_name in connector_config.items():
            if connector_name in connector_classes:
                connectors[service_type] = connector_classes[connector_name](
                    config=self.state_config,
                    mock_failure=self.mock_failure
                )
                logger.info(f"   Initialized {connector_name} for {service_type}")
        
        # Always initialize generic connectors
        if 'identity' not in connectors:
            connectors['identity'] = AadhaarConnector(self.state_config, self.mock_failure)
        if 'documents' not in connectors:
            connectors['documents'] = DigiLockerConnector(self.state_config, self.mock_failure)
        
        return connectors
    
    def fetch_property_unified(self, property_id: str) -> Dict[str, Any]:
        """
        Fetch unified property data from all relevant connectors
        Uses cache-first strategy with fallback
        """
        cache_key = f"property:{self.active_state}:{property_id}"
        
        # Try cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"✅ Cache hit for property {property_id}")
            cached_data['_source'] = 'cache'
            return cached_data
        
        # Fetch from connectors
        unified_data = {
            "property_id": property_id,
            "state": self.active_state,
            "connector_data": {},
            "fetch_timestamp": None
        }
        
        try:
            # Property registration system
            if 'property_registration' in self.connectors:
                connector = self.connectors['property_registration']
                try:
                    data = connector.fetch_property_data(property_id)
                    unified_data['connector_data']['property_registration'] = data
                except Exception as e:
                    logger.error(f"Property registration connector failed: {e}")
                    unified_data['connector_data']['property_registration'] = {"error": str(e)}
            
            # Additional state-specific connectors
            for service_type, connector in self.connectors.items():
                if service_type not in ['property_registration', 'identity', 'documents']:
                    try:
                        data = connector.fetch_property_data(property_id)
                        if data:  # Only add if data is returned
                            unified_data['connector_data'][service_type] = data
                    except Exception as e:
                        logger.error(f"{service_type} connector failed: {e}")
            
            from datetime import datetime
            unified_data['fetch_timestamp'] = datetime.now().isoformat()
            unified_data['_source'] = 'connectors'
            
            # Cache the result
            cache.set(cache_key, unified_data, ttl=300)
            
            return unified_data
            
        except Exception as e:
            logger.error(f"Error fetching property data: {e}")
            
            # Try to serve stale cache on complete failure
            stale_cache = cache.get(cache_key)
            if stale_cache:
                logger.warning(f"Serving stale cache for property {property_id}")
                stale_cache['_source'] = 'stale_cache'
                return stale_cache
            
            raise
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        """Verify property title across all relevant connectors"""
        cache_key = f"title:{self.active_state}:{property_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        verification_results = {
            "property_id": property_id,
            "state": self.active_state,
            "verifications": []
        }
        
        try:
            for service_type, connector in self.connectors.items():
                if service_type in ['property_registration', 'urban_property', 'rural_land', 'land_records']:
                    try:
                        result = connector.verify_title(property_id)
                        if result:
                            verification_results['verifications'].append(result)
                    except Exception as e:
                        logger.error(f"Title verification failed for {service_type}: {e}")
            
            # Determine overall status
            statuses = [v.get('title_status') for v in verification_results['verifications']]
            if 'disputed' in statuses:
                verification_results['overall_status'] = 'disputed'
            elif 'encumbered' in statuses:
                verification_results['overall_status'] = 'encumbered'
            elif any(statuses):
                verification_results['overall_status'] = 'clear'
            else:
                verification_results['overall_status'] = 'unknown'
            
            cache.set(cache_key, verification_results, ttl=600)
            return verification_results
            
        except Exception as e:
            logger.error(f"Error in title verification: {e}")
            raise
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        """Check encumbrances across all relevant connectors"""
        cache_key = f"encumbrance:{self.active_state}:{property_id}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        encumbrance_results = {
            "property_id": property_id,
            "state": self.active_state,
            "checks": [],
            "all_encumbrances": []
        }
        
        try:
            for service_type, connector in self.connectors.items():
                if service_type in ['property_registration', 'urban_property', 'rural_land', 'land_records']:
                    try:
                        result = connector.check_encumbrance(property_id)
                        if result:
                            encumbrance_results['checks'].append(result)
                            if result.get('has_encumbrance') and result.get('encumbrances'):
                                encumbrance_results['all_encumbrances'].extend(result['encumbrances'])
                    except Exception as e:
                        logger.error(f"Encumbrance check failed for {service_type}: {e}")
            
            encumbrance_results['has_any_encumbrance'] = len(encumbrance_results['all_encumbrances']) > 0
            encumbrance_results['total_encumbrance_amount'] = sum(
                enc.get('amount', 0) for enc in encumbrance_results['all_encumbrances']
            )
            
            cache.set(cache_key, encumbrance_results, ttl=600)
            return encumbrance_results
            
        except Exception as e:
            logger.error(f"Error in encumbrance check: {e}")
            raise
    
    def verify_citizen(self, aadhaar_number: str) -> Dict[str, Any]:
        """Verify citizen via Aadhaar"""
        cache_key = f"citizen:{aadhaar_number}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            aadhaar_connector = self.connectors.get('identity')
            if aadhaar_connector and hasattr(aadhaar_connector, 'verify_citizen'):
                result = aadhaar_connector.verify_citizen(aadhaar_number)
                cache.set(cache_key, result, ttl=1800)  # Cache for 30 minutes
                return result
            else:
                raise Exception("Aadhaar connector not available")
        except Exception as e:
            logger.error(f"Citizen verification failed: {e}")
            raise
    
    def get_workflow_steps(self) -> List[Dict[str, Any]]:
        """Get workflow steps for the active state"""
        return self.state_config.get('workflow_steps', [])
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get state configuration info"""
        return {
            "state": self.state_config.get('state'),
            "state_name": self.state_config.get('state_name'),
            "languages": self.state_config.get('languages'),
            "stamp_duty_rate": self.state_config.get('stamp_duty_rate'),
            "registration_fee_rate": self.state_config.get('registration_fee_rate'),
            "processing_days": self.state_config.get('processing_days'),
            "districts": self.state_config.get('districts'),
            "document_requirements": self.state_config.get('document_requirements')
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all connectors"""
        health_status = {
            "state": self.active_state,
            "connectors": {}
        }
        
        for service_type, connector in self.connectors.items():
            status = connector.get_connector_status()
            health_status['connectors'][service_type] = status
        
        # Overall health
        all_online = all(
            conn['status'] == 'online' 
            for conn in health_status['connectors'].values()
        )
        health_status['overall_status'] = 'healthy' if all_online else 'degraded'
        
        return health_status

# Global connector service instance
connector_service = ConnectorService()
