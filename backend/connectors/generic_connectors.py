from .base_connector import BaseConnector
from typing import Dict, Any
import random
from datetime import datetime, timedelta

class AadhaarConnector(BaseConnector):
    """UIDAI Aadhaar Verification Service"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        # Aadhaar doesn't have property data
        return {}
    
    def verify_citizen(self, aadhaar_number: str) -> Dict[str, Any]:
        """Verify Aadhaar and fetch citizen details"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        # Check for fraud patterns
        is_valid = random.random() > 0.05  # 95% valid Aadhaar
        
        if not is_valid:
            return {
                "source": "Aadhaar",
                "aadhaar_number": aadhaar_number,
                "is_valid": False,
                "error": random.choice([
                    "Aadhaar number not found",
                    "Aadhaar marked as deceased",
                    "Aadhaar suspended"
                ]),
                "verified_at": datetime.now().isoformat()
            }
        
        return {
            "source": "Aadhaar",
            "aadhaar_number": aadhaar_number,
            "is_valid": True,
            "name": f"Citizen-{aadhaar_number[-4:]}",
            "date_of_birth": (datetime.now() - timedelta(days=random.randint(7300, 25550))).strftime("%Y-%m-%d"),
            "age": random.randint(20, 70),
            "gender": random.choice(["Male", "Female", "Other"]),
            "address_on_file": True,
            "mobile_verified": random.choice([True, False]),
            "email_verified": random.choice([True, False]),
            "verified_at": datetime.now().isoformat()
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {}
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        return {}


class DigiLockerConnector(BaseConnector):
    """DigiLocker Document Verification Service"""
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        return {}
    
    def fetch_citizen_documents(self, citizen_id: str) -> Dict[str, Any]:
        """Fetch citizen's uploaded documents from DigiLocker"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        has_documents = random.random() > 0.1  # 90% have documents
        
        documents = []
        if has_documents:
            doc_types = ["aadhaar", "pan_card", "driving_license", "voter_id"]
            num_docs = random.randint(1, len(doc_types))
            
            for doc_type in random.sample(doc_types, num_docs):
                documents.append({
                    "document_type": doc_type,
                    "document_id": f"DL-{doc_type.upper()}-{random.randint(10000, 99999)}",
                    "issued_by": random.choice(["UIDAI", "Income Tax Dept", "Transport Dept", "Election Commission"]),
                    "issue_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).isoformat(),
                    "verified": random.choice([True, False])
                })
        
        return {
            "source": "DigiLocker",
            "citizen_id": citizen_id,
            "documents_available": has_documents,
            "documents": documents,
            "fetched_at": datetime.now().isoformat()
        }
    
    def verify_document(self, document_id: str) -> Dict[str, Any]:
        """Verify a specific document"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        is_genuine = random.random() > 0.08  # 92% genuine documents
        
        return {
            "source": "DigiLocker",
            "document_id": document_id,
            "is_genuine": is_genuine,
            "verification_status": "verified" if is_genuine else "suspicious",
            "verified_at": datetime.now().isoformat(),
            "notes": "" if is_genuine else random.choice([
                "Document signature mismatch",
                "Potential forgery detected",
                "Issuing authority verification failed"
            ])
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {}
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        return {}
