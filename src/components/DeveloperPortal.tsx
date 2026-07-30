import React, { useState } from 'react';
import { 
  Code, Key, Shield, Terminal, Zap, CheckCircle2, Copy, Play, 
  ExternalLink, BarChart3, Lock, Server, FileCode, Layers, DollarSign
} from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';

export const DeveloperPortal: React.FC = () => {
  const { t } = useTranslation();
  const [orgName, setOrgName] = useState('Standard Chartered Bank / Conveyance AI');
  const [selectedTier, setSelectedTier] = useState('pro');
  const [generatedKey, setGeneratedKey] = useState<string | null>('aeth_live_bank_demo_key_9988');
  const [copiedKey, setCopiedKey] = useState(false);

  // Interactive API Sandbox state
  const [sandboxEndpoint, setSandboxEndpoint] = useState('/api/v1/property/verify-title');
  const [sandboxCountry, setSandboxCountry] = useState('IN');
  const [sandboxParcel, setSandboxParcel] = useState('DELHI-REG-9872-B');
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [isLoadingApi, setIsLoadingApi] = useState(false);

  const handleGenerateKey = (e: React.FormEvent) => {
    e.preventDefault();
    const newKey = `aeth_live_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
    setGeneratedKey(newKey);
  };

  const copyKeyToClipboard = () => {
    if (generatedKey) {
      navigator.clipboard.writeText(generatedKey);
      setCopiedKey(true);
      setTimeout(() => setCopiedKey(false), 2000);
    }
  };

  const runApiTest = () => {
    setIsLoadingApi(true);
    setTimeout(() => {
      setIsLoadingApi(false);
      setApiResponse({
        status: "200 OK",
        execution_time_ms: 142,
        sovereign_node: `${sandboxCountry}-NODE-01`,
        payload: {
          parcel_id: sandboxParcel,
          country_code: sandboxCountry,
          title_holder: "Sovereign Verified Trustee",
          encumbrance_status: "CLEARED_NO_LIEN",
          fraud_risk_score: 0.02,
          stamp_duty_compliance: "FULLY_PAID",
          ledger_tx_hash: "0x8f9c12004e1a04b"
        }
      });
    }, 500);
  };

  return (
    <div id="section-developer-portal" className="space-y-8">
      {/* Hero Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/40 text-blue-300 text-xs font-semibold mb-3">
              <Terminal className="w-3.5 h-3.5 text-blue-400" />
              <span>Private Sector & Financial Infrastructure</span>
            </div>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              {t('dev_portal_title', 'Aether Developer Portal')}
            </h1>
            <p className="text-slate-400 text-sm mt-2 max-w-2xl leading-relaxed">
              {t('dev_portal_subtitle', 'Institutional grade APIs for Banks, Insurers, Developers, and Conveyancers.')}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-slate-950/80 rounded-2xl border border-slate-800 text-xs text-slate-300">
              Rate Limit: <span className="text-emerald-400 font-bold font-mono">50,000 req/mo</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Key Provisioning Panel */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
              <Key className="w-4 h-4 text-blue-400" />
              <span>Generate API Credentials</span>
            </h2>
          </div>

          <form onSubmit={handleGenerateKey} className="space-y-4">
            <div className="space-y-1">
              <label id="lbl-org-name" className="text-xs font-medium text-slate-300">Organization Name / Entity:</label>
              <input
                id="input-org-name"
                type="text"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                required
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="space-y-1">
              <label id="lbl-select-tier" className="text-xs font-medium text-slate-300">Pricing Tier:</label>
              <select
                id="select-api-tier"
                value={selectedTier}
                onChange={(e) => setSelectedTier(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="free">Free Sandbox (100 req/mo - $0)</option>
                <option value="starter">Starter (10,000 req/mo - $99/mo)</option>
                <option value="pro">Pro Tier (50,000 req/mo - $499/mo)</option>
                <option value="enterprise">Sovereign Enterprise (Custom)</option>
              </select>
            </div>

            <button
              id="btn-generate-api-key"
              type="submit"
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl transition-all shadow-lg shadow-blue-600/20"
            >
              Issue Production Key
            </button>
          </form>

          {generatedKey && (
            <div className="bg-slate-950 border border-blue-500/40 rounded-2xl p-4 space-y-2">
              <div className="text-[10px] font-bold uppercase tracking-wider text-blue-400">Your Active API Key:</div>
              <div className="flex items-center justify-between bg-slate-900 px-3 py-2 rounded-xl border border-slate-800">
                <code className="text-xs font-mono text-emerald-400 truncate">{generatedKey}</code>
                <button
                  id="btn-copy-api-key"
                  onClick={copyKeyToClipboard}
                  className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                >
                  {copiedKey ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
              <p className="text-[11px] text-slate-500">
                Include as <code className="text-slate-300 font-mono">X-Aether-Api-Key</code> in HTTP Request Headers.
              </p>
            </div>
          )}
        </div>

        {/* Interactive API Sandbox */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
              <Code className="w-4 h-4 text-blue-400" />
              <span>Interactive API Playground</span>
            </h2>
            <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800">
              SANDBOX LIVE
            </span>
          </div>

          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label id="lbl-api-endpoint" className="text-[11px] text-slate-400 block mb-1">Endpoint API Route:</label>
                <select
                  id="select-sandbox-endpoint"
                  value={sandboxEndpoint}
                  onChange={(e) => setSandboxEndpoint(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs font-mono text-slate-200"
                >
                  <option value="/api/v1/property/verify-title">Verify Title & Lien</option>
                  <option value="/api/v1/fraud/risk-score">AI Fraud Risk Score</option>
                  <option value="/api/v1/valuation/market-price">Automated Valuation Model</option>
                </select>
              </div>

              <div>
                <label id="lbl-sandbox-country" className="text-[11px] text-slate-400 block mb-1">Country Node:</label>
                <select
                  id="select-sandbox-country"
                  value={sandboxCountry}
                  onChange={(e) => setSandboxCountry(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs font-mono text-slate-200"
                >
                  <option value="IN">IN (India)</option>
                  <option value="KE">KE (Kenya)</option>
                  <option value="AE">AE (UAE)</option>
                  <option value="EE">EE (Estonia)</option>
                  <option value="US">US (USA)</option>
                </select>
              </div>

              <div>
                <label id="lbl-parcel-param" className="text-[11px] text-slate-400 block mb-1">Parcel Code:</label>
                <input
                  id="input-sandbox-parcel"
                  type="text"
                  value={sandboxParcel}
                  onChange={(e) => setSandboxParcel(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs font-mono text-slate-200"
                />
              </div>
            </div>

            <button
              id="btn-execute-sandbox-call"
              onClick={runApiTest}
              className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Execute Sandbox Request</span>
            </button>

            {/* JSON Output Viewer */}
            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 space-y-2">
              <div className="text-[10px] font-mono text-slate-500 uppercase flex items-center justify-between">
                <span>Response Payload (JSON)</span>
                {apiResponse && <span className="text-emerald-400 font-bold">{apiResponse.status}</span>}
              </div>
              <pre className="text-xs font-mono text-emerald-300 overflow-x-auto p-2 bg-slate-900 rounded-xl max-h-56">
                {isLoadingApi
                  ? "Sending request to Aether Node..."
                  : apiResponse
                  ? JSON.stringify(apiResponse, null, 2)
                  : "// Response will appear here after execution..."}
              </pre>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
