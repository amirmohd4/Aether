"""India-wide service-family seed catalog.

This is intentionally a family-level catalog, not a claim that each row is an
identical legal workflow in every State/UT. The National Government Services
Portal lists thousands of jurisdiction-specific services; Aether uses these
families for objective understanding and then requires a source-backed
jurisdiction rule pack before production execution.
"""

INDIA_SERVICE_FAMILY_DEFINITIONS = [
    # Identity, civil registration and certificates
    ("marriage_registration", "Marriage Registration", "Civil Registration", ["citizen"], ["marriage registration", "register marriage", "marriage certificate"], None, "marriage_certificate"),
    ("domicile_certificate", "Domicile/Residence Certificate", "Revenue", ["citizen"], ["domicile certificate", "residence certificate", "residential certificate"], None, "domicile_certificate"),
    ("income_certificate", "Income Certificate", "Revenue", ["citizen"], ["income certificate"], None, "income_certificate"),
    ("caste_certificate", "Caste/Community Certificate", "Revenue", ["citizen"], ["caste certificate", "community certificate", "scheduled caste certificate", "scheduled tribe certificate"], None, "caste_certificate"),
    ("legal_heir_certificate", "Legal Heir/Surviving Member Certificate", "Revenue", ["citizen"], ["legal heir certificate", "surviving member certificate", "family member certificate"], None, "legal_heir_certificate"),
    ("character_certificate", "Character Certificate", "Police", ["citizen"], ["character certificate", "police character certificate"], None, "character_certificate"),
    ("disability_certificate", "Disability Certificate", "Health", ["citizen"], ["disability certificate", "pwd certificate", "udid"], None, "disability_certificate"),
    ("senior_citizen_certificate", "Senior Citizen Certificate", "Social Welfare", ["citizen"], ["senior citizen certificate"], None, "senior_citizen_certificate"),
    ("family_register_extract", "Family Register/Household Record", "Local Government", ["citizen"], ["family register", "household certificate", "family record"], None, "family_record"),
    ("birth_registration_correction", "Birth Record Correction", "Civil Registration", ["citizen"], ["birth certificate correction", "correct birth record"], None, "updated_birth_record"),
    ("death_registration_correction", "Death Record Correction", "Civil Registration", ["citizen"], ["death certificate correction", "correct death record"], None, "updated_death_record"),

    # Property, revenue and registration
    ("certified_land_record", "Certified Land Record", "Revenue", ["citizen", "business", "bank", "developer", "insurer"], ["land record", "land record extract", "record of rights", "ror", "jamabandi"], None, "certified_land_record"),
    ("property_tax_assessment", "Property Tax Assessment", "Municipal", ["citizen", "business", "developer"], ["property tax assessment", "house tax assessment", "property assessment"], None, "property_tax_assessment"),
    ("property_tax_payment", "Property Tax Payment", "Municipal", ["citizen", "business", "developer"], ["property tax payment", "house tax payment", "property tax"], None, "property_tax_receipt"),
    ("property_registration_copy", "Certified Registered Deed Copy", "Registration", ["citizen", "business", "bank", "developer", "insurer"], ["registered deed copy", "certified sale deed copy", "registration document copy"], None, "certified_registration_copy"),
    ("stamp_duty_assessment", "Stamp Duty Assessment", "Registration", ["citizen", "business", "developer"], ["stamp duty", "stamp duty assessment", "registration fee"], None, "stamp_duty_assessment"),
    ("lease_registration", "Lease/Agreement Registration", "Registration", ["citizen", "business"], ["lease registration", "rent agreement registration", "agreement registration"], None, "registered_agreement"),
    ("partition_land", "Land Partition", "Revenue", ["citizen", "business"], ["land partition", "partition of land", "property partition"], None, "partition_order"),
    ("land_demarcation", "Land Demarcation/Survey", "Revenue", ["citizen", "business", "developer"], ["land demarcation", "land survey", "boundary demarcation"], None, "demarcation_report"),
    ("land_use_certificate", "Land Use/Zoning Certificate", "Municipal", ["citizen", "business", "developer"], ["land use certificate", "zoning certificate", "land use permission"], None, "land_use_certificate"),
    ("building_completion_certificate", "Building Completion Certificate", "Municipal", ["citizen", "business", "developer"], ["completion certificate", "building completion", "construction completion"], None, "completion_certificate"),
    ("occupancy_certificate", "Occupancy Certificate", "Municipal", ["citizen", "business", "developer"], ["occupancy certificate", "building occupancy", "oc"], None, "occupancy_certificate"),

    # Municipal and local government
    ("trade_license_renewal", "Trade Licence Renewal", "Municipal", ["citizen", "business"], ["trade license renewal", "trade licence renewal", "renew business license"], "restaurant", "renewed_trade_license"),
    ("shop_establishment_registration", "Shops & Establishments Registration", "Labour", ["business"], ["shops establishment", "shop establishment registration", "commercial establishment registration"], None, "shops_establishment_certificate"),
    ("street_vendor_certificate", "Street Vendor Certificate", "Municipal", ["citizen", "business"], ["street vendor certificate", "street vending license", "hawker license"], None, "vendor_certificate"),
    ("advertisement_signage_permit", "Advertisement/Signage Permit", "Municipal", ["citizen", "business"], ["signboard license", "advertisement permit", "hoarding permission", "signage permit"], None, "signage_permit"),
    ("sanitation_trade_clearance", "Sanitation/Health Trade Clearance", "Municipal", ["business"], ["sanitation clearance", "health trade license", "municipal health clearance"], None, "sanitation_clearance"),
    ("sewer_connection", "Sewer Connection", "Municipal", ["citizen", "business"], ["sewer connection", "new sewer connection"], None, "sewer_connection"),
    ("water_sewer_connection", "Water/Sewer Connection", "Municipal", ["citizen", "business"], ["water sewer connection", "new water sewer connection"], None, "water_sewer_connection"),
    ("electricity_connection", "Electricity New Connection", "Electricity", ["citizen", "business"], ["electricity connection", "new power connection", "new electricity connection"], None, "electricity_connection"),
    ("electricity_meter_service", "Electricity Meter/Load Service", "Electricity", ["citizen", "business"], ["meter change", "meter transfer", "load enhancement", "electricity meter"], None, "electricity_service_order"),

    # Business, industry and regulatory licensing
    ("contract_labour_license", "Contract Labour Licence", "Labour", ["business"], ["contract labour license", "contract labour licence", "contractor labour license"], None, "contract_labour_license"),
    ("interstate_migrant_worker_registration", "Inter-State Migrant Worker Registration", "Labour", ["business"], ["interstate migrant worker registration", "migrant worker registration"], None, "labour_registration"),
    ("boiler_registration", "Boiler Registration/Certificate", "Labour", ["business"], ["boiler registration", "boiler certificate", "boiler inspection"], None, "boiler_certificate"),
    ("drug_sale_license", "Drug Sale/Pharmacy Licence", "Health", ["business"], ["drug license", "drug licence", "pharmacy license", "medical store license"], None, "drug_license"),
    ("clinical_establishment_registration", "Clinical Establishment Registration", "Health", ["business"], ["clinical establishment", "hospital registration", "clinic registration"], None, "clinical_establishment_registration"),
    ("ayush_establishment_registration", "AYUSH Establishment Registration", "Health", ["business"], ["ayush registration", "ayush clinic registration", "ayush establishment"], None, "ayush_registration"),
    ("weights_measures_license", "Legal Metrology Registration/Licence", "Consumer Affairs", ["business"], ["legal metrology", "weights measures license", "weighing instrument license"], None, "legal_metrology_license"),
    ("professional_tax_registration", "Professional Tax Registration", "Tax", ["business"], ["professional tax registration", "pt registration"], None, "professional_tax_registration"),
    ("pollution_consent", "Pollution Control Consent", "Environment", ["business", "developer"], ["pollution consent", "consent to establish", "consent to operate", "cto", "cte"], "commercial_project", "pollution_consent"),
    ("environmental_clearance", "Environmental Clearance", "Environment", ["business", "developer"], ["environmental clearance", "ec application", "environment clearance"], "commercial_project", "environmental_clearance"),
    ("hazardous_waste_authorization", "Hazardous Waste Authorization", "Environment", ["business", "developer"], ["hazardous waste authorization", "hazardous waste license"], None, "waste_authorization"),
    ("factory_plan_approval", "Factory Plan Approval", "Labour", ["business", "developer"], ["factory plan approval", "factory layout approval", "factory building approval"], "commercial_project", "factory_plan_approval"),
    ("fire_noc", "Fire Safety NOC", "Fire", ["citizen", "business", "developer"], ["fire noc", "fire n oc", "fire clearance", "fire safety certificate"], None, "fire_noc"),
    ("food_business_renewal", "Food Business Licence Renewal", "Food Safety", ["business"], ["fssai renewal", "food license renewal", "food licence renewal"], "restaurant", "food_business_renewal"),

    # Corporate and tax
    ("company_name_reservation", "Company/LLP Name Reservation", "Corporate Registry", ["business"], ["company name reservation", "reserve company name", "llp name"], None, "name_reservation"),
    ("llp_incorporation", "LLP Incorporation", "Corporate Registry", ["business"], ["llp registration", "incorporate llp", "llp incorporation"], None, "llp_incorporation"),
    ("director_registration", "Director/Signatory Registration", "Corporate Registry", ["business"], ["director registration", "director identification", "din registration"], None, "director_registration"),
    ("company_master_data_change", "Company Master Data Change", "Corporate Registry", ["business"], ["company master data change", "mca company change", "registered office change"], None, "company_update"),
    ("gst_registration_update", "GST Registration Amendment", "Tax", ["business"], ["gst amendment", "gst registration amendment", "change gst details"], None, "gst_amendment"),
    ("gst_return_filing", "GST Return Filing", "Tax", ["business"], ["gst return", "gst filing", "gstr filing"], None, "gst_return"),
    ("income_tax_return", "Income Tax Return Filing", "Tax", ["citizen", "business"], ["income tax return", "itr filing", "income tax filing"], None, "itr_filing"),
    ("income_tax_refund", "Income Tax Refund", "Tax", ["citizen", "business"], ["income tax refund", "itr refund", "tax refund"], None, "tax_refund"),
    ("tax_demand_response", "Tax Demand/Notice Response", "Tax", ["citizen", "business"], ["tax notice", "tax demand", "income tax notice", "demand response"], None, "tax_demand_response"),
    ("pan_services", "PAN Application/Correction", "Tax", ["citizen", "business"], ["pan card", "pan application", "pan correction"], None, "pan"),
    ("tan_services", "TAN Application/Correction", "Tax", ["business"], ["tan application", "tan correction"], None, "tan"),

    # Transport
    ("learner_driving_license", "Learner Driving Licence", "Transport", ["citizen"], ["learner license", "learner licence", "learning license", "llr"], None, "learner_license"),
    ("driving_license_renewal", "Driving Licence Renewal", "Transport", ["citizen"], ["driving license renewal", "driving licence renewal"], None, "renewed_driving_license"),
    ("vehicle_transfer", "Vehicle Ownership Transfer", "Transport", ["citizen", "business"], ["vehicle transfer", "transfer rc", "ownership transfer vehicle"], None, "updated_vehicle_record"),
    ("vehicle_fitness_certificate", "Vehicle Fitness Certificate", "Transport", ["business", "citizen"], ["vehicle fitness", "fitness certificate", "commercial vehicle fitness"], None, "fitness_certificate"),
    ("vehicle_permit", "Vehicle Permit", "Transport", ["business", "citizen"], ["vehicle permit", "transport permit", "goods carriage permit", "passenger permit"], None, "vehicle_permit"),
    ("vehicle_noc", "Vehicle NOC", "Transport", ["citizen", "business"], ["vehicle noc", "rto noc", "transport noc"], None, "vehicle_noc"),
    ("road_tax", "Motor Vehicle Tax", "Transport", ["citizen", "business"], ["road tax", "motor vehicle tax", "vehicle tax"], None, "vehicle_tax_receipt"),

    # Agriculture and rural
    ("pm_kisan_registration", "PM-KISAN Registration/Correction", "Agriculture", ["citizen"], ["pm kisan registration", "pm-kisan registration", "kisan registration"], None, "pm_kisan_record"),
    ("farmer_scheme_benefit", "Farmer Scheme Benefit", "Agriculture", ["citizen"], ["farmer scheme", "agriculture subsidy", "farmer subsidy"], None, "farmer_benefit"),
    ("soil_health_service", "Soil Health Card/Service", "Agriculture", ["citizen", "business"], ["soil health card", "soil testing"], None, "soil_health_record"),
    ("seed_license", "Seed Licence/Registration", "Agriculture", ["business"], ["seed license", "seed licence", "seed dealer license"], None, "seed_license"),
    ("fertilizer_license", "Fertilizer Licence/Registration", "Agriculture", ["business"], ["fertilizer license", "fertiliser licence", "fertilizer dealer"], None, "fertilizer_license"),
    ("pesticide_license", "Insecticide/Pesticide Licence", "Agriculture", ["business"], ["pesticide license", "insecticide license", "pesticide dealer"], None, "pesticide_license"),
    ("agricultural_market_license", "Agricultural Market/Trader Licence", "Agriculture", ["business"], ["mandi license", "agricultural market license", "market trader license"], None, "market_license"),
    ("mgnrega_job_card", "MGNREGA Job Card/Employment Demand", "Rural Development", ["citizen"], ["mgnrega job card", "nrega job card", "rural employment"], None, "mgnrega_record"),

    # Social welfare, food and benefits
    ("old_age_pension", "Old Age Social Pension", "Social Welfare", ["citizen"], ["old age pension", "senior citizen pension"], None, "social_pension"),
    ("widow_pension", "Widow Pension", "Social Welfare", ["citizen"], ["widow pension"], None, "social_pension"),
    ("disability_pension", "Disability Pension", "Social Welfare", ["citizen"], ["disability pension", "disabled pension"], None, "social_pension"),
    ("ration_card_update", "Ration Card Addition/Deletion/Correction", "Food & Civil Supplies", ["citizen"], ["ration card update", "add family member ration card", "ration card correction"], None, "updated_ration_card"),
    ("food_entitlement_claim", "Food Entitlement/Subsidy Claim", "Food & Civil Supplies", ["citizen"], ["food entitlement", "food subsidy claim", "pds benefit"], None, "food_benefit"),
    ("ayushman_card", "Ayushman Bharat Card/Eligibility", "Health", ["citizen"], ["ayushman card", "pmjay card", "ayushman bharat card"], None, "health_benefit"),
    ("housing_benefit", "Government Housing Benefit", "Housing", ["citizen"], ["housing subsidy", "pmay benefit", "government housing benefit"], None, "housing_benefit"),
    ("education_scholarship", "Education Scholarship/Benefit", "Education", ["citizen"], ["scholarship application", "education scholarship", "student scholarship"], None, "scholarship_decision"),
    ("pension_service", "Government Pension Service/Claim", "Pension", ["citizen"], ["government pension", "pension claim", "pension service"], None, "pension_outcome"),

    # Education
    ("school_transfer_certificate", "School Transfer/Leaving Certificate", "Education", ["citizen"], ["school leaving certificate", "transfer certificate", "tc"], None, "transfer_certificate"),
    ("education_migration_certificate", "Education Migration Certificate", "Education", ["citizen"], ["migration certificate", "university migration"], None, "migration_certificate"),
    ("degree_certificate", "Degree/Academic Certificate", "Education", ["citizen"], ["degree certificate", "academic certificate", "university certificate"], None, "degree_certificate"),
    ("teacher_registration", "Teacher/Professional Education Registration", "Education", ["citizen", "business"], ["teacher registration", "teacher licence", "teacher eligibility registration"], None, "teacher_registration"),
    ("apprenticeship_registration", "Apprenticeship Registration", "Skill/Employment", ["citizen", "business"], ["apprenticeship registration", "apprentice registration"], None, "apprenticeship_registration"),
    ("skill_training_application", "Government Skill Training Application", "Skill/Employment", ["citizen"], ["skill training", "government skill course", "skill development"], None, "training_enrolment"),

    # Police, justice and public accountability
    ("police_complaint", "Police Complaint/General Petition", "Police", ["citizen", "business"], ["police complaint", "police petition", "complaint to police"], None, "police_complaint"),
    ("fir_copy", "FIR Copy/Status", "Police", ["citizen", "business"], ["fir copy", "fir status", "first information report copy"], None, "fir_copy"),
    ("police_verification", "Police Verification", "Police", ["citizen", "business"], ["police verification", "address police verification", "tenant verification"], None, "police_verification"),
    ("rtI_application", "RTI Application/Transfer", "Information Commission", ["citizen", "business"], ["rti application", "right to information", "rti request"], None, "rti_response"),
    ("rti_first_appeal", "RTI First Appeal", "Information Commission", ["citizen", "business"], ["rti first appeal", "first appeal rti"], None, "rti_appeal"),
    ("government_grievance", "Government Grievance/Complaint", "Grievance", ["citizen", "business"], ["government grievance", "public grievance", "complaint government"], None, "grievance_resolution"),
    ("legal_aid_application", "Legal Aid Application", "Legal Services Authority", ["citizen"], ["legal aid", "free legal aid", "legal services authority"], None, "legal_aid"),
    ("court_certified_copy", "Court Certified Copy", "Courts", ["citizen", "business"], ["court certified copy", "certified court order", "court document copy"], None, "certified_court_copy"),
    ("court_case_filing_online", "Online Court Case Filing", "Courts", ["citizen", "business"], ["online court filing", "e filing court", "efile case"], None, "case_filing"),

    # Passport, citizenship and travel
    ("passport_renewal", "Passport Renewal", "Passport", ["citizen"], ["passport renewal", "renew passport"], None, "renewed_passport"),
    ("passport_reissue", "Passport Re-Issue", "Passport", ["citizen"], ["passport reissue", "passport re-issue"], None, "reissued_passport"),
    ("citizenship_application", "Citizenship Application/Registration", "Home Affairs", ["citizen"], ["citizenship application", "indian citizenship", "citizenship registration"], None, "citizenship_status"),
    ("oci_services", "OCI Application/Service", "External Affairs", ["citizen"], ["oci card", "overseas citizen india", "oci application"], None, "oci_card"),
    ("immigration_services", "Immigration/Travel Permission", "Home Affairs", ["citizen", "business"], ["immigration permission", "immigration service"], None, "immigration_outcome"),

    # Environment, forests and natural resources
    ("forest_permission", "Forest Permission/Clearance", "Forest", ["citizen", "business", "developer"], ["forest clearance", "forest permission", "forest department approval"], "commercial_project", "forest_permission"),
    ("tree_felling_permission", "Tree Felling Permission", "Forest", ["citizen", "business", "developer"], ["tree cutting permission", "tree felling", "tree removal permission"], None, "tree_permission"),
    ("wildlife_permission", "Wildlife/Protected Area Permission", "Forest", ["business", "developer", "citizen"], ["wildlife permission", "protected area permission", "wildlife clearance"], None, "wildlife_permission"),
    ("mining_lease", "Mining Lease/Permit", "Mines", ["business", "developer"], ["mining lease", "mining permit", "mineral concession"], "commercial_project", "mining_lease"),
    ("quarry_permission", "Quarry/Minor Mineral Permission", "Mines", ["business", "developer"], ["quarry permit", "minor mineral permit", "stone quarry license"], None, "quarry_permission"),

    # Procurement and public sector
    ("government_vendor_registration", "Government Vendor/Contractor Registration", "Procurement", ["business"], ["government vendor registration", "contractor registration", "vendor empanelment"], None, "vendor_registration"),
    ("government_tender_bid", "Government Tender/Bid Submission", "Procurement", ["business"], ["government tender", "tender bid", "government eprocurement"], None, "tender_submission"),
    ("procurement_contract_management", "Government Contract/Work Order Management", "Procurement", ["business"], ["government contract", "work order", "contract management"], None, "contract_record"),

    # Consumer and other regulatory services
    ("consumer_grievance", "Consumer Complaint/Redressal", "Consumer Affairs", ["citizen", "business"], ["consumer complaint", "consumer grievance", "consumer forum"], None, "consumer_resolution"),
    ("labour_complaint", "Labour Complaint/Inspection Request", "Labour", ["citizen", "business"], ["labour complaint", "labour grievance", "wage complaint"], None, "labour_resolution"),
    ("employment_exchange_registration", "Employment Exchange/Job-Seeker Registration", "Employment", ["citizen"], ["employment exchange", "job seeker registration", "employment registration"], None, "employment_registration"),
]

# Guard against accidental duplicate identifiers during catalog maintenance.
_seen = set()
for _row in INDIA_SERVICE_FAMILY_DEFINITIONS:
    if _row[0] in _seen:
        raise ValueError(f"Duplicate India service family: {_row[0]}")
    _seen.add(_row[0])
