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

type View = 'search' | 'officer' | 'fraud' | 'marketplace' | 'trade-license' | 'building-permit' | 'water-connection' | 'birth' | 'death' | 'medical-license' | 'scholarship' | 'admission' | 'transfer-certificate';

function App() {
  const [activeView, setActiveView] = useState<View>('search');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-md p-4 flex flex-wrap gap-2 justify-center">
        <button
          onClick={() => setActiveView('search')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'search' ? 'bg-blue-600 text-white' : 'bg-gray-200'
          }`}
        >
          <Building2 className="w-4 h-4" /> Property
        </button>
        <button
          onClick={() => setActiveView('trade-license')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'trade-license' ? 'bg-green-600 text-white' : 'bg-gray-200'
          }`}
        >
          🏪 Trade License
        </button>
        <button
          onClick={() => setActiveView('building-permit')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'building-permit' ? 'bg-purple-600 text-white' : 'bg-gray-200'
          }`}
        >
          🏗️ Building Permit
        </button>
        <button
          onClick={() => setActiveView('water-connection')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'water-connection' ? 'bg-teal-600 text-white' : 'bg-gray-200'
          }`}
        >
          💧 Water Connection
        </button>
        <button
  onClick={() => setActiveView('birth')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'birth' ? 'bg-pink-600 text-white' : 'bg-gray-200'
  }`}
>
  👶 Birth
</button>
<button
  onClick={() => setActiveView('death')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'death' ? 'bg-gray-700 text-white' : 'bg-gray-200'
  }`}
>
  💀 Death
</button>
<button
  onClick={() => setActiveView('medical-license')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'medical-license' ? 'bg-teal-600 text-white' : 'bg-gray-200'
  }`}
>
  🏥 Medical License
</button>
        <button
  onClick={() => setActiveView('scholarship')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'scholarship' ? 'bg-indigo-600 text-white' : 'bg-gray-200'
  }`}
>
  🎓 Scholarship
</button>
<button
  onClick={() => setActiveView('admission')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'admission' ? 'bg-cyan-600 text-white' : 'bg-gray-200'
  }`}
>
  📚 Admission
</button>
<button
  onClick={() => setActiveView('transfer-certificate')}
  className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
    activeView === 'transfer-certificate' ? 'bg-amber-600 text-white' : 'bg-gray-200'
  }`}
>
  📄 Transfer Certificate
</button>
        <button
          onClick={() => setActiveView('officer')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'officer' ? 'bg-red-600 text-white' : 'bg-gray-200'
          }`}
        >
          
          <Users className="w-4 h-4" /> Officer
        </button>
        <button
          onClick={() => setActiveView('fraud')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'fraud' ? 'bg-orange-600 text-white' : 'bg-gray-200'
          }`}
        >
          <Shield className="w-4 h-4" /> Fraud
        </button>
        <button
          onClick={() => setActiveView('marketplace')}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            activeView === 'marketplace' ? 'bg-indigo-600 text-white' : 'bg-gray-200'
          }`}
        >
          <Code className="w-4 h-4" /> API
        </button>
      </nav>

      {/* Main Content */}
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
      </div>
    </div>
  );
}


export default App;
