import os
import json
from typing import Dict, Any, List, Optional

# Comprehensive UN Member States dataset in Python
UN_MEMBER_STATES = [
    {"code": "IN", "name": "India", "flag": "🇮🇳", "region": "Asia", "curr": "INR", "id": "Aadhaar / PAN"},
    {"code": "AE", "name": "United Arab Emirates", "flag": "🇦🇪", "region": "Asia", "curr": "AED", "id": "UAE Pass / Emirates ID"},
    {"code": "SA", "name": "Saudi Arabia", "flag": "🇸🇦", "region": "Asia", "curr": "SAR", "id": "Nafath / Iqama"},
    {"code": "JP", "name": "Japan", "flag": "🇯🇵", "region": "Asia", "curr": "JPY", "id": "My Number Card"},
    {"code": "SG", "name": "Singapore", "flag": "🇸🇬", "region": "Asia", "curr": "SGD", "id": "Singpass / NRIC"},
    {"code": "CN", "name": "China", "flag": "🇨🇳", "region": "Asia", "curr": "CNY", "id": "Resident ID"},
    {"code": "KR", "name": "South Korea", "flag": "🇰🇷", "region": "Asia", "curr": "KRW", "id": "Resident Registration Card"},
    {"code": "ID", "name": "Indonesia", "flag": "🇮🇩", "region": "Asia", "curr": "IDR", "id": "e-KTP (NIK)"},
    {"code": "MY", "name": "Malaysia", "flag": "🇲🇾", "region": "Asia", "curr": "MYR", "id": "MyKad / NRIC"},
    {"code": "TH", "name": "Thailand", "flag": "🇹🇭", "region": "Asia", "curr": "THB", "id": "Thai Citizen ID"},
    {"code": "VN", "name": "Vietnam", "flag": "🇻🇳", "region": "Asia", "curr": "VND", "id": "CCCD / Citizen ID"},
    {"code": "PH", "name": "Philippines", "flag": "🇵🇭", "region": "Asia", "curr": "PHP", "id": "PhilSys National ID"},
    {"code": "PK", "name": "Pakistan", "flag": "🇵🇰", "region": "Asia", "curr": "PKR", "id": "NADRA CNIC"},
    {"code": "BD", "name": "Bangladesh", "flag": "🇧🇩", "region": "Asia", "curr": "BDT", "id": "National Smart ID"},
    {"code": "LK", "name": "Sri Lanka", "flag": "🇱🇰", "region": "Asia", "curr": "LKR", "id": "NIC Card"},
    {"code": "NP", "name": "Nepal", "flag": "🇳🇵", "region": "Asia", "curr": "NPR", "id": "National ID Card"},
    {"code": "IL", "name": "Israel", "flag": "🇮🇱", "region": "Asia", "curr": "ILS", "id": "Teudat Zehut"},
    {"code": "QA", "name": "Qatar", "flag": "🇶🇦", "region": "Asia", "curr": "QAR", "id": "QID Card"},
    {"code": "KW", "name": "Kuwait", "flag": "🇰🇼", "region": "Asia", "curr": "KWD", "id": "Civil ID Card"},
    {"code": "OM", "name": "Oman", "flag": "🇴🇲", "region": "Asia", "curr": "OMR", "id": "Civil Status ID"},
    {"code": "BH", "name": "Bahrain", "flag": "🇧🇭", "region": "Asia", "curr": "BHD", "id": "CPR ID Card"},
    {"code": "JO", "name": "Jordan", "flag": "🇯🇴", "region": "Asia", "curr": "JOD", "id": "National ID Number"},
    {"code": "LB", "name": "Lebanon", "flag": "🇱🇧", "region": "Asia", "curr": "LBP", "id": "Lebanese ID"},
    {"code": "IQ", "name": "Iraq", "flag": "🇮🇶", "region": "Asia", "curr": "IQD", "id": "Unified ID Card"},
    {"code": "IR", "name": "Iran", "flag": "🇮🇷", "region": "Asia", "curr": "IRR", "id": "National Smart Card"},
    {"code": "KZ", "name": "Kazakhstan", "flag": "🇰🇿", "region": "Asia", "curr": "KZT", "id": "IIN / eGov.kz"},
    {"code": "UZ", "name": "Uzbekistan", "flag": "🇺🇿", "region": "Asia", "curr": "UZS", "id": "JShShIR / PINFL"},
    {"code": "AZ", "name": "Azerbaijan", "flag": "🇦🇿", "region": "Asia", "curr": "AZN", "id": "FIN Code"},
    {"code": "GE", "name": "Georgia", "flag": "🇬🇪", "region": "Asia", "curr": "GEL", "id": "Personal Number ID"},
    {"code": "AM", "name": "Armenia", "flag": "🇦🇲", "region": "Asia", "curr": "AMD", "id": "PSN Card"},

    {"code": "EE", "name": "Estonia", "flag": "🇪🇪", "region": "Europe", "curr": "EUR", "id": "e-Residency / Smart-ID"},
    {"code": "GB", "name": "United Kingdom", "flag": "🇬🇧", "region": "Europe", "curr": "GBP", "id": "GOV.UK One Login"},
    {"code": "DE", "name": "Germany", "flag": "🇩🇪", "region": "Europe", "curr": "EUR", "id": "BundID / eID"},
    {"code": "FR", "name": "France", "flag": "🇫🇷", "region": "Europe", "curr": "EUR", "id": "FranceConnect / CNI"},
    {"code": "IT", "name": "Italy", "flag": "🇮🇹", "region": "Europe", "curr": "EUR", "id": "SPID / CIE Digital"},
    {"code": "ES", "name": "Spain", "flag": "🇪🇸", "region": "Europe", "curr": "EUR", "id": "Cl@ve / DNIe"},
    {"code": "NL", "name": "Netherlands", "flag": "🇳🇱", "region": "Europe", "curr": "EUR", "id": "DigiD / BSN"},
    {"code": "CH", "name": "Switzerland", "flag": "🇨🇭", "region": "Europe", "curr": "CHF", "id": "SwissID / AHV"},
    {"code": "SE", "name": "Sweden", "flag": "🇸🇪", "region": "Europe", "curr": "SEK", "id": "BankID / Personnummer"},
    {"code": "NO", "name": "Norway", "flag": "🇳🇴", "region": "Europe", "curr": "NOK", "id": "BankID / Fødselsnummer"},
    {"code": "DK", "name": "Denmark", "flag": "🇩🇰", "region": "Europe", "curr": "DKK", "id": "MitID / CPR"},
    {"code": "FI", "name": "Finland", "flag": "🇫🇮", "region": "Europe", "curr": "EUR", "id": "Suomi.fi / Henkilötunnus"},
    {"code": "IE", "name": "Ireland", "flag": "🇮🇪", "region": "Europe", "curr": "EUR", "id": "MyGovID / PPSN"},
    {"code": "BE", "name": "Belgium", "flag": "🇧🇪", "region": "Europe", "curr": "EUR", "id": "itsme / eID"},
    {"code": "AT", "name": "Austria", "flag": "🇦🇹", "region": "Europe", "curr": "EUR", "id": "ID Austria"},
    {"code": "PL", "name": "Poland", "flag": "🇵🇱", "region": "Europe", "curr": "PLN", "id": "mObywatel / PESEL"},
    {"code": "PT", "name": "Portugal", "flag": "🇵🇹", "region": "Europe", "curr": "EUR", "id": "Chave Móvel Digital"},
    {"code": "GR", "name": "Greece", "flag": "🇬🇷", "region": "Europe", "curr": "EUR", "id": "Gov.gr / AFM"},
    {"code": "CZ", "name": "Czechia", "flag": "🇨🇿", "region": "Europe", "curr": "CZK", "id": "eIdentita / Rodné číslo"},
    {"code": "HU", "name": "Hungary", "flag": "🇭🇺", "region": "Europe", "curr": "HUF", "id": "Ügyfélkapu / TAJ"},
    {"code": "RO", "name": "Romania", "flag": "🇷🇴", "region": "Europe", "curr": "RON", "id": "Ghișeul.ro / CNP"},
    {"code": "UA", "name": "Ukraine", "flag": "🇺🇦", "region": "Europe", "curr": "UAH", "id": "Diia App / RNTRC"},

    {"code": "US", "name": "United States", "flag": "🇺🇸", "region": "Americas", "curr": "USD", "id": "SSN / Login.gov"},
    {"code": "CA", "name": "Canada", "flag": "🇨🇦", "region": "Americas", "curr": "CAD", "id": "SIN / Interac Verified"},
    {"code": "MX", "name": "Mexico", "flag": "🇲🇽", "region": "Americas", "curr": "MXN", "id": "CURP / INE Digital"},
    {"code": "BR", "name": "Brazil", "flag": "🇧🇷", "region": "Americas", "curr": "BRL", "id": "CPF / Gov.br"},
    {"code": "AR", "name": "Argentina", "flag": "🇦🇷", "region": "Americas", "curr": "ARS", "id": "Mi Argentina / DNI"},
    {"code": "CO", "name": "Colombia", "flag": "🇨🇴", "region": "Americas", "curr": "COP", "id": "Cédula Digital"},
    {"code": "CL", "name": "Chile", "flag": "🇨🇱", "region": "Americas", "curr": "CLP", "id": "ClaveÚnica / RUN"},
    {"code": "PE", "name": "Peru", "flag": "🇵🇪", "region": "Americas", "curr": "PEN", "id": "RENIEC / DNI"},
    {"code": "EC", "name": "Ecuador", "flag": "🇪🇨", "region": "Americas", "curr": "USD", "id": "Registro Civil / Cédula"},
    {"code": "UY", "name": "Uruguay", "flag": "🇺🇾", "region": "Americas", "curr": "UYU", "id": "Gub.uy / Cédula"},

    {"code": "KE", "name": "Kenya", "flag": "🇰🇪", "region": "Africa", "curr": "KES", "id": "Huduma Namba / National ID"},
    {"code": "NG", "name": "Nigeria", "flag": "🇳🇬", "region": "Africa", "curr": "NGN", "id": "NIN / BVN"},
    {"code": "ZA", "name": "South Africa", "flag": "🇿🇦", "region": "Africa", "curr": "ZAR", "id": "Smart ID Card / eHomeAffairs"},
    {"code": "EG", "name": "Egypt", "flag": "🇪🇬", "region": "Africa", "curr": "EGP", "id": "National ID Card"},
    {"code": "MA", "name": "Morocco", "flag": "🇲🇦", "region": "Africa", "curr": "MAD", "id": "CNIE / Gov.ma"},
    {"code": "GH", "name": "Ghana", "flag": "🇬🇭", "region": "Africa", "curr": "GHS", "id": "Ghana Card / NIA"},
    {"code": "ET", "name": "Ethiopia", "flag": "🇪🇹", "region": "Africa", "curr": "ETB", "id": "Fayda Digital ID"},
    {"code": "TZ", "name": "Tanzania", "flag": "🇹🇿", "region": "Africa", "curr": "TZS", "id": "NIDA Card"},
    {"code": "UG", "name": "Uganda", "flag": "🇺🇬", "region": "Africa", "curr": "UGX", "id": "NIRA NIN Card"},
    {"code": "RW", "name": "Rwanda", "flag": "🇷🇼", "region": "Africa", "curr": "RWF", "id": "Irembo / National ID"},

    {"code": "AU", "name": "Australia", "flag": "🇦🇺", "region": "Oceania", "curr": "AUD", "id": "myGov / Medicare / TFN"},
    {"code": "NZ", "name": "New Zealand", "flag": "🇳🇿", "region": "Oceania", "curr": "NZD", "id": "RealMe / IRD Number"},
    {"code": "PG", "name": "Papua New Guinea", "flag": "🇵🇬", "region": "Oceania", "curr": "PGK", "id": "NIPA National ID"},
    {"code": "FJ", "name": "Fiji", "flag": "🇫🇯", "region": "Oceania", "curr": "FJD", "id": "Fiji Joint Card / TIN"}
]

