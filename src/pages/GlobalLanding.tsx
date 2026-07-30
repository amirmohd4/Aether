import React, { useState } from 'react';
import { SearchBox } from '../components/SearchBox';
import { CountrySelector } from '../components/CountrySelector';
import { StateSelector } from '../components/StateSelector';
import { ServiceList, ServiceItem } from '../components/ServiceList';
import { IDField } from '../components/IDField';
import { ResultsView } from '../components/ResultsView';
import { getCountryConfig, getCountryStates } from '../configs/countriesData';
import { Globe, Loader2, ArrowLeft } from 'lucide-react';

export const GlobalLanding: React.FC = () => {
  const [step, setStep] = useState<'search' | 'country' | 'services' | 'state' | 'id' | 'processing' | 'results'>('search');
  
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [countryCode, setCountryCode] = useState<string>('');
  const [selectedService, setSelectedService] = useState<ServiceItem | null>(null);
  const [selectedState, setSelectedState] = useState<string>('');

  const handleSearchSubmit = (query: string) => {
    setSearchQuery(query);
    setStep('country');
  };

  const handleSelectCountry = (code: string) => {
    setCountryCode(code);
    setSelectedState('');
  };

  const handleCountryContinue = () => {
    if (!countryCode) return;
    setStep('services');
  };

  const handleSelectService = (service: ServiceItem) => {
    setSelectedService(service);
    const states = getCountryStates(countryCode);
    if (states && states.length > 0) {
      setStep('state');
    } else {
      setStep('id');
    }
  };

  const handleStateContinue = () => {
    setStep('id');
  };

  const handleSubmitID = (_idValue: string) => {
    setStep('processing');
    setTimeout(() => {
      setStep('results');
    }, 1500);
  };

  const handleDone = () => {
    setStep('search');
    setSearchQuery('');
    setCountryCode('');
    setSelectedService(null);
    setSelectedState('');
  };

  const countryConfig = countryCode ? getCountryConfig(countryCode) : null;

  return (
    <div className="min-h-screen bg-white text-slate-900 flex flex-col items-center justify-center p-4">
      
      {/* Centered layout, max-width 600px */}
      <div className="w-full max-w-[600px] mx-auto flex flex-col items-center text-center space-y-8 my-auto">
        
        {/* Logo & Tagline */}
        <div className="flex flex-col items-center space-y-3 cursor-pointer" onClick={handleDone}>
          <div className="w-14 h-14 rounded-2xl bg-[#1a365d] flex items-center justify-center text-white shadow-md">
            <Globe className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h1 className="text-3xl font-bold text-[#1a365d] tracking-tight">
              Aether
            </h1>
            <p className="text-base font-medium text-slate-600">
              Government services, simplified.
            </p>
          </div>
        </div>

        {/* STEP 1: Search Box */}
        {step === 'search' && (
          <div className="w-full">
            <SearchBox onSearch={handleSearchSubmit} />
          </div>
        )}

        {/* STEP 2: Country Selector */}
        {step === 'country' && (
          <div className="w-full">
            <CountrySelector
              selectedCountryCode={countryCode}
              onSelectCountry={handleSelectCountry}
              onContinue={handleCountryContinue}
              onBack={() => setStep('search')}
            />
          </div>
        )}

        {/* STEP 3: Service Selection List for Country */}
        {step === 'services' && (
          <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <button
                type="button"
                onClick={() => setStep('country')}
                className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-[#1a365d] transition-colors cursor-pointer"
              >
                <ArrowLeft className="w-4 h-4" />
                Change Country ({countryConfig?.flag} {countryConfig?.country_name})
              </button>
            </div>

            <ServiceList
              countryCode={countryCode}
              searchQuery={searchQuery}
              onSelectService={handleSelectService}
            />
          </div>
        )}

        {/* STEP 4: State Selector (If applicable for selected country) */}
        {step === 'state' && (
          <div className="w-full">
            <StateSelector
              countryCode={countryCode}
              selectedState={selectedState}
              onSelectState={setSelectedState}
              onContinue={handleStateContinue}
              onBack={() => setStep('services')}
            />
          </div>
        )}

        {/* STEP 5: ID Field */}
        {step === 'id' && (
          <div className="w-full">
            <IDField
              onSubmitID={handleSubmitID}
              onBack={() => {
                const states = getCountryStates(countryCode);
                if (states && states.length > 0) {
                  setStep('state');
                } else {
                  setStep('services');
                }
              }}
            />
          </div>
        )}

        {/* STEP 6: Processing */}
        {step === 'processing' && (
          <div className="w-full bg-white border border-slate-200 rounded-2xl p-8 shadow-xl text-center space-y-4">
            <Loader2 className="w-10 h-10 text-[#1a365d] animate-spin mx-auto" />
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-slate-900">
                Processing your request...
              </h3>
              <p className="text-xs text-slate-500">
                Connecting to official digital service registry
              </p>
            </div>
          </div>
        )}

        {/* STEP 7: Results View */}
        {step === 'results' && (
          <div className="w-full">
            <ResultsView
              serviceName={selectedService?.name || searchQuery || 'Government Service'}
              countryName={countryConfig?.country_name}
              stateName={selectedState}
              onDone={handleDone}
            />
          </div>
        )}

      </div>
    </div>
  );
};
