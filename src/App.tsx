import { useState } from 'react';
import { Building2, Users, Shield, Code } from 'lucide-react';
import { PropertySearch } from './components/PropertySearch';
import { OfficerDashboard } from './components/OfficerDashboard';
import { FraudDetection } from './components/FraudDetection';
import { APIMarketplace } from './components/APIMarketplace';
import { TradeLicenseApplication } from './components/TradeLicenseApplication';
import { BuildingPermitApplication } from './components/BuildingPermitApplication';
import { WaterConnectionApplication } from './components/WaterConnectionApplication';
import { BirthCertificateApplication } from './components/BirthCertificateApplication';
import { DeathCertificateApplication } from './components/DeathCertificateApplication';
import { MedicalLicenseApplication } from './components/MedicalLicenseApplication';
import { ScholarshipApplication } from './components/ScholarshipApplication';
import { AdmissionApplication } from './components/AdmissionApplication';
import { TransferCertificateApplication } from './components/TransferCertificateApplication';
import { FactoryLicenseApplication } from './components/FactoryLicenseApplication';
import { PFESIApplication } from './components/PFESIApplication';
import { GSTApplication } from './components/GSTApplication';
import { CompanyApplication } from './components/CompanyApplication';
import { RationCardApplication } from './components/RationCardApplication';
import { PDSSubsidyApplication } from './components/PDSSubsidyApplication';
import { PoliceClearanceApplication } from './components/PoliceClearanceApplication';
import { FIRApplication } from './components/FIRApplication';
import { FarmerIDApplication } from './components/FarmerIDApplication';
import { CropInsuranceApplication } from './components/CropInsuranceApplication';
import { PMAYApplication } from './components/PMAYApplication';
import { AffordableHousingApplication } from './components/AffordableHousingApplication';
import { RERAProjectApplication } from './components/RERAProjectApplication';
import { RERACertificateApplication } from './components/RERACertificateApplication';
import { CourtCaseApplication } from './components/CourtCaseApplication';
import { ECourtApplication } from './components/ECourtApplication';
import { PassportApplication } from './components/PassportApplication';
import { VisaApplication } from './components/VisaApplication';

type View =
  | 'search' | 'officer' | 'fraud' | 'marketplace'
  | 'trade-license' | 'building-permit' | 'water-connection'
  | 'birth' | 'death' | 'medical-license' | 'scholarship' | 'admission' | 'transfer-certificate'
  | 'factory-license' | 'pf-esi'
  | 'gst' | 'company'
  | 'ration-card' | 'pds-subsidy'
  | 'police-clearance' | 'fir'
  | 'farmer' | 'crop-insurance'
  | 'pmay' | 'housing'
  | 'rera-project' | 'rera-certificate'
  | 'court-case' | 'e-court'
  | 'passport' | 'visa';