class CountryConfigLoader:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_dir = os.path.join(base_dir, "configs", "countries")
        else:
            self.config_dir = config_dir

    def list_available_countries(self) -> List[Dict[str, str]]:
        countries_dict = {}
        # First load files if any
        if os.path.exists(self.config_dir):
            for file in os.listdir(self.config_dir):
                if file.endswith(".json"):
                    file_path = os.path.join(self.config_dir, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            code = data.get("country_code", file.replace(".json", "").upper())
                            countries_dict[code] = {
                                "code": code,
                                "name": data.get("country_name", file.replace(".json", "").capitalize()),
                                "flag": data.get("flag", "🌐"),
                                "default_language": data.get("default_language", "en")
                            }
                    except Exception as e:
                        print(f"Error reading config {file}: {e}")

        # Supplement with UN member states list
        for item in UN_MEMBER_STATES:
            if item["code"] not in countries_dict:
                countries_dict[item["code"]] = {
                    "code": item["code"],
                    "name": item["name"],
                    "flag": item["flag"],
                    "default_language": "en"
                }

        return sorted(list(countries_dict.values()), key=lambda x: x["name"])

    def get_country_config(self, country_code: str) -> Optional[Dict[str, Any]]:
        code_upper = country_code.upper()
        file_path = os.path.join(self.config_dir, f"{country_code.lower()}.json")
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        # Dynamic fallback generation for UN member states
        match = next((item for item in UN_MEMBER_STATES if item["code"] == code_upper), None)
        if match:
            return {
                "country_code": match["code"],
                "country_name": match["name"],
                "flag": match["flag"],
                "currency": {"code": match["curr"], "symbol": "$", "name": match["curr"]},
                "id_system": {"name": match["id"], "format": "National ID Format", "verification_endpoint": f"/api/v1/identity/verify/{match['code'].lower()}"},
                "default_language": "en",
                "supported_languages": ["en"],
                "departments": [
                    {"id": f"dept_rev_{match['code'].lower()}", "name": f"Ministry of Lands, Housing & Revenue Registry ({match['name']})", "code": "REV", "icon": "Landmark"},
                    {"id": f"dept_corp_{match['code'].lower()}", "name": "Ministry of Trade & Corporate Affairs", "code": "MCA", "icon": "Building2"}
                ],
                "services": [
                    {
                        "id": f"srv_{match['code'].lower()}_prop_reg",
                        "department_id": f"dept_rev_{match['code'].lower()}",
                        "name": f"Digital Property Registration & Title Audit ({match['name']})",
                        "description": f"Instant title audit, cadastral parcel check, stamp duty clearance in {match['name']}.",
                        "processing_time": "< 30 seconds",
                        "fees": {"base_fee": 250, "stamp_duty_percentage": 3.5, "registration_fee_percentage": 0.5},
                        "required_documents": [f"Identity ({match['id']})", "Title Deed Copy"],
                        "workflow_steps": [
                            {"id": "title_check", "name": "Title Audit & Registry Verification"},
                            {"id": "encumbrance", "name": "Lien & Encumbrance Search"},
                            {"id": "fraud_detection", "name": "AI Land Fraud Risk Scoring"},
                            {"id": "registration", "name": "Digital Registry Ledger Recordation"}
                        ]
                    }
                ]
            }
        
        return None

    def get_country_services(self, country_code: str) -> List[Dict[str, Any]]:
        config = self.get_country_config(country_code)
        if config:
            return config.get("services", [])
        return []

    def get_country_departments(self, country_code: str) -> List[Dict[str, Any]]:
        config = self.get_country_config(country_code)
        if config:
            return config.get("departments", [])
        return []

    def get_country_states(self, country_code: str) -> List[str]:
        states_map = {
            "IN": ["Karnataka", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Delhi NCR", "Gujarat", "Telangana", "Kerala", "West Bengal", "Rajasthan"],
            "US": ["California", "Texas", "New York", "Florida", "Illinois", "Washington", "Pennsylvania", "Georgia", "Ohio", "North Carolina"],
            "AE": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
            "KE": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu (Eldoret)", "Kiambu", "Machakos", "Kilifi"],
            "CA": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan"],
            "AU": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia"],
            "DE": ["Bavaria", "Berlin", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse"],
            "GB": ["England", "Scotland", "Wales", "Northern Ireland"],
            "NG": ["Lagos", "Abuja FCT", "Kano", "Rivers", "Oyo", "Enugu"],
            "BR": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná"]
        }
        return states_map.get(country_code.upper(), [])

config_loader = CountryConfigLoader()

