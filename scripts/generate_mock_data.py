#!/usr/bin/env python3
"""
Generate mock data for Aether GovOS
Creates 5000 properties per state with fraud patterns
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from faker import Faker
import random
import json
from datetime import datetime, timedelta
from database import SessionLocal, init_db
from models.database_models import Property, Citizen, WorkflowState, WorkflowStatusEnum
import uuid

fake = Faker('en_IN')

# Fraud patterns configuration
FRAUD_PATTERNS = {
    "blacklisted_seller": 0.02,  # 2%
    "court_disputed": 0.03,      # 3%
    "benami_transaction": 0.02,   # 2%
    "price_jump": 0.05,           # 5%
    "ghost_applicant": 0.01,      # 1%
    "forged_document": 0.02,      # 2%
    "multiple_claims": 0.03,      # 3%
    "deceased_owner": 0.01,       # 1%
    "minor_owner": 0.01,          # 1%
    "shell_company": 0.02         # 2%
}

def generate_karnataka_property(index):
    """Generate a property in Karnataka"""
    property_id = f"KAR-PROP-{str(uuid.uuid4())[:8].upper()}"
    
    # Determine if this property has fraud patterns
    fraud_flags = {}
    for pattern, probability in FRAUD_PATTERNS.items():
        if random.random() < probability:
            fraud_flags[pattern] = True
    
    # Base property details
    districts = ["Bengaluru Urban", "Bengaluru Rural", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi"]
    district = random.choice(districts)
    
    property_value = random.uniform(500000, 50000000)
    
    # Apply fraud pattern: sudden price jump
    if fraud_flags.get("price_jump"):
        property_value *= random.uniform(1.5, 3.0)  # 50-200% jump
    
    # Title status
    title_status = "clear"
    if fraud_flags.get("court_disputed"):
        title_status = "disputed"
    elif fraud_flags.get("multiple_claims"):
        title_status = "encumbered"
    elif random.random() < 0.15:
        title_status = random.choice(["disputed", "encumbered"])
    
    # Encumbrances
    encumbrances = []
    if title_status == "encumbered" or random.random() < 0.2:
        encumbrances.append({
            "type": random.choice(["mortgage", "loan", "lien"]),
            "amount": random.uniform(100000, property_value * 0.5),
            "creditor": random.choice(["SBI Bank", "HDFC Bank", "Canara Bank", "ICICI Bank"])
        })
    
    # Property history
    num_transactions = random.randint(1, 5)
    history = []
    for i in range(num_transactions):
        history.append({
            "date": (datetime.now() - timedelta(days=random.randint(365 * i, 365 * (i + 1)))).isoformat(),
            "transaction_type": random.choice(["sale", "inheritance", "gift"]),
            "previous_owner": fake.name()
        })
    
    # State-specific data
    state_specific_data = {
        "kaveri_id": f"KAV-{random.randint(100000, 999999)}",
        "bhoomi_id": f"BH-{random.randint(100000, 999999)}",
        "e_aasthi_id": f"EA-{random.randint(100000, 999999)}",
        "survey_number": f"{random.randint(1, 500)}/{random.randint(1, 10)}",
        "sub_registrar_office": random.choice(["Bangalore North", "Bangalore South", "Mysore Circle", "Hubli Circle"]),
        "fraud_flags": fraud_flags
    }
    
    owner_name = fake.name()
    
    # Check for deceased owner fraud
    if fraud_flags.get("deceased_owner"):
        owner_name += " (Deceased)"
    
    # Check for minor owner fraud
    if fraud_flags.get("minor_owner"):
        owner_name += " (Minor)"
    
    property = Property(
        property_id=property_id,
        state="karnataka",
        location=fake.address(),
        district=district,
        tehsil=random.choice(["Bangalore North", "Bangalore South", "Yelahanka", "KR Puram"]),
        village=random.choice(["Devanahalli", "Nelamangala", "Doddaballapur", "Hoskote"]),
        owner=owner_name,
        owner_citizen_id=None,  # Will be linked later
        title_status=title_status,
        encumbrances=encumbrances,
        history=history,
        property_value=property_value,
        property_size=random.uniform(500, 5000),
        property_type=random.choice(["residential", "commercial", "agricultural"]),
        state_specific_data=state_specific_data
    )
    
    return property


def generate_jk_property(index):
    """Generate a property in Jammu & Kashmir"""
    property_id = f"JK-PROP-{str(uuid.uuid4())[:8].upper()}"
    
    # Determine fraud patterns
    fraud_flags = {}
    for pattern, probability in FRAUD_PATTERNS.items():
        if random.random() < probability:
            fraud_flags[pattern] = True
    
    districts = ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Budgam", "Pulwama"]
    district = random.choice(districts)
    
    property_value = random.uniform(300000, 30000000)
    
    if fraud_flags.get("price_jump"):
        property_value *= random.uniform(1.6, 2.5)
    
    title_status = "clear"
    if fraud_flags.get("court_disputed"):
        title_status = "disputed"
    elif fraud_flags.get("multiple_claims"):
        title_status = "encumbered"
    elif random.random() < 0.18:
        title_status = random.choice(["disputed", "encumbered"])
    
    encumbrances = []
    if title_status == "encumbered" or random.random() < 0.22:
        encumbrances.append({
            "type": random.choice(["mortgage", "cooperative_loan", "revenue_arrears"]),
            "amount": random.uniform(50000, property_value * 0.4),
            "creditor": random.choice(["J&K Bank", "Cooperative Bank", "Revenue Department"])
        })
    
    num_transactions = random.randint(1, 4)
    history = []
    for i in range(num_transactions):
        history.append({
            "date": (datetime.now() - timedelta(days=random.randint(365 * i, 365 * (i + 1)))).isoformat(),
            "transaction_type": random.choice(["sale", "inheritance", "gift", "intiqal"]),
            "previous_owner": fake.name()
        })
    
    state_specific_data = {
        "lris_id": f"LRIS-{random.randint(100000, 999999)}",
        "khewat_number": f"KH-{random.randint(1000, 9999)}",
        "khasra_number": f"KS-{random.randint(100, 999)}",
        "total_kanals": random.uniform(1, 20),
        "total_marlas": random.randint(0, 19),
        "jamabandi_year": random.randint(2020, 2024),
        "fraud_flags": fraud_flags
    }
    
    owner_name = fake.name()
    
    if fraud_flags.get("deceased_owner"):
        owner_name += " (Deceased)"
    
    if fraud_flags.get("minor_owner"):
        owner_name += " (Minor)"
    
    property = Property(
        property_id=property_id,
        state="jk",
        location=fake.address(),
        district=district,
        tehsil=random.choice(["Srinagar", "Ganderbal", "Budgam", "Anantnag"]),
        village=random.choice(["Srinagar City", "Budgam Town", "Anantnag Town", "Baramulla"]),
        owner=owner_name,
        owner_citizen_id=None,
        title_status=title_status,
        encumbrances=encumbrances,
        history=history,
        property_value=property_value,
        property_size=random.uniform(400, 4000),
        property_type=random.choice(["residential", "commercial", "agricultural", "horticulture"]),
        state_specific_data=state_specific_data
    )
    
    return property


def generate_citizens(count=100):
    """Generate mock citizens"""
    citizens = []
    
    for i in range(count):
        citizen_id = f"CIT-{str(uuid.uuid4())[:8].upper()}"
        
        citizen = Citizen(
            citizen_id=citizen_id,
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()[:15],
            aadhaar_number=f"{random.randint(100000000000, 999999999999)}",
            verified_attributes={
                "aadhaar_verified": random.choice([True, False]),
                "phone_verified": random.choice([True, False]),
                "email_verified": random.choice([True, False])
            },
            state=random.choice(["karnataka", "jk"]),
            district=random.choice(["Bengaluru Urban", "Srinagar"]),
            address=fake.address()
        )
        
        citizens.append(citizen)
    
    return citizens


def main():
    print("🚀 Generating mock data for Aether GovOS...")
    
    # Initialize database
    print("📊 Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Generate citizens
        print("👥 Generating 100 citizens...")
        citizens = generate_citizens(100)
        db.bulk_save_objects(citizens)
        db.commit()
        print("✅ Citizens generated")
        
        # Generate Karnataka properties
        print("🏘️  Generating 5000 properties for Karnataka...")
        karnataka_properties = []
        for i in range(5000):
            prop = generate_karnataka_property(i)
            karnataka_properties.append(prop)
            
            if (i + 1) % 1000 == 0:
                print(f"   Generated {i + 1}/5000 Karnataka properties...")
        
        db.bulk_save_objects(karnataka_properties)
        db.commit()
        print("✅ Karnataka properties generated")
        
        # Generate J&K properties
        print("🏘️  Generating 5000 properties for J&K...")
        jk_properties = []
        for i in range(5000):
            prop = generate_jk_property(i)
            jk_properties.append(prop)
            
            if (i + 1) % 1000 == 0:
                print(f"   Generated {i + 1}/5000 J&K properties...")
        
        db.bulk_save_objects(jk_properties)
        db.commit()
        print("✅ J&K properties generated")
        
        # Statistics
        print("\n📈 Generation Summary:")
        print(f"   Total Citizens: 100")
        print(f"   Karnataka Properties: 5000")
        print(f"   J&K Properties: 5000")
        print(f"   Total Properties: 10000")
        
        # Count fraud patterns
        all_properties = karnataka_properties + jk_properties
        fraud_count = sum(1 for p in all_properties if p.state_specific_data.get('fraud_flags'))
        print(f"   Properties with fraud patterns: {fraud_count}")
        
        print("\n✅ Mock data generation complete!")
        
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
