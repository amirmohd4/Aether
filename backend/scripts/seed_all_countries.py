import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from models.database_models import Property, Citizen

# Map country codes to Faker locales
LOCALE_MAP = {
    'IN': 'en_IN',
    'US': 'en_US',
    'GB': 'en_GB',
    'CA': 'en_CA',
    'AU': 'en_AU',
    'NZ': 'en_NZ',
    'ZA': 'en_ZA',
    'NG': 'en_NG',
    'KE': 'en_US',  # No Kenya locale, use en_US
    'AE': 'en_US',  # No UAE locale, use en_US
    'SG': 'en_US',  # No Singapore locale, use en_US
    # ... add more as needed
}
DEFAULT_LOCALE = 'en_US'

# All UN member states (simplified list)
COUNTRIES = [
    {"code": "IN", "name": "India", "states": ["Karnataka", "Maharashtra", "Tamil Nadu", "Uttar Pradesh", "Gujarat", "Rajasthan", "Kerala", "West Bengal", "Andhra Pradesh", "Telangana"]},
    {"code": "US", "name": "United States", "states": ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan"]},
    {"code": "GB", "name": "United Kingdom", "states": ["England", "Scotland", "Wales", "Northern Ireland"]},
    {"code": "AE", "name": "United Arab Emirates", "states": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"]},
    {"code": "KE", "name": "Kenya", "states": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi", "Kitale"]},
    {"code": "CA", "name": "Canada", "states": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan"]},
    {"code": "AU", "name": "Australia", "states": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia"]},
    {"code": "DE", "name": "Germany", "states": ["Bavaria", "Berlin", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse"]},
    {"code": "FR", "name": "France", "states": ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie"]},
    {"code": "IT", "name": "Italy", "states": ["Lombardy", "Lazio", "Campania", "Veneto", "Emilia-Romagna"]},
    {"code": "ES", "name": "Spain", "states": ["Madrid", "Catalonia", "Andalusia", "Valencia", "Basque Country"]},
    {"code": "NL", "name": "Netherlands", "states": ["North Holland", "South Holland", "Utrecht", "Gelderland", "North Brabant"]},
    {"code": "SE", "name": "Sweden", "states": ["Stockholm", "Västra Götaland", "Skåne", "Uppsala", "Östergötland"]},
    {"code": "NO", "name": "Norway", "states": ["Oslo", "Viken", "Vestland", "Rogaland", "Trøndelag"]},
    {"code": "DK", "name": "Denmark", "states": ["Capital Region", "Central Denmark", "North Jutland", "Zealand", "South Denmark"]},
    {"code": "FI", "name": "Finland", "states": ["Uusimaa", "Pirkanmaa", "Varsinais-Suomi", "Ostrobothnia", "Lapland"]},
    {"code": "IE", "name": "Ireland", "states": ["Dublin", "Cork", "Galway", "Limerick", "Waterford"]},
    {"code": "BE", "name": "Belgium", "states": ["Flanders", "Wallonia", "Brussels"]},
    {"code": "CH", "name": "Switzerland", "states": ["Zurich", "Bern", "Geneva", "Basel", "Lausanne"]},
    {"code": "AT", "name": "Austria", "states": ["Vienna", "Lower Austria", "Upper Austria", "Styria", "Tyrol"]},
    {"code": "PL", "name": "Poland", "states": ["Masovian", "Silesian", "Greater Poland", "Lesser Poland", "Lower Silesian"]},
    {"code": "PT", "name": "Portugal", "states": ["Lisbon", "Porto", "Braga", "Setúbal", "Aveiro"]},
    {"code": "GR", "name": "Greece", "states": ["Attica", "Central Macedonia", "Thessaly", "Peloponnese", "Crete"]},
    {"code": "CZ", "name": "Czechia", "states": ["Prague", "Central Bohemian", "South Moravian", "Moravian-Silesian", "Ústí nad Labem"]},
    {"code": "HU", "name": "Hungary", "states": ["Budapest", "Pest", "Csongrád", "Borsod", "Hajdú-Bihar"]},
    {"code": "RO", "name": "Romania", "states": ["Bucharest", "Cluj", "Timiș", "Iași", "Constanța"]},
    {"code": "UA", "name": "Ukraine", "states": ["Kyiv", "Kharkiv", "Odessa", "Dnipro", "Lviv"]},
    {"code": "RU", "name": "Russia", "states": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"]},
    {"code": "CN", "name": "China", "states": ["Beijing", "Shanghai", "Guangdong", "Zhejiang", "Jiangsu"]},
    {"code": "JP", "name": "Japan", "states": ["Tokyo", "Osaka", "Aichi", "Fukuoka", "Hokkaido"]},
    {"code": "KR", "name": "South Korea", "states": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"]},
    {"code": "ID", "name": "Indonesia", "states": ["Jakarta", "East Java", "West Java", "Central Java", "North Sumatra"]},
    {"code": "MY", "name": "Malaysia", "states": ["Kuala Lumpur", "Selangor", "Johor", "Penang", "Sarawak"]},
    {"code": "TH", "name": "Thailand", "states": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Khon Kaen"]},
    {"code": "VN", "name": "Vietnam", "states": ["Ho Chi Minh City", "Hanoi", "Da Nang", "Can Tho", "Hai Phong"]},
    {"code": "PH", "name": "Philippines", "states": ["Manila", "Cebu", "Davao", "Iloilo", "Baguio"]},
    {"code": "PK", "name": "Pakistan", "states": ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Islamabad"]},
    {"code": "BD", "name": "Bangladesh", "states": ["Dhaka", "Chittagong", "Rajshahi", "Khulna", "Sylhet"]},
    {"code": "LK", "name": "Sri Lanka", "states": ["Western", "Central", "Southern", "Northern", "Eastern"]},
    {"code": "NP", "name": "Nepal", "states": ["Bagmati", "Lumbini", "Sudurpashchim", "Karnali", "Gandaki"]},
    {"code": "EG", "name": "Egypt", "states": ["Cairo", "Alexandria", "Giza", "Port Said", "Suez"]},
    {"code": "MA", "name": "Morocco", "states": ["Casablanca-Settat", "Rabat-Salé", "Tangier-Tétouan", "Marrakech", "Fès"]},
    {"code": "ZA", "name": "South Africa", "states": ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Mpumalanga"]},
    {"code": "NG", "name": "Nigeria", "states": ["Lagos", "Abuja", "Kano", "Rivers", "Oyo"]},
    {"code": "GH", "name": "Ghana", "states": ["Greater Accra", "Ashanti", "Western", "Eastern", "Northern"]},
    {"code": "ET", "name": "Ethiopia", "states": ["Addis Ababa", "Oromia", "Amhara", "Tigray", "Sidama"]},
    {"code": "TZ", "name": "Tanzania", "states": ["Dar es Salaam", "Dodoma", "Mwanza", "Arusha", "Mbeya"]},
    {"code": "UG", "name": "Uganda", "states": ["Kampala", "Wakiso", "Mukono", "Jinja", "Gulu"]},
    {"code": "RW", "name": "Rwanda", "states": ["Kigali", "Eastern", "Western", "Northern", "Southern"]},
]

def generate_property_id(country_code, index):
    return f"{country_code}-PROP-{index:04d}"

def generate_national_id(country_code):
    # Simplified national ID generation
    if country_code == 'IN':
        return f"{random.randint(100000000000, 999999999999)}"
    elif country_code == 'US':
        return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
    elif country_code == 'AE':
        return f"{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(100000, 999999)}"
    elif country_code == 'KE':
        return f"{random.randint(10000000, 99999999)}"
    elif country_code == 'GB':
        return f"{random.randint(100000, 999999)}"
    else:
        return f"ID-{random.randint(100000, 999999)}"

def seed_country(db: Session, country_code: str, country_name: str, states: list):
    locale = LOCALE_MAP.get(country_code, DEFAULT_LOCALE)
    fake = Faker(locale)
    
    # Generate citizens
    citizens = []
    for i in range(20):
        citizen = Citizen(
            citizen_id=f"{country_code}-CIT-{i:04d}",
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()[:15],
            aadhaar_number=generate_national_id(country_code),  # using aadhaar field as national_id
            verified_attributes={
                "national_id_verified": random.choice([True, False]),
                "phone_verified": random.choice([True, False]),
                "email_verified": random.choice([True, False])
            },
            state=country_code,
            district=random.choice(states) if states else "Default",
            address=fake.address()
        )
        citizens.append(citizen)
    db.bulk_save_objects(citizens)
    db.commit()
    
    # Generate properties
    properties = []
    for i in range(100):
        state = random.choice(states) if states else "Default"
        prop = Property(
            property_id=generate_property_id(country_code, i),
            state=country_code,
            location=fake.address(),
            district=state,
            tehsil=fake.city(),
            village=fake.city(),
            owner=random.choice(citizens).name,
            owner_citizen_id=random.choice(citizens).citizen_id,
            title_status=random.choice(["clear", "clear", "clear", "disputed"]),
            encumbrances=[{"type": "mortgage", "amount": random.uniform(100000, 5000000)}] if random.random() < 0.1 else [],
            history=[{"date": (datetime.now() - timedelta(days=random.randint(365, 3650))).isoformat(),
                      "transaction_type": random.choice(["sale", "inheritance"]),
                      "previous_owner": fake.name()} for _ in range(random.randint(1, 3))],
            property_value=random.uniform(500000, 50000000),
            property_size=random.uniform(500, 5000),
            property_type=random.choice(["residential", "commercial", "agricultural"]),
            state_specific_data={
                "country": country_code,
                "national_id": generate_national_id(country_code)
            }
        )
        properties.append(prop)
    db.bulk_save_objects(properties)
    db.commit()
    
    print(f"✅ Seeded {country_name} ({country_code}): {len(citizens)} citizens, {len(properties)} properties")
    return {"country": country_code, "citizens": len(citizens), "properties": len(properties)}

def seed_all_countries():
    db = SessionLocal()
    results = {}
    for country in COUNTRIES:
        try:
            results[country['code']] = seed_country(db, country['code'], country['name'], country['states'])
        except Exception as e:
            print(f"❌ Error seeding {country['code']}: {e}")
            db.rollback()
    db.close()
    print("\n✅ All countries seeded!")
    for code, result in results.items():
        print(f"  {code}: {result['citizens']} citizens, {result['properties']} properties")

if __name__ == "__main__":
    # Install faker if not installed
    try:
        import faker
    except ImportError:
        print("Installing faker...")
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
        import faker
    seed_all_countries()
