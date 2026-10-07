export type ServiceConfig = {
  id: string;
  label: string;
  icon: string;
  component: string;
  endpoint: string;
};

/**
 * User-facing service shortcuts. This list mirrors the 34-service Aether
 * backend registry; specialized forms are used where available and the
 * generic Aether service surface is used for services that do not need a
 * bespoke legacy form.
 */
export const servicesConfig: ServiceConfig[] = [
  { id: 'property-registration', label: 'Property Registration', icon: '🏠', component: 'PropertyRegistrationApplication', endpoint: '/property-registration' },
  { id: 'mutation', label: 'Land / Property Mutation', icon: '🌾', component: 'MutationApplication', endpoint: '/mutation' },
  { id: 'encumbrance-certificate', label: 'Encumbrance Certificate', icon: '🔍', component: 'EncumbranceCertificateApplication', endpoint: '/encumbrance-certificate' },
  { id: 'land-conversion', label: 'Land Conversion', icon: '🗺️', component: 'LandConversionApplication', endpoint: '/land-conversion' },
  { id: 'title-verification', label: 'Title Verification', icon: '📜', component: 'TitleVerificationApplication', endpoint: '/title-verification' },
  { id: 'trade-license', label: 'Trade License', icon: '🏬', component: 'TradeLicenseApplication', endpoint: '/trade-license' },
  { id: 'building-permit', label: 'Building Permit', icon: '🏗️', component: 'BuildingPermitApplication', endpoint: '/building-permit' },
  { id: 'water-connection', label: 'Water Connection', icon: '🚰', component: 'WaterConnectionApplication', endpoint: '/water-connection' },
  { id: 'birth-certificate', label: 'Birth Certificate', icon: '🆔', component: 'BirthCertificateApplication', endpoint: '/birth-certificate' },
  { id: 'death-certificate', label: 'Death Certificate', icon: '📄', component: 'DeathCertificateApplication', endpoint: '/death-certificate' },
  { id: 'medical-license', label: 'Medical License', icon: '🩺', component: 'MedicalLicenseApplication', endpoint: '/medical-license' },
  { id: 'scholarship', label: 'Scholarship', icon: '🎓', component: 'ScholarshipApplication', endpoint: '/scholarship' },
  { id: 'admission', label: 'Education Admission', icon: '🏫', component: 'AdmissionApplication', endpoint: '/admission' },
  { id: 'transfer-certificate', label: 'Transfer Certificate', icon: '📘', component: 'TransferCertificateApplication', endpoint: '/transfer-certificate' },
  { id: 'driving-license', label: 'Driving License', icon: '🚗', component: 'DrivingLicenseApplication', endpoint: '/driving-license' },
  { id: 'vehicle-registration', label: 'Vehicle Registration', icon: '🚙', component: 'VehicleRegistrationApplication', endpoint: '/vehicle-registration' },
  { id: 'factory-license', label: 'Factory License', icon: '🏭', component: 'FactoryLicenseApplication', endpoint: '/factory-license' },
  { id: 'pf-esi', label: 'PF/ESI Registration', icon: '👷', component: 'PFESIApplication', endpoint: '/pf-esi' },
  { id: 'gst', label: 'GST Registration', icon: '🧾', component: 'GSTApplication', endpoint: '/gst' },
  { id: 'company', label: 'Company Registration (MCA)', icon: '🏢', component: 'CompanyApplication', endpoint: '/company' },
  { id: 'ration-card', label: 'Ration Card', icon: '🥫', component: 'RationCardApplication', endpoint: '/ration-card' },
  { id: 'pds-subsidy', label: 'PDS Subsidy', icon: '🌾', component: 'PDSSubsidyApplication', endpoint: '/pds-subsidy' },
  { id: 'police-clearance', label: 'Police Clearance Certificate', icon: '🛡️', component: 'PoliceClearanceApplication', endpoint: '/police-clearance' },
  { id: 'fir', label: 'FIR Report', icon: '📋', component: 'FIRApplication', endpoint: '/fir' },
  { id: 'farmer', label: 'Farmer ID', icon: '🚜', component: 'FarmerIDApplication', endpoint: '/farmer' },
  { id: 'crop-insurance', label: 'Crop Insurance', icon: '🌱', component: 'CropInsuranceApplication', endpoint: '/crop-insurance' },
  { id: 'pmay', label: 'PMAY Application', icon: '🏠', component: 'PMAYApplication', endpoint: '/pmay' },
  { id: 'housing', label: 'Affordable Housing', icon: '🏘️', component: 'AffordableHousingApplication', endpoint: '/housing' },
  { id: 'rera-project', label: 'RERA Project Registration', icon: '🏗️', component: 'RERAProjectApplication', endpoint: '/rera-project' },
  { id: 'rera-certificate', label: 'RERA Certificate', icon: '📜', component: 'RERACertificateApplication', endpoint: '/rera-certificate' },
  { id: 'court-case', label: 'Court Case Filing', icon: '⚖️', component: 'CourtCaseApplication', endpoint: '/court-case' },
  { id: 'e-court', label: 'E-Court', icon: '💻', component: 'ECourtApplication', endpoint: '/e-court' },
  { id: 'passport', label: 'Passport Application', icon: '📔', component: 'PassportApplication', endpoint: '/passport' },
  { id: 'visa', label: 'Visa Services', icon: '✈️', component: 'VisaApplication', endpoint: '/visa' },
  { id: 'food-business-license', label: 'Food Business License / Registration', icon: '🍲', component: 'TradeLicenseApplication', endpoint: '/food-business-license' },
];
