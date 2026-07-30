import React, { useState, useMemo, useEffect } from 'react';
import { 
  X, Globe, Shield, Sparkles, CheckCircle2, ChevronRight, ArrowLeft, 
  Search, Lock, Check, FileCheck, Building2, Download, RefreshCw, AlertCircle
} from 'lucide-react';
import { ALL_UN_COUNTRIES, getCountryConfig, getCountryStates, CountryConfig } from '../configs/countriesData';
import { ServiceSearch, ServiceItem, MASTER_GLOBAL_SERVICES } from './ServiceSearch';

interface StartFlowProps {
  isOpen: boolean;
  onClose: () => void;
  initialCountryCode?: string;
}

export const StartFlow: React.FC<StartFlowProps> = ({
  isOpen,
  onClose,
  initialCountryCode = 'IN'
}) => {
  // Steps: 'search' -> 'country_state' -> 'id_entry' -> 'processing' -> 'completed'
  const [step, setStep] = useState<'search' | 'country_state' | 'id_entry' | 'processing' | 'completed'>('search');

  // Selected state
  const [selectedService, setSelectedService] = useState<ServiceItem | null>(null);
  const [selectedCountryCode, setSelectedCountryCode] = useState<string>(initialCountryCode);
  const [selectedState, setSelectedState] = useState<string>('');
  const [nationalId, setNationalId] = useState<string>('');

  // Country search inside modal dropdown
  const [countryQuery, setCountryQuery] = useState('');
  const [selectedRegion, setSelectedRegion] = useState<string>('All');

  // Processing animation steps
  const [processProgress, setProcessProgress] = useState(0);
  const [activeStepIndex, setActiveStepIndex] = useState(0);

  const countryConfig: CountryConfig = useMemo(() => {
    return getCountryConfig(selectedCountryCode);
  }, [selectedCountryCode]);

  const countryStates = useMemo(() => {
    return getCountryStates(selectedCountryCode);
  }, [selectedCountryCode]);

  // Reset state when modal opens
  useEffect(() => {
    if (isOpen) {
      setStep('search');
      setSelectedService(null);
      setNationalId('');
      setProcessProgress(0);
      setActiveStepIndex(0);
    }
  }, [isOpen]);

  // Handle service selection
  const handleServiceSelect = (service: ServiceItem) => {
    setSelectedService(service);
    setStep('country_state');
  };

  // Handle country change
  const handleCountrySelect = (code: string) => {
    setSelectedCountryCode(code);
    setSelectedState(''); // reset state
  };

  // Processing simulation effect
  useEffect(() => {
    if (step === 'processing') {
      const interval = setInterval(() => {
        setProcessProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            setTimeout(() => setStep('completed'), 500);
            return 100;
          }
          const next = prev + 10;
          if (next > 75) setActiveStepIndex(3);
          else if (next > 50) setActiveStepIndex(2);
          else if (next > 25) setActiveStepIndex(1);
          return next;
        });
      }, 250);

      return () => clearInterval(interval);
    }
  }, [step]);

  // Start Processing
  const handleStartProcessing = (e: React.FormEvent) => {
    e.preventDefault();
    if (!nationalId.trim()) return;
    setStep('processing');
    setProcessProgress(0);
    setActiveStepIndex(0);
  };

  const filteredCountries = useMemo(() => {
    return ALL_UN_COUNTRIES.filter((c) => {
      const matchesSearch = 
        c.name.toLowerCase().includes(countryQuery.toLowerCase()) ||
        c.code.toLowerCase().includes(countryQuery.toLowerCase()) ||
        c.idName.toLowerCase().includes(countryQuery.toLowerCase());
      
      const matchesRegion = selectedRegion === 'All' || c.region === selectedRegion;

      return matchesSearch && matchesRegion;
    });
  }, [countryQuery, selectedRegion]);

  if (!isOpen) return null;

  const executionSteps = [
    { title: "National ID & Identity Authentication", detail: `Verifying ${countryConfig.id_system.name}...` },
    { title: "Sovereign Registry Ledger Audit", detail: `Querying ${countryConfig.country_name} Ministry Database...` },
    { title: "AI Land & Fraud Risk Scoring", detail: "Checking zero-knowledge encumbrance records (0% Risk)..." },
    { title: "e-Deed & Seal Generation", detail: "Recording cryptographic transaction block..." }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto bg-slate-950/80 backdrop-blur-md animate-fade-in">
      
      {/* Modal Card */}
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-3xl shadow-2xl overflow-hidden my-auto space-y-0">
        
        {/* Header Bar */}
        <div className="p-5 bg-slate-950 border-b border-slate-800 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 font-black shadow-md shadow-emerald-500/20">
              <Globe className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-white">Aether GovOS</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60 font-semibold">
                  195 UN Nations Engine
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {step === 'search' && 'Step 1 of 4: Search & Select Service'}
                {step === 'country_state' && 'Step 2 of 4: Select Country & Region'}
                {step === 'id_entry' && 'Step 3 of 4: Enter Sovereign ID'}
                {step === 'processing' && 'Step 4 of 4: Autonomous Processing'}
                {step === 'completed' && 'Service Issued Successfully'}
              </p>
            </div>
          </div>

          <button
            id="btn-close-start-flow"
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-6">
          
          {/* STEP 1: SEARCH SERVICE */}
          {step === 'search' && (
            <div className="space-y-4">
              <div className="text-center space-y-1">
                <h3 className="text-xl font-black text-white">What service do you need today?</h3>
                <p className="text-xs text-slate-400">Search from birth certificates, property titles, business licenses, or driving permits.</p>
              </div>

              <ServiceSearch onSelectService={handleServiceSelect} />
            </div>
          )}

          {/* STEP 2: SELECT COUNTRY & STATE */}
          {step === 'country_state' && selectedService && (
            <div className="space-y-5">
              <button
                onClick={() => setStep('search')}
                className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-emerald-400 font-semibold"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back to Search</span>
              </button>

              {/* Selected Service Preview Badge */}
              <div className="flex items-center justify-between p-3.5 bg-slate-950 rounded-2xl border border-slate-800">
                <div className="flex items-center gap-3">
                  <span className="text-2xl p-2 rounded-xl bg-slate-900 border border-slate-800">{selectedService.icon}</span>
                  <div>
                    <span className="text-xs font-semibold text-emerald-400 block">Selected Service</span>
                    <span className="font-bold text-sm text-white">{selectedService.name}</span>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
                  {selectedService.processingTime}
                </span>
              </div>

              {/* Country Selector */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center justify-between">
                  <span>1. Select Sovereign Country (195 UN Members)</span>
                  <span className="text-emerald-400 font-normal">{countryConfig.country_name} ({countryConfig.country_code})</span>
                </label>

                {/* Search Box */}
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={countryQuery}
                    onChange={(e) => setCountryQuery(e.target.value)}
                    placeholder="Search 195 countries by name or ID system..."
                    className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                  />
                </div>

                {/* Country Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-48 overflow-y-auto pr-1">
                  {filteredCountries.slice(0, 30).map((c) => {
                    const isSelected = c.code === selectedCountryCode;
                    return (
                      <button
                        key={c.code}
                        id={`btn-modal-country-${c.code.toLowerCase()}`}
                        onClick={() => handleCountrySelect(c.code)}
                        className={`flex items-center gap-2.5 p-2.5 rounded-xl border text-left transition-all ${
                          isSelected
                            ? 'bg-emerald-950 border-emerald-500 text-white font-bold ring-1 ring-emerald-500/50'
                            : 'bg-slate-950/80 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-800'
                        }`}
                      >
                        <span className="text-lg flex-shrink-0">{c.flag}</span>
                        <div className="min-w-0 flex-1">
                          <div className="font-semibold text-xs truncate">{c.name}</div>
                          <div className="text-[9px] text-slate-500 truncate">{c.idName}</div>
                        </div>
                        {isSelected && <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* State / Region Selector if applicable */}
              {countryStates && countryStates.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <label className="text-xs font-bold text-slate-200 uppercase tracking-wider block">
                    2. Select State / Region / Province
                  </label>
                  <select
                    id="select-state-region"
                    value={selectedState}
                    onChange={(e) => setSelectedState(e.target.value)}
                    className="w-full p-3 bg-slate-950 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500"
                  >
                    <option value="">-- Select State / Province --</option>
                    {countryStates.map((st) => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>
              )}

              {/* Continue CTA */}
              <button
                id="btn-continue-to-id"
                onClick={() => setStep('id_entry')}
                className="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-sm shadow-xl shadow-emerald-500/20 hover:scale-[1.01] transition-transform flex items-center justify-center gap-2"
              >
                <span>Continue to Sovereign ID Verification</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* STEP 3: ENTER NATIONAL ID / DIGITAL ID */}
          {step === 'id_entry' && selectedService && (
            <form onSubmit={handleStartProcessing} className="space-y-5">
              <button
                type="button"
                onClick={() => setStep('country_state')}
                className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-emerald-400 font-semibold"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back to Country & State</span>
              </button>

              <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>Selected Country:</span>
                  <span className="font-bold text-white flex items-center gap-1.5">
                    <span className="text-lg">{countryConfig.flag}</span>
                    <span>{countryConfig.country_name}</span>
                    {selectedState && <span className="text-emerald-400">({selectedState})</span>}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>Service Requested:</span>
                  <span className="font-bold text-emerald-400">{selectedService.name}</span>
                </div>
              </div>

              {/* Abstracted ID Input Field */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <span>Enter your National ID / Digital ID</span>
                </label>

                <div className="p-3 bg-emerald-950/40 rounded-xl border border-emerald-800/50 text-[11px] text-emerald-300 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>
                    Auto-detected ID Engine for <strong>{countryConfig.country_name}</strong>: <strong>{countryConfig.id_system.name}</strong>
                  </span>
                </div>

                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    id="input-national-id"
                    type="text"
                    required
                    value={nationalId}
                    onChange={(e) => setNationalId(e.target.value)}
                    placeholder={`e.g. ${countryConfig.id_system.format}`}
                    className="w-full pl-10 pr-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-sm font-mono text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <p className="text-[10px] text-slate-500">
                  Encrypted end-to-end with W3C Verifiable Credentials & Zero-Knowledge Proofs.
                </p>
              </div>

              {/* Submit CTA */}
              <button
                id="btn-process-service"
                type="submit"
                className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-sm shadow-xl shadow-emerald-500/20 hover:scale-[1.01] transition-transform flex items-center justify-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                <span>Process & Issue Service Instant</span>
              </button>
            </form>
          )}

          {/* STEP 4: PROCESSING ANIMATION */}
          {step === 'processing' && (
            <div className="py-8 space-y-6 text-center">
              <div className="relative w-20 h-20 mx-auto flex items-center justify-center">
                <div className="absolute inset-0 rounded-full border-4 border-slate-800 animate-ping" />
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 border-2 border-emerald-500 flex items-center justify-center text-emerald-400 animate-spin">
                  <RefreshCw className="w-8 h-8" />
                </div>
              </div>

              <div>
                <h3 className="text-xl font-black text-white">Autonomous Service Processing</h3>
                <p className="text-xs text-slate-400 mt-1">Executing cross-department digital workflow in {countryConfig.country_name}...</p>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-slate-950 rounded-full h-3 border border-slate-800 p-0.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-300"
                  style={{ width: `${processProgress}%` }}
                />
              </div>

              {/* Live Step Log */}
              <div className="space-y-2 text-left bg-slate-950 p-4 rounded-2xl border border-slate-800">
                {executionSteps.map((s, idx) => {
                  const isDone = idx < activeStepIndex;
                  const isCurrent = idx === activeStepIndex;
                  return (
                    <div
                      key={idx}
                      className={`flex items-center gap-3 p-2 rounded-xl text-xs transition-all ${
                        isDone
                          ? 'text-emerald-400 bg-emerald-950/30'
                          : isCurrent
                          ? 'text-white font-bold bg-slate-900 border border-slate-700'
                          : 'text-slate-600'
                      }`}
                    >
                      {isDone ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      ) : isCurrent ? (
                        <RefreshCw className="w-4 h-4 text-emerald-400 animate-spin flex-shrink-0" />
                      ) : (
                        <div className="w-4 h-4 rounded-full border border-slate-700 flex-shrink-0" />
                      )}
                      <div>
                        <div className="font-semibold">{s.title}</div>
                        <div className="text-[10px] text-slate-400 font-mono">{s.detail}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 5: COMPLETED CERTIFICATE */}
          {step === 'completed' && selectedService && (
            <div className="space-y-6 text-center animate-fade-in">
              <div className="w-16 h-16 rounded-full bg-emerald-500/20 border-2 border-emerald-500 flex items-center justify-center text-emerald-400 mx-auto shadow-xl shadow-emerald-500/30">
                <CheckCircle2 className="w-10 h-10" />
              </div>

              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 px-3 py-1 rounded-full border border-emerald-800">
                  Official Sovereign Document Issued
                </span>
                <h3 className="text-2xl font-black text-white mt-2">
                  {selectedService.name} Certificate
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Issued under authority of {countryConfig.country_name} Ministry of Digital Affairs.
                </p>
              </div>

              {/* Official Pass Card */}
              <div className="p-5 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/50 rounded-2xl border-2 border-emerald-500/60 shadow-2xl space-y-4 text-left">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{countryConfig.flag}</span>
                    <div>
                      <div className="font-bold text-xs text-white uppercase">{countryConfig.country_name} Sovereign Deed</div>
                      <div className="text-[10px] text-slate-400 font-mono">ID: {nationalId}</div>
                    </div>
                  </div>
                  <FileCheck className="w-6 h-6 text-emerald-400" />
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-slate-500 text-[10px] uppercase block">Service Type</span>
                    <span className="font-bold text-white">{selectedService.name}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] uppercase block">Region / State</span>
                    <span className="font-bold text-white">{selectedState || 'Federal Central Registry'}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] uppercase block">Verification Hash</span>
                    <span className="font-mono text-[10px] text-emerald-400">0x8f2a...e491</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] uppercase block">Timestamp</span>
                    <span className="font-mono text-[10px] text-slate-300">{new Date().toISOString().slice(0, 10)}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <button
                  id="btn-download-cert"
                  onClick={() => alert("Downloading official cryptographic digital certificate (PDF + W3C VC)...")}
                  className="flex-1 py-3 px-4 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 hover:bg-emerald-400 transition-colors shadow-lg shadow-emerald-500/20"
                >
                  <Download className="w-4 h-4" />
                  <span>Download Official Certificate</span>
                </button>

                <button
                  id="btn-restart-flow"
                  onClick={() => setStep('search')}
                  className="py-3 px-4 rounded-xl bg-slate-800 text-slate-200 hover:text-white font-bold text-xs flex items-center justify-center gap-2 hover:bg-slate-700 transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>Process Another Service</span>
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};
