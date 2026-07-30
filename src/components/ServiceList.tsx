import React from 'react';
import { ChevronRight } from 'lucide-react';

export interface ServiceItem {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: string;
}

export const INDIA_32_SERVICES: ServiceItem[] = [
  { id: 'in_prop_reg', name: 'Property Registration & Title Deed', category: 'Property & Land', description: 'Instant land title verification, encumbrance audit, and conveyance deed registration', icon: '🏠' },
  { id: 'in_dl_renewal', name: 'Driving Licence Renewal & Transfer', category: 'Transport & Driving', description: 'Biometric verification, traffic challan check, and mParivahan pass issuance', icon: '🚗' },
  { id: 'in_biz_inc', name: 'SPICe+ Company Incorporation', category: 'Business & Licenses', description: 'Single-window incorporation covering DIN, PAN, TAN, and GSTIN registration', icon: '🏢' },
  { id: 'in_birth_cert', name: 'Birth Certificate Issuance & Correction', category: 'Identity & Documents', description: 'Apply for official birth registration certificate or record correction', icon: '🆔' },
  { id: 'in_death_cert', name: 'Death Certificate Registration', category: 'Identity & Documents', description: 'Register official death record and issue verified legal certificate', icon: '📄' },
  { id: 'in_marriage_cert', name: 'Marriage Certificate Registration', category: 'Identity & Documents', description: 'Register marriage under Special Marriage Act or Hindu Marriage Act', icon: '💍' },
  { id: 'in_khata_mutation', name: 'Land Revenue & Khata Mutation', category: 'Property & Land', description: 'Transfer property tax revenue record and obtain updated Khata certificate', icon: '🌾' },
  { id: 'in_itr_tax', name: 'Income Tax Clearance & Assessment', category: 'Taxes & Revenue', description: 'Obtain tax status clearance certificate and assessment audit', icon: '🧾' },
  { id: 'in_trade_license', name: 'Commercial Trade License', category: 'Business & Licenses', description: 'Issue or renew local municipal commercial trade operation permit', icon: '🏬' },
  { id: 'in_building_permit', name: 'Building Plan Approval & Permit', category: 'Property & Land', description: 'Submit architectural plan for sanction and structural clearance', icon: '🏗️' },
  { id: 'in_crop_insurance', name: 'PM Fasal Bima Crop Insurance', category: 'Health & Agriculture', description: 'Agricultural yield coverage registration and claim processing', icon: '🌱' },
  { id: 'in_caste_domicile', name: 'Caste & Domicile Certificate', category: 'Identity & Documents', description: 'Issue government residence and community identity verification', icon: '📜' },
  { id: 'in_ration_card', name: 'Ration Card Pass & Family Addition', category: 'Health & Welfare', description: 'Apply for national food security card or update family members', icon: '🍚' },
  { id: 'in_court_efiling', name: 'Court Case E-Filing & Order Audit', category: 'Legal & Courts', description: 'E-file judicial petition and audit digital court orders', icon: '⚖️' },
  { id: 'in_passport_renew', name: 'Passport Renewal & Tatkaal Pass', category: 'Identity & Documents', description: 'Re-issue passport or request expedited Tatkaal processing', icon: '🛂' },
  { id: 'in_gst_reg', name: 'GST Registration & Filing', category: 'Taxes & Revenue', description: 'Obtain Goods & Services Tax identification number and file returns', icon: '📊' },
  { id: 'in_elec_conn', name: 'New Electricity Utility Connection', category: 'Utilities & Power', description: 'Request new residential or commercial power meter connection', icon: '⚡' },
  { id: 'in_water_conn', name: 'Water & Sewage Connection Permit', category: 'Utilities & Power', description: 'Apply for municipal drinking water supply and sanitation pipeline', icon: '🚰' },
  { id: 'in_police_pcc', name: 'Police Clearance Certificate (PCC)', category: 'Legal & Security', description: 'Background verification report for employment or international visa', icon: '👮' },
  { id: 'in_fire_noc', name: 'Fire Safety NOC Clearance', category: 'Business & Licenses', description: 'Inspect establishment for fire compliance certificate issuance', icon: '🔥' },
  { id: 'in_legal_heir', name: 'Legal Heirship & Succession Certificate', category: 'Legal & Courts', description: 'Establish legal inheritance rights for deceased asset transfer', icon: '📋' },
  { id: 'in_arms_license', name: 'Arms License Application & Renewal', category: 'Legal & Security', description: 'Permit application for personal security firearm under Arms Act', icon: '🛡️' },
  { id: 'in_pension_life', name: 'Pension Dispersal & Jeevan Pramaan', category: 'Health & Welfare', description: 'Submit digital life certificate for monthly pension credit', icon: '👵' },
  { id: 'in_fssai_food', name: 'FSSAI Food Safety License', category: 'Business & Licenses', description: 'Registration and license for food manufacturers, vendors, and restaurants', icon: '🍲' },
  { id: 'in_pcb_clearance', name: 'Pollution Control Board Clearance', category: 'Environment & Industry', description: 'Consent to establish (CTE) and consent to operate (CTO) industrial unit', icon: '🏭' },
  { id: 'in_encumbrance_ec', name: 'Encumbrance Certificate (EC) Search', category: 'Property & Land', description: 'Audit registered transactions and encumbrances on land parcel', icon: '🔍' },
  { id: 'in_excise_permit', name: 'Excise & Commercial Alcohol Permit', category: 'Business & Licenses', description: 'Permit for commercial hospitality distribution under state excise', icon: '🍷' },
  { id: 'in_shops_est', name: 'Shops & Establishment License', category: 'Business & Licenses', description: 'Mandatory commercial registration for shops and office premises', icon: '🛍️' },
  { id: 'in_industrial_land', name: 'Industrial Single Window Land Allotment', category: 'Environment & Industry', description: 'Apply for manufacturing land plot allocation in industrial park', icon: '🏭' },
  { id: 'in_labour_license', name: 'Contract Labour Employment License', category: 'Business & Licenses', description: 'License for engaging contract personnel in commercial projects', icon: '👷' },
  { id: 'in_stamp_val', name: 'Stamp Duty & Guidance Valuation', category: 'Taxes & Revenue', description: 'Calculate official property guidance value and stamp duty liability', icon: '💰' },
  { id: 'in_senior_citizen', name: 'Senior Citizen ID & Healthcare Pass', category: 'Health & Welfare', description: 'Issue special welfare benefits pass and medical priority card', icon: '🏥' }
];

