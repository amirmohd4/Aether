import React, { useState, useEffect } from 'react';
import { 
  Play, RotateCcw, Share2, Check, Shield, ShieldCheck, Zap, Award, 
  Clock, ArrowRight, Sparkles, AlertCircle, FileText, CheckCircle2,
  Copy, ExternalLink, RefreshCw, Layers, Lock, Cpu
} from 'lucide-react';
import { COUNTRIES_CONFIG, Service, CountryConfig, getCountryConfig } from '../configs/countriesData';
import { CountrySelector } from './CountrySelector';
import { useTranslation } from '../hooks/useTranslation';

interface GlobalDemoProps {
  initialCountryCode?: string;
  initialServiceId?: string;
}

export const GlobalDemo: React.FC<GlobalDemoProps> = ({
  initialCountryCode = 'IN',
  initialServiceId
}) => {
  const { t } = useTranslation();
  
  // State from URL query or defaults
  const [selectedCountryCode, setSelectedCountryCode] = useState<string>(() => {
    const params = new URLSearchParams(window.location.search);
    return params.get('country') || initialCountryCode;
  });

  const country = getCountryConfig(selectedCountryCode);

  const [selectedServiceId, setSelectedServiceId] = useState<string>(() => {
    const params = new URLSearchParams(window.location.search);
    const paramSrv = params.get('service');
    if (paramSrv && country.services.some(s => s.id === paramSrv)) {
      return paramSrv;
    }
    return initialServiceId || country.services[0]?.id || 'srv_prop_reg';
  });

  const currentService = country.services.find(s => s.id === selectedServiceId) || country.services[0];

  // User input simulation state
  const [nationalId, setNationalId] = useState<string>('9988-7766-5544');
  const [propertyParcelId, setPropertyParcelId] = useState<string>('PARCEL-2026-AE99');
  
  // Execution State
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentStepIdx, setCurrentStepIdx] = useState<number>(-1);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [executionTimeMs, setExecutionTimeMs] = useState<number>(0);
  const [isCompleted, setIsCompleted] = useState<boolean>(false);
  const [copiedLink, setCopiedLink] = useState<boolean>(false);
  const [showCertificateModal, setShowCertificateModal] = useState<boolean>(false);

  // Sync service when country changes
  useEffect(() => {
    const newCountry = getCountryConfig(selectedCountryCode);
    if (!newCountry.services.some(s => s.id === selectedServiceId)) {
      setSelectedServiceId(newCountry.services[0]?.id || '');
    }
  }, [selectedCountryCode]);

  // Handle Workflow Runner
  const runGovernanceWorkflow = () => {
    if (isRunning) return;
    setIsRunning(true);
    setIsCompleted(false);
    setCurrentStepIdx(0);
    setCompletedSteps([]);
    setExecutionTimeMs(0);

    const steps = currentService.workflow_steps;
    let step = 0;
    const startTime = Date.now();

    const interval = setInterval(() => {
      setCompletedSteps(prev => [...prev, step]);
      step += 1;
      
      if (step < steps.length) {
        setCurrentStepIdx(step);
      } else {
        clearInterval(interval);
        setCurrentStepIdx(steps.length - 1);
        setIsRunning(false);
        setIsCompleted(true);
        setExecutionTimeMs(Date.now() - startTime);
      }
    }, 450); // Fast 450ms per step for instant gratification
  };

  const resetDemo = () => {
    setIsRunning(false);
    setIsCompleted(false);
    setCurrentStepIdx(-1);
    setCompletedSteps([]);
    setExecutionTimeMs(0);
  };

  const shareDemoLink = () => {
    const url = new URL(window.location.href);
    url.searchParams.set('country', selectedCountryCode);
    url.searchParams.set('service', selectedServiceId);
    navigator.clipboard.writeText(url.toString());
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 3000);
  };

  return (
    <div id="section-global-demo" className="space-y-6">
      {/* Banner / Header */}
      <div className="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 border border-emerald-800/60 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
              <span>The "ChatGPT Moment" for Digital Governance</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              Aether Universal Sovereign Demo
            </h1>
            <p className="text-slate-300 text-sm mt-2 max-w-2xl leading-relaxed">
              Experience instant, zero-paperwork, zero-fraud government service execution for any nation. Try real-time title checking, encumbrance auditing, and e-deed issuance below.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              id="btn-share-demo-link"
              onClick={shareDemoLink}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition-all shadow-md"
            >
              {copiedLink ? <Check className="w-4 h-4 text-emerald-400" /> : <Share2 className="w-4 h-4 text-emerald-400" />}
              <span>{copiedLink ? t('link_copied', 'Link Copied!') : t('btn_share', 'Share This Demo')}</span>
            </button>
            <button
              id="btn-reset-demo"
              onClick={resetDemo}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 text-xs font-semibold transition-all"
            >
              <RotateCcw className="w-4 h-4" />
              <span>{t('btn_reset', 'Reset')}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Interactive Demo Box */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Control Panel */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-400" />
              <span>{t('step_country', '1. Country & Service Setup')}</span>
            </h2>
          </div>

          {/* Country Selection */}
          <div className="space-y-2">
            <label id="lbl-target-country" className="text-xs font-semibold text-slate-300 block">
              Target Sovereign Nation:
            </label>
            <CountrySelector
              selectedCountryCode={selectedCountryCode}
              onSelectCountry={setSelectedCountryCode}
              variant="card"
            />
          </div>

          {/* Service Selector */}
          <div className="space-y-2 pt-2">
            <label id="lbl-select-service" className="text-xs font-semibold text-slate-300 block">
              Select Sovereign Government Service:
            </label>
            <div className="space-y-2">
              {country.services.map((srv) => {
                const isSelected = srv.id === selectedServiceId;
                return (
                  <button
                    key={srv.id}
                    id={`btn-select-service-option-${srv.id}`}
                    onClick={() => {
                      setSelectedServiceId(srv.id);
                      resetDemo();
                    }}
                    className={`w-full text-left p-3.5 rounded-2xl border transition-all ${
                      isSelected
                        ? 'bg-slate-800 border-emerald-500 text-white shadow-lg ring-1 ring-emerald-500/40'
                        : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800/80 hover:text-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-xs text-white">{srv.name}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-950 text-emerald-400 font-mono">
                        {srv.processing_time}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1 line-clamp-1">{srv.description}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Input Parameters Form */}
          <div className="space-y-3 pt-2 bg-slate-950/80 p-4 rounded-2xl border border-slate-800">
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
              <span>Required Identity & Asset Data</span>
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
            </div>

            <div className="space-y-1">
              <label id="lbl-citizen-id" className="text-[11px] text-slate-400">
                {country.id_system.name} ID:
              </label>
              <input
                id="input-citizen-id"
                type="text"
                value={nationalId}
                onChange={(e) => setNationalId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs font-mono text-emerald-300 focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div className="space-y-1">
              <label id="lbl-property-id" className="text-[11px] text-slate-400">
                Property / Asset Cadastral Code:
              </label>
              <input
                id="input-property-id"
                type="text"
                value={propertyParcelId}
                onChange={(e) => setPropertyParcelId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs font-mono text-emerald-300 focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          {/* Trigger Workflow CTA */}
          <button
            id="btn-run-governance-workflow"
            onClick={runGovernanceWorkflow}
            disabled={isRunning}
            className={`w-full py-4 rounded-2xl font-bold text-sm flex items-center justify-center gap-2.5 transition-all shadow-xl ${
              isRunning
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                : 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-emerald-500/25 active:scale-[0.98]'
            }`}
          >
            {isRunning ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin text-emerald-400" />
                <span>Executing Sovereign Engine...</span>
              </>
            ) : (
              <>
                <Play className="w-5 h-5 fill-current" />
                <span>{t('btn_run_demo', 'Run Governance Workflow')}</span>
              </>
            )}
          </button>
        </div>

        {/* Right Execution Engine Screen */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl flex flex-col justify-between space-y-6">
          
          <div>
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-sm font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-emerald-400" />
                  <span>Sovereign Ledger Execution Pipeline</span>
                </h2>
                <div className="text-xs text-slate-400 mt-0.5">
                  Engine: <span className="text-slate-200 font-semibold">{country.country_name} Aether Node v2.0</span>
                </div>
              </div>

              {isCompleted && (
                <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/50 text-emerald-400 text-xs font-mono font-bold">
                  <Clock className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Executed in {(executionTimeMs / 1000).toFixed(2)}s</span>
                </div>
              )}
            </div>

            {/* Workflow Steps Tracker */}
            <div className="mt-6 space-y-3">
              {currentService.workflow_steps.map((step, idx) => {
                const isDone = completedSteps.includes(idx);
                const isCurrent = currentStepIdx === idx && isRunning;
                const isPending = !isDone && !isCurrent;

                return (
                  <div
                    key={step.id}
                    id={`step-indicator-${step.id}`}
                    className={`p-4 rounded-2xl border transition-all duration-300 flex items-center justify-between ${
                      isDone
                        ? 'bg-slate-950/90 border-emerald-500/60 text-white'
                        : isCurrent
                        ? 'bg-slate-800 border-emerald-400 text-emerald-300 shadow-lg shadow-emerald-950/50 ring-1 ring-emerald-400'
                        : 'bg-slate-950/40 border-slate-800/80 text-slate-500'
                    }`}
                  >
                    <div className="flex items-center gap-3.5">
                      <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-mono text-xs font-bold transition-all ${
                        isDone
                          ? 'bg-emerald-500 text-slate-950'
                          : isCurrent
                          ? 'bg-emerald-950 border border-emerald-400 text-emerald-400 animate-pulse'
                          : 'bg-slate-800 text-slate-500'
                      }`}>
                        {isDone ? <Check className="w-4 h-4 stroke-[3]" /> : idx + 1}
                      </div>

                      <div>
                        <div className={`text-xs font-bold ${isDone ? 'text-emerald-300' : isCurrent ? 'text-white' : 'text-slate-400'}`}>
                          {step.name}
                        </div>
                        <div className="text-[10px] text-slate-500 font-mono mt-0.5">
                          {isDone ? 'Cryptographically Sealed & Verified' : isCurrent ? 'Verifying with Sovereign Databases...' : 'Queued in Ledger Pipeline'}
                        </div>
                      </div>
                    </div>

                    <div className="text-right">
                      {isDone && (
                        <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/50">
                          PASSED
                        </span>
                      )}
                      {isCurrent && (
                        <span className="text-[10px] font-mono text-amber-400 animate-pulse bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/50">
                          CHECKING...
                        </span>
                      )}
                      {isPending && (
                        <span className="text-[10px] font-mono text-slate-600">
                          WAITING
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Final Certificate Card Output */}
          {isCompleted ? (
            <div className="bg-gradient-to-br from-emerald-950/90 via-slate-950 to-slate-900 border border-emerald-500/60 rounded-2xl p-5 shadow-2xl space-y-4 animate-in fade-in slide-in-from-bottom-3 duration-500">
              <div className="flex items-center justify-between border-b border-emerald-800/60 pb-3">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
                    Official Sovereign Document Generated
                  </span>
                </div>
                <span className="text-xl">{country.flag}</span>
              </div>

              <div className="space-y-1">
                <h4 className="text-base font-bold text-white">
                  {country.country_name} e-Deed Certificate #{Math.floor(100000 + Math.random() * 900000)}
                </h4>
                <p className="text-xs text-slate-300">
                  Issued to Identity <span className="font-mono text-emerald-400">{nationalId}</span> for Asset <span className="font-mono text-amber-300">{propertyParcelId}</span>
                </p>
              </div>

              <div className="flex items-center justify-between pt-2">
                <span className="text-[10px] font-mono text-slate-400">
                  Sealed by Aether GovStack Mediator
                </span>
                <button
                  id="btn-view-official-certificate"
                  onClick={() => setShowCertificateModal(true)}
                  className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold rounded-xl transition-all shadow-md shadow-emerald-500/20 flex items-center gap-1.5"
                >
                  <FileText className="w-4 h-4" />
                  <span>View Sovereign Certificate</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-6 text-center text-slate-500 text-xs">
              Click <span className="text-emerald-400 font-semibold">"Run Governance Workflow"</span> to trigger real-time AI fraud check and instant title generation.
            </div>
          )}
        </div>
      </div>

      {/* Official Certificate Modal */}
      {showCertificateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
          <div className="bg-slate-900 border border-emerald-500/60 rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl space-y-6 text-slate-200 relative overflow-hidden">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{country.flag}</span>
                <div>
                  <div className="text-xs font-bold text-emerald-400 uppercase tracking-widest">
                    Government of {country.country_name}
                  </div>
                  <h3 className="text-lg font-extrabold text-white">Official Certificate of Digital Title</h3>
                </div>
              </div>
              <button
                id="btn-close-certificate-modal"
                onClick={() => setShowCertificateModal(false)}
                className="text-slate-400 hover:text-white text-sm font-bold px-2 py-1 bg-slate-800 rounded-lg"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4 bg-slate-950 p-5 rounded-2xl border border-slate-800 font-mono text-xs">
              <div className="flex justify-between border-b border-slate-800 pb-2">
                <span className="text-slate-500">Certificate ID:</span>
                <span className="text-emerald-400 font-bold">SOV-2026-{selectedCountryCode}-9982</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-2">
                <span className="text-slate-500">Citizen ID ({country.id_system.name}):</span>
                <span className="text-slate-200">{nationalId}</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-2">
                <span className="text-slate-500">Cadastral Parcel:</span>
                <span className="text-slate-200">{propertyParcelId}</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-2">
                <span className="text-slate-500">Registry Stamp Duty Paid:</span>
                <span className="text-amber-400">{country.currency.symbol} {currentService.fees.base_fee}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Encumbrance / Lien Status:</span>
                <span className="text-emerald-400 font-bold">CLEAR & FREE OF ENCUMBRANCE</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="text-[10px] text-slate-500">
                Validated via GovStack 2.0 Information Mediator
              </div>
              <button
                id="btn-print-certificate"
                onClick={() => window.print()}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold rounded-xl border border-slate-700 flex items-center gap-2"
              >
                <FileText className="w-4 h-4" />
                <span>Print Certificate</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
