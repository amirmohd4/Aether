from typing import Dict, Any, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from models.database_models import Property, FraudDetectionLog, FraudSeverityEnum, WorkflowState
import uuid
import logging
import numpy as np
from sklearn.ensemble import IsolationForest
import json

logger = logging.getLogger(__name__)

class FraudDetectionService:
    """
    AI-powered fraud detection using Isolation Forest + Business Rules
    """
    
    def __init__(self):
        self.model = None
        self.fraud_rules = [
            "blacklisted_seller",
            "court_disputed",
            "benami_transaction",
            "sudden_price_jump",
            "ghost_applicant",
            "forged_document",
            "multiple_ownership_claims",
            "deceased_owner_transfer",
            "minor_as_owner",
            "shell_company_transfer"
        ]
    
    def train_model(self, db: Session):
        """Train Isolation Forest on mock data"""
        try:
            # Fetch all properties
            properties = db.query(Property).limit(5000).all()
            
            if len(properties) < 100:
                logger.warning("Insufficient data for training, using default model")
                return
            
            # Extract features for training
            features = []
            for prop in properties:
                feature_vector = self._extract_features(prop)
                features.append(feature_vector)
            
            features_array = np.array(features)
            
            # Train Isolation Forest
            self.model = IsolationForest(
                contamination=0.15,  # Expect 15% anomalies
                random_state=42,
                n_estimators=100
            )
            self.model.fit(features_array)
            
            logger.info(f"✅ Fraud detection model trained on {len(properties)} properties")
            
        except Exception as e:
            logger.error(f"Error training fraud detection model: {e}")
            self.model = None
    
    def _extract_features(self, property: Property) -> List[float]:
        """Extract numerical features from property for ML model"""
        features = []
        
        # Property value (normalized)
        features.append(property.property_value / 1000000)  # In millions
        
        # Property size
        features.append(property.property_size / 1000)  # In thousands sq ft
        
        # Price per sq ft
        price_per_sqft = property.property_value / max(property.property_size, 1)
        features.append(price_per_sqft / 1000)  # Normalized
        
        # Title status (encoded)
        title_encoding = {"clear": 0, "encumbered": 0.5, "disputed": 1}
        features.append(title_encoding.get(property.title_status, 0))
        
        # Number of encumbrances
        features.append(len(property.encumbrances) if property.encumbrances else 0)
        
        # Number of historical transactions
        features.append(len(property.history) if property.history else 0)
        
        # Property type encoding
        property_type_encoding = {"residential": 0, "commercial": 0.5, "agricultural": 1}
        features.append(property_type_encoding.get(property.property_type, 0))
        
        # Fraud flags count from state-specific data
        fraud_flags = property.state_specific_data.get('fraud_flags', {}) if property.state_specific_data else {}
        features.append(len(fraud_flags))
        
        return features
    
    def detect_fraud(
        self,
        db: Session,
        property_id: str,
        workflow_id: str = None
    ) -> Dict[str, Any]:
        """
        Detect fraud for a property using AI + business rules
        Returns fraud score (0-100) with explanation
        """
        
        property = db.query(Property).filter(Property.property_id == property_id).first()
        if not property:
            raise ValueError(f"Property {property_id} not found")
        
        # Run business rule checks
        rule_results = self._check_business_rules(property)
        
        # Run AI model if trained
        ml_score = 0
        if self.model:
            features = self._extract_features(property)
            anomaly_score = self.model.decision_function([features])[0]
            # Convert to 0-100 scale (more negative = more anomalous)
            ml_score = max(0, min(100, (-anomaly_score) * 20))
        
        # Combine scores
        rule_violations = sum(1 for r in rule_results if r["violated"])
        rule_score = min(100, rule_violations * 15)  # 15 points per violation
        
        # Final fraud score (weighted average)
        final_score = (ml_score * 0.4 + rule_score * 0.6)
        
        # Determine severity
        severity = self._calculate_severity(final_score)
        
        # Generate explanation
        explanation = self._generate_explanation(rule_results, ml_score, final_score)
        
        # Create fraud detection log
        fraud_log = FraudDetectionLog(
            fraud_id=f"FRAUD-{uuid.uuid4().hex[:12].upper()}",
            property_id=property_id,
            workflow_id=workflow_id,
            fraud_type="comprehensive_check",
            severity=severity,
            fraud_score=final_score,
            description=f"Detected {rule_violations} rule violations, ML anomaly score: {ml_score:.2f}",
            explanation=explanation,
            evidence=rule_results,
            resolved=False
        )
        
        db.add(fraud_log)
        db.commit()
        db.refresh(fraud_log)
        
        logger.info(f"Fraud check for {property_id}: Score={final_score:.2f}, Severity={severity}")
        
        return {
            "fraud_id": fraud_log.fraud_id,
            "property_id": property_id,
            "fraud_score": final_score,
            "severity": severity.value,
            "rule_violations": rule_violations,
            "ml_score": ml_score,
            "explanation": explanation,
            "evidence": rule_results,
            "flagged_at": fraud_log.flagged_at.isoformat()
        }
    
    def _check_business_rules(self, property: Property) -> List[Dict[str, Any]]:
        """Check 10 business rules for fraud detection"""
        
        results = []
        fraud_flags = property.state_specific_data.get('fraud_flags', {}) if property.state_specific_data else {}
        
        # Rule 1: Blacklisted seller
        results.append({
            "rule": "blacklisted_seller",
            "violated": fraud_flags.get('blacklisted_seller', False),
            "description": "Seller is on government blacklist",
            "severity": "critical"
        })
        
        # Rule 2: Court disputed property
        results.append({
            "rule": "court_disputed",
            "violated": fraud_flags.get('court_disputed', False) or property.title_status == "disputed",
            "description": "Property is under court dispute",
            "severity": "high"
        })
        
        # Rule 3: Benami transaction
        results.append({
            "rule": "benami_transaction",
            "violated": fraud_flags.get('benami_transaction', False),
            "description": "Potential benami (proxy ownership) transaction",
            "severity": "high"
        })
        
        # Rule 4: Sudden price jump > 50%
        price_jump_detected = fraud_flags.get('price_jump', False)
        if property.history and len(property.history) > 0:
            # Check if recent transaction
            last_transaction = property.history[-1] if property.history else None
            # In real system, would compare with market rate
        
        results.append({
            "rule": "sudden_price_jump",
            "violated": price_jump_detected,
            "description": "Property value increased >50% suddenly",
            "severity": "medium"
        })
        
        # Rule 5: Ghost applicant
        results.append({
            "rule": "ghost_applicant",
            "violated": fraud_flags.get('ghost_applicant', False),
            "description": "Applicant identity cannot be verified",
            "severity": "critical"
        })
        
        # Rule 6: Forged document
        results.append({
            "rule": "forged_document",
            "violated": fraud_flags.get('forged_document', False),
            "description": "Suspected forged or tampered documents",
            "severity": "critical"
        })
        
        # Rule 7: Multiple ownership claims
        results.append({
            "rule": "multiple_ownership_claims",
            "violated": fraud_flags.get('multiple_claims', False),
            "description": "Multiple parties claiming ownership",
            "severity": "high"
        })
        
        # Rule 8: Deceased owner transfer
        deceased_owner = "(Deceased)" in property.owner if property.owner else False
        results.append({
            "rule": "deceased_owner_transfer",
            "violated": fraud_flags.get('deceased_owner', False) or deceased_owner,
            "description": "Attempting to transfer property from deceased owner",
            "severity": "high"
        })
        
        # Rule 9: Minor as owner
        minor_owner = "(Minor)" in property.owner if property.owner else False
        results.append({
            "rule": "minor_as_owner",
            "violated": fraud_flags.get('minor_owner', False) or minor_owner,
            "description": "Property owner is a minor (requires guardian)",
            "severity": "medium"
        })
        
        # Rule 10: Shell company transfer
        results.append({
            "rule": "shell_company_transfer",
            "violated": fraud_flags.get('shell_company', False),
            "description": "Transfer involves suspected shell company",
            "severity": "high"
        })
        
        return results
    
    def _calculate_severity(self, fraud_score: float) -> FraudSeverityEnum:
        """Calculate severity based on fraud score"""
        if fraud_score >= 75:
            return FraudSeverityEnum.critical
        elif fraud_score >= 50:
            return FraudSeverityEnum.high
        elif fraud_score >= 25:
            return FraudSeverityEnum.medium
        else:
            return FraudSeverityEnum.low
    
    def _generate_explanation(
        self,
        rule_results: List[Dict[str, Any]],
        ml_score: float,
        final_score: float
    ) -> str:
        """Generate human-readable explanation for fraud decision"""
        
        violations = [r for r in rule_results if r["violated"]]
        
        if final_score < 25:
            explanation = f"✅ Low risk transaction (Score: {final_score:.1f}/100). "
            if violations:
                explanation += f"Minor concerns: {', '.join(v['rule'] for v in violations)}. "
            else:
                explanation += "No major red flags detected. "
        elif final_score < 50:
            explanation = f"⚠️  Medium risk transaction (Score: {final_score:.1f}/100). "
            explanation += f"Detected {len(violations)} rule violations: "
            explanation += ", ".join(v['description'] for v in violations) + ". "
            explanation += "Recommend additional verification. "
        elif final_score < 75:
            explanation = f"🚨 High risk transaction (Score: {final_score:.1f}/100). "
            explanation += f"Multiple red flags detected ({len(violations)} violations). "
            explanation += "Issues: " + ", ".join(v['description'] for v in violations) + ". "
            explanation += "Requires manual review and investigation. "
        else:
            explanation = f"🔴 CRITICAL RISK (Score: {final_score:.1f}/100). "
            explanation += f"Severe fraud indicators detected ({len(violations)} violations). "
            critical_violations = [v for v in violations if v['severity'] == 'critical']
            if critical_violations:
                explanation += "Critical issues: " + ", ".join(v['description'] for v in critical_violations) + ". "
            explanation += "IMMEDIATE MANUAL REVIEW AND INVESTIGATION REQUIRED. "
        
        if ml_score > 60:
            explanation += f"AI model also flagged unusual patterns (anomaly score: {ml_score:.1f}). "
        
        return explanation
    
    def get_fraud_alert(self, db: Session, fraud_id: str) -> FraudDetectionLog:
        """Get fraud alert details"""
        fraud_log = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.fraud_id == fraud_id
        ).first()
        
        if not fraud_log:
            raise ValueError(f"Fraud alert {fraud_id} not found")
        
        return fraud_log
    
    def resolve_fraud_alert(
        self,
        db: Session,
        fraud_id: str,
        resolution_notes: str
    ):
        """Mark fraud alert as resolved"""
        fraud_log = db.query(FraudDetectionLog).filter(
            FraudDetectionLog.fraud_id == fraud_id
        ).first()
        
        if not fraud_log:
            raise ValueError(f"Fraud alert {fraud_id} not found")
        
        fraud_log.resolved = True
        fraud_log.resolution_notes = resolution_notes
        
        db.commit()
        logger.info(f"✅ Fraud alert {fraud_id} resolved")

# Global fraud detection service
fraud_service = FraudDetectionService()