export const GENERIC_SERVICES: ServiceItem[] = [
  { id: 'gen_prop_reg', name: 'Property Registration', category: 'Property & Land', description: 'Register land title deed and verify ownership records', icon: '🏠' },
  { id: 'gen_birth_cert', name: 'Birth Certificate', category: 'Identity & Documents', description: 'Apply for or retrieve official birth registration certificate', icon: '🆔' },
  { id: 'gen_biz_license', name: 'Business License', category: 'Business & Licenses', description: 'Register a commercial business or renew operating license', icon: '📄' },
  { id: 'gen_driving_license', name: 'Driving License', category: 'Transport & Driving', description: 'Apply for driver license or renew existing driving permit', icon: '🚗' },
  { id: 'gen_passport_renew', name: 'Passport Renewal', category: 'Identity & Documents', description: 'Renew passport or apply for international travel document', icon: '🛂' },
  { id: 'gen_tax_clearance', name: 'Tax Clearance Certificate', category: 'Taxes & Revenue', description: 'Obtain official tax status clearance certificate', icon: '🧾' },
  { id: 'gen_building_permit', name: 'Building Permit', category: 'Property & Land', description: 'Apply for construction approval or renovation permit', icon: '🏗️' },
  { id: 'gen_court_filing', name: 'Court Case Filing', category: 'Legal & Courts', description: 'Submit legal document filing or check judicial case status', icon: '⚖️' },
  { id: 'gen_crop_insurance', name: 'Crop Insurance', category: 'Health & Agriculture', description: 'Register for agricultural support and crop disaster coverage', icon: '🌾' }
];

interface ServiceListProps {
  countryCode: string;
  searchQuery?: string;
  onSelectService: (service: ServiceItem) => void;
}

export const ServiceList: React.FC<ServiceListProps> = ({
  countryCode,
  searchQuery = '',
  onSelectService
}) => {
  const isIndia = countryCode.toUpperCase() === 'IN';
  const rawServices = isIndia ? INDIA_32_SERVICES : GENERIC_SERVICES;

  const filteredServices = searchQuery.trim()
    ? rawServices.filter(
        s => s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
             s.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
             s.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : rawServices;

  return (
    <div className="w-full space-y-3 text-left">
      <div className="flex items-center justify-between px-1">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
          {isIndia ? 'Services in India (32 Services)' : 'Available Services'}
        </span>
        <span className="text-xs text-slate-400 font-medium">
          {filteredServices.length} service{filteredServices.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="grid grid-cols-1 gap-2.5 max-h-80 overflow-y-auto pr-1">
        {filteredServices.length === 0 ? (
          <div className="p-4 text-center bg-slate-50 border border-slate-200 rounded-xl text-slate-500 text-sm">
            No services matching "{searchQuery}" found for this country.
          </div>
        ) : (
          filteredServices.map((service) => (
            <button
              key={service.id}
              id={`btn-service-${service.id}`}
              onClick={() => onSelectService(service)}
              className="w-full text-left p-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-[#1a365d] transition-all flex items-center justify-between gap-3 group shadow-xs cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl flex-shrink-0 p-2 rounded-lg bg-slate-100">
                  {service.icon}
                </span>
                <div>
                  <div className="font-bold text-sm text-slate-900 group-hover:text-[#1a365d] transition-colors">
                    {service.name}
                  </div>
                  <div className="text-xs text-slate-500 line-clamp-1">
                    {service.description}
                  </div>
                </div>
              </div>

              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-[#1a365d] group-hover:translate-x-0.5 transition-all flex-shrink-0" />
            </button>
          ))
        )}
      </div>
    </div>
  );
};
