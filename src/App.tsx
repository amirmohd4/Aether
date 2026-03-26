import { useState } from 'react';
import { PropertySearch } from './components/PropertySearch';
import { OfficerDashboard } from './components/OfficerDashboard';
import { FraudDetection } from './components/FraudDetection';
import { APIMarketplace } from './components/APIMarketplace';
import { Building2, Users, Shield, Map, Zap, Code } from 'lucide-react';

type View = 'search' | 'officer' | 'fraud' | 'marketplace';

function App() {
  const [activeView, setActiveView] = useState<View>('search');
  const [selectedState, setSelectedState] = useState('karnataka');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100">
      <header className="bg-white shadow-md border-b-4 border-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Building2 className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Aether GovOS</h1>
                <p className="text-sm text-gray-600">One API for all government services</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Map className="w-5 h-5 text-gray-600" />
                <select
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg bg-white text-gray-700 font-medium focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="karnataka">Karnataka</option>
                  <option value="jk">Jammu & Kashmir</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-1">
            <button
              onClick={() => setActiveView('search')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${
                activeView === 'search'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
              data-testid="property-search-tab"
            >
              <Shield className="w-5 h-5" />
              Property Search
            </button>
            <button
              onClick={() => setActiveView('officer')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${
                activeView === 'officer'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
              data-testid="officer-dashboard-tab"
            >
              <Users className="w-5 h-5" />
              Officer Dashboard
            </button>
            <button
              onClick={() => setActiveView('fraud')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${
                activeView === 'fraud'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
              data-testid="fraud-detection-tab"
            >
              <Zap className="w-5 h-5" />
              AI Fraud Detection
            </button>
            <button
              onClick={() => setActiveView('marketplace')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${
                activeView === 'marketplace'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
              data-testid="api-marketplace-tab"
            >
              <Code className="w-5 h-5" />
              API Marketplace
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'search' && <PropertySearch selectedState={selectedState} />}
        {activeView === 'officer' && <OfficerDashboard selectedState={selectedState} />}
        {activeView === 'fraud' && <FraudDetection selectedState={selectedState} />}
        {activeView === 'marketplace' && <APIMarketplace />}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>Aether GovOS - Government Integration Operating System</p>
            <p className="mt-1">Powered by FastAPI, PostgreSQL & React</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
