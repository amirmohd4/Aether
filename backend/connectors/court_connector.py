from .base_connector import BaseConnector
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

class CourtRecordsConnector(BaseConnector):
    """Court Records and Legal Disputes Connector"""
    
    CASE_TYPES = [
        'Civil Suit',
        'Property Dispute',
        'Partition Suit',
        'Title Dispute',
        'Encroachment Case',
        'Revenue Case',
        'Family Dispute'
    ]
    
    CASE_STATUS = [
        'Pending',
        'Under Trial',
        'Disposed',
        'Dismissed',
        'Decreed',
        'Stayed',
        'Appealed'
    ]
    
    def fetch_property_data(self, property_id: str) -> Dict[str, Any]:
        self._simulate_network_delay()
        self._check_mock_failure()
        
        return {
            "source": "Court Records",
            "property_id": property_id,
            "court_id": f"CRT-{property_id[-8:]}",
            "has_pending_cases": random.random() < 0.15,  # 15% have pending cases
            "total_cases": random.randint(0, 5)
        }
    
    def get_dispute_status(self, property_id: str) -> Dict[str, Any]:
        """Get all court cases and disputes related to property"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        has_disputes = random.random() < 0.15  # 15% have disputes
        
        cases = []
        if has_disputes:
            num_cases = random.randint(1, 3)
            for i in range(num_cases):
                case_date = datetime.now() - timedelta(days=random.randint(30, 1825))  # Last 5 years
                
                case = {
                    "case_number": f"CS-{random.randint(1000, 9999)}/{case_date.year}",
                    "case_type": random.choice(self.CASE_TYPES),
                    "filing_date": case_date.isoformat(),
                    "status": random.choice(self.CASE_STATUS),
                    "court_name": random.choice([
                        "District Court",
                        "Civil Court",
                        "High Court",
                        "Revenue Court"
                    ]),
                    "plaintiff": f"Plaintiff-{random.randint(100, 999)}",
                    "defendant": f"Defendant-{random.randint(100, 999)}",
                    "next_hearing": None if random.random() < 0.5 else (
                        datetime.now() + timedelta(days=random.randint(7, 90))
                    ).isoformat(),
                    "stay_order": random.random() < 0.2,  # 20% have stay orders
                    "injunction": random.random() < 0.15  # 15% have injunctions
                }
                cases.append(case)
        
        # Calculate risk score based on cases
        risk_score = 0
        if cases:
            risk_score = len(cases) * 20
            for case in cases:
                if case['status'] in ['Pending', 'Under Trial']:
                    risk_score += 15
                if case.get('stay_order'):
                    risk_score += 25
                if case.get('injunction'):
                    risk_score += 30
        
        risk_score = min(risk_score, 100)  # Cap at 100
        
        return {
            "source": "Court Records",
            "property_id": property_id,
            "has_disputes": has_disputes,
            "total_cases": len(cases),
            "active_cases": len([c for c in cases if c['status'] in ['Pending', 'Under Trial']]),
            "cases": cases,
            "risk_score": risk_score,
            "risk_level": 'Low' if risk_score < 30 else 'Medium' if risk_score < 60 else 'High',
            "checked_at": datetime.now().isoformat()
        }
    
    def get_ownership_chain(self, property_id: str, years: int = 30) -> Dict[str, Any]:
        """Get ownership chain for last N years"""
        self._simulate_network_delay()
        self._check_mock_failure()
        
        # Generate ownership chain
        num_transfers = random.randint(1, 5)
        chain = []
        
        for i in range(num_transfers):
            transfer_date = datetime.now() - timedelta(days=random.randint(0, years * 365))
            
            chain.append({
                "transfer_number": num_transfers - i,
                "date": transfer_date.isoformat(),
                "from_owner": f"Owner-{random.randint(1000, 9999)}" if i < num_transfers - 1 else "Original Owner",
                "to_owner": f"Owner-{random.randint(1000, 9999)}",
                "transfer_type": random.choice(['Sale', 'Inheritance', 'Gift', 'Partition']),
                "document_number": f"DOC-{random.randint(10000, 99999)}",
                "verified": random.choice([True, False])
            })
        
        # Sort by date
        chain.sort(key=lambda x: x['date'])
        
        return {
            "source": "Court Records",
            "property_id": property_id,
            "years_searched": years,
            "ownership_chain": chain,
            "chain_complete": random.choice([True, False]),
            "gaps_found": random.choice([True, False]),
            "fetched_at": datetime.now().isoformat()
        }
    
    def verify_title(self, property_id: str) -> Dict[str, Any]:
        return {}
    
    def check_encumbrance(self, property_id: str) -> Dict[str, Any]:
        return {}
