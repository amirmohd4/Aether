export type ServiceConfig = {
  id: string;
  label: string;
  icon: string;
  component: string;
  endpoint: string;
};

export const servicesConfig: ServiceConfig[] = [
  // Department 1: Labour Department
  { id: 'factory-license', label: 'Factory License', icon: '🏭', component: 'FactoryLicenseApplication', endpoint: '/factory-license' },
  { id: 'pf-esi', label: 'PF/ESI Registration', icon: '👷', component: 'PFESIApplication', endpoint: '/pf-esi' },

  // Department 2: Finance Department
  { id: 'gst', label: 'GST Registration', icon: '🧾', component: 'GSTApplication', endpoint: '/gst' },
  { id: 'company', label: 'Company Registration (MCA)', icon: '🏢', component: 'CompanyApplication', endpoint: '/company' },

  // Department 3: Food & Civil Supplies
  { id: 'ration-card', label: 'Ration Card', icon: '🥫', component: 'RationCardApplication', endpoint: '/ration-card' },
  { id: 'pds-subsidy', label: 'PDS Subsidy', icon: '🌾', component: 'PDSSubsidyApplication', endpoint: '/pds-subsidy' },

  // Department 4: Police Department
  { id: 'police-clearance', label: 'Police Clearance Certificate', icon: '🛡️', component: 'PoliceClearanceApplication', endpoint: '/police-clearance' },
  { id: 'fir', label: 'FIR Report', icon: '📋', component: 'FIRApplication', endpoint: '/fir' },

  // Department 5: Agriculture Department
  { id: 'farmer', label: 'Farmer ID', icon: '🚜', component: 'FarmerIDApplication', endpoint: '/farmer' },
  { id: 'crop-insurance', label: 'Crop Insurance', icon: '🌱', component: 'CropInsuranceApplication', endpoint: '/crop-insurance' },

  // Department 6: Housing Department
  { id: 'pmay', label: 'PMAY Application', icon: '🏠', component: 'PMAYApplication', endpoint: '/pmay' },
  { id: 'housing', label: 'Affordable Housing', icon: '🏘️', component: 'AffordableHousingApplication', endpoint: '/housing' },

  // Department 7: RERA Department
  { id: 'rera-project', label: 'RERA Project Registration', icon: '🏗️', component: 'RERAProjectApplication', endpoint: '/rera-project' },
  { id: 'rera-certificate', label: 'RERA Certificate', icon: '📜', component: 'RERACertificateApplication', endpoint: '/rera-certificate' },

  // Department 8: Courts Department
  { id: 'court-case', label: 'Court Case Filing', icon: '⚖️', component: 'CourtCaseApplication', endpoint: '/court-case' },
  { id: 'e-court', label: 'E-Court', icon: '💻', component: 'ECourtApplication', endpoint: '/e-court' },

  // Department 9: Passport/MEA
  { id: 'passport', label: 'Passport Application', icon: '📔', component: 'PassportApplication', endpoint: '/passport' },
  { id: 'visa', label: 'Visa Services', icon: '✈️', component: 'VisaApplication', endpoint: '/visa' },
];
