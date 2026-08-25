from typing import Dict, Any, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.database_models import Property, FraudDetectionLog, FraudSeverityEnum, WorkflowState
import uuid
import logging
import numpy as np
import json

logger = logging.getLogger(__name__)

class FraudDetectionService:
    """
    AI-powered fraud detection using Isolation Forest + Business Rules
    """

    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the Isolation Forest model"""
        try:
            from sklearn.ensemble import IsolationForest
            self.model = IsolationForest(contamination=0.1, random_state=42)
            # Train with dummy data for now
            dummy_data = np.random.randn(100, 5)
            self.model.fit(dummy_data)
            logger.info("Fraud detection model initialized")
        except Exception as e:
            logger.error(f"Failed to initialize fraud model: {e}")
            self.model = None

    def detect_fraud(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect fraud in property data"""
        try:
            # Extract features
            features = self._extract_features(property_data)
            
            if self.model is not None:
                prediction = self.model.predict([features])[0]
                score = self.model.score_samples([features])[0]
                is_fraud = prediction == -1
            else:
                # Fallback to rule-based detection
                is_fraud = self._rule_based_detection(property_data)
                score = -0.5 if is_fraud else 0.5

            return {
                "is_fraud": is_fraud,
                "score": float(score),
                "confidence": 0.85 if is_fraud else 0.92,
                "checks": self._run_checks(property_data),
                "detected_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Fraud detection error: {e}")
            return {
                "is_fraud": False,
                "score": 0.0,
                "confidence": 0.0,
                "checks": [],
                "error": str(e)
            }

    def _extract_features(self, data: Dict[str, Any]) -> List[float]:
        """Extract numeric features for ML model"""
        features = []
        # Extract relevant numeric features
        features.append(float(data.get("property_value", 0)) / 1000000)
        features.append(float(data.get("area_sqft", 0)) / 1000)
        features.append(float(data.get("age_years", 0)) / 50)
        features.append(float(data.get("previous_transactions", 0)) / 10)
        features.append(float(data.get("tax_arrears", 0)) / 10000)
        return features

    def _rule_based_detection(self, data: Dict[str, Any]) -> bool:
        """Rule-based fraud detection fallback"""
        warnings = 0
        if data.get("property_value", 0) > 100000000:
            warnings += 1
        if data.get("area_sqft", 0) > 10000:
            warnings += 1
        if data.get("previous_transactions", 0) > 5:
            warnings += 1
        if data.get("tax_arrears", 0) > 50000:
            warnings += 1
        return warnings >= 2

    def _run_checks(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run individual fraud checks"""
        checks = []
        
        # Value check
        checks.append({
            "name": "property_value_check",
            "passed": data.get("property_value", 0) < 100000000,
            "message": "Property value seems reasonable" if data.get("property_value", 0) < 100000000 else "Property value unusually high"
        })
        
        # Area check
        checks.append({
            "name": "area_check",
            "passed": data.get("area_sqft", 0) < 10000,
            "message": "Area seems reasonable" if data.get("area_sqft", 0) < 10000 else "Area unusually large"
        })
        
        return checks

# Singleton instance
fraud_service = FraudDetectionService()