const navItems: { id: View; label: string; icon: string; activeClass: string }[] = [
  { id: 'search', label: 'Property', icon: '🏠', activeClass: 'bg-blue-600' },
  { id: 'trade-license', label: 'Trade License', icon: '🏪', activeClass: 'bg-green-600' },
  { id: 'building-permit', label: 'Building Permit', icon: '🏗️', activeClass: 'bg-purple-600' },
  { id: 'water-connection', label: 'Water', icon: '💧', activeClass: 'bg-teal-600' },
  { id: 'birth', label: 'Birth', icon: '👶', activeClass: 'bg-pink-600' },
  { id: 'death', label: 'Death', icon: '💀', activeClass: 'bg-gray-700' },
  { id: 'medical-license', label: 'Medical License', icon: '🏥', activeClass: 'bg-teal-600' },
  { id: 'scholarship', label: 'Scholarship', icon: '🎓', activeClass: 'bg-indigo-600' },
  { id: 'admission', label: 'Admission', icon: '📚', activeClass: 'bg-cyan-600' },
  { id: 'transfer-certificate', label: 'Transfer Certificate', icon: '📄', activeClass: 'bg-amber-600' },
  { id: 'factory-license', label: 'Factory License', icon: '🏭', activeClass: 'bg-orange-600' },
  { id: 'pf-esi', label: 'PF/ESI', icon: '👷', activeClass: 'bg-orange-700' },
  { id: 'gst', label: 'GST', icon: '🧾', activeClass: 'bg-emerald-600' },
  { id: 'company', label: 'Company (MCA)', icon: '🏢', activeClass: 'bg-slate-600' },
  { id: 'ration-card', label: 'Ration Card', icon: '🥫', activeClass: 'bg-yellow-600' },
  { id: 'pds-subsidy', label: 'PDS Subsidy', icon: '🌾', activeClass: 'bg-lime-600' },
  { id: 'police-clearance', label: 'Police Clearance', icon: '🛡️', activeClass: 'bg-blue-700' },
  { id: 'fir', label: 'FIR', icon: '📋', activeClass: 'bg-red-700' },
  { id: 'farmer', label: 'Farmer ID', icon: '🚜', activeClass: 'bg-green-700' },
  { id: 'crop-insurance', label: 'Crop Insurance', icon: '🌱', activeClass: 'bg-green-800' },
  { id: 'pmay', label: 'PMAY', icon: '🏚️', activeClass: 'bg-rose-600' },
  { id: 'housing', label: 'Housing', icon: '🏘️', activeClass: 'bg-rose-700' },
  { id: 'rera-project', label: 'RERA Project', icon: '🏗️', activeClass: 'bg-violet-600' },
  { id: 'rera-certificate', label: 'RERA Certificate', icon: '📜', activeClass: 'bg-violet-700' },
  { id: 'court-case', label: 'Court Case', icon: '⚖️', activeClass: 'bg-gray-800' },
  { id: 'e-court', label: 'E-Court', icon: '💻', activeClass: 'bg-gray-900' },
  { id: 'passport', label: 'Passport', icon: '📔', activeClass: 'bg-indigo-700' },
  { id: 'visa', label: 'Visa', icon: '✈️', activeClass: 'bg-sky-600' },
  { id: 'officer', label: 'Officer', icon: '👤', activeClass: 'bg-red-600' },
  { id: 'fraud', label: 'Fraud', icon: '🛡️', activeClass: 'bg-orange-600' },
  { id: 'marketplace', label: 'API', icon: '🔌', activeClass: 'bg-indigo-600' },
];

function App() {
  const [activeView, setActiveView] = useState<View>('search');

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md p-4 flex flex-wrap gap-2 justify-center">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveView(item.id)}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
              activeView === item.id ? `${item.activeClass} text-white` : 'bg-gray-200'
            }`}
          >
            <span>{item.icon}</span> {item.label}
          </button>
        ))}
      </nav>

      <div className="p-4 max-w-6xl mx-auto">
        {activeView === 'search' && <PropertySearch />}
        {activeView === 'trade-license' && <TradeLicenseApplication />}
        {activeView === 'building-permit' && <BuildingPermitApplication />}
        {activeView === 'water-connection' && <WaterConnectionApplication />}
        {activeView === 'officer' && <OfficerDashboard />}
        {activeView === 'fraud' && <FraudDetection />}
        {activeView === 'marketplace' && <APIMarketplace />}
        {activeView === 'birth' && <BirthCertificateApplication />}
        {activeView === 'death' && <DeathCertificateApplication />}
        {activeView === 'medical-license' && <MedicalLicenseApplication />}
        {activeView === 'scholarship' && <ScholarshipApplication />}
        {activeView === 'admission' && <AdmissionApplication />}
        {activeView === 'transfer-certificate' && <TransferCertificateApplication />}
        {activeView === 'factory-license' && <FactoryLicenseApplication />}
        {activeView === 'pf-esi' && <PFESIApplication />}
        {activeView === 'gst' && <GSTApplication />}
        {activeView === 'company' && <CompanyApplication />}
        {activeView === 'ration-card' && <RationCardApplication />}
        {activeView === 'pds-subsidy' && <PDSSubsidyApplication />}
        {activeView === 'police-clearance' && <PoliceClearanceApplication />}
        {activeView === 'fir' && <FIRApplication />}
        {activeView === 'farmer' && <FarmerIDApplication />}
        {activeView === 'crop-insurance' && <CropInsuranceApplication />}
        {activeView === 'pmay' && <PMAYApplication />}
        {activeView === 'housing' && <AffordableHousingApplication />}
        {activeView === 'rera-project' && <RERAProjectApplication />}
        {activeView === 'rera-certificate' && <RERACertificateApplication />}
        {activeView === 'court-case' && <CourtCaseApplication />}
        {activeView === 'e-court' && <ECourtApplication />}
        {activeView === 'passport' && <PassportApplication />}
        {activeView === 'visa' && <VisaApplication />}
      </div>
    </div>
  );
}

export default App;
