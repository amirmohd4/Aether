import React, { useState } from 'react';
import { CheckCircle2, Copy } from 'lucide-react';

interface ResultsViewProps {
  serviceName: string;
  countryName?: string;
  stateName?: string;
  onDone: () => void;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ serviceName, countryName, stateName, onDone }) => {
  const [referenceNumber] = useState(() => `SIM-${Math.random().toString(36).slice(2, 9).toUpperCase()}`);
  const [copyMessage, setCopyMessage] = useState('');
  const summary = [
    'Aether GovOS — synthetic journey preview',
    'Service: ' + serviceName,
    'Jurisdiction label: ' + [countryName, stateName].filter(Boolean).join(' / '),
    'Synthetic reference: ' + referenceNumber,
    'No official application was submitted. No government system was contacted. No approval or certificate was issued.',
  ].join('\n');

  async function copySummary() {
    try {
      await navigator.clipboard.writeText(summary);
      setCopyMessage('Synthetic summary copied.');
    } catch {
      setCopyMessage('Copy is unavailable in this browser. You can note the synthetic reference shown above.');
    }
  }

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xl text-center space-y-6">
      <div className="w-16 h-16 mx-auto rounded-full bg-cyan-100 text-cyan-800 flex items-center justify-center">
        <CheckCircle2 className="w-10 h-10" />
      </div>
      <div className="space-y-2">
        <p className="inline-flex rounded-full border border-amber-300 bg-amber-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-amber-900">Synthetic only · Not official</p>
        <h2 className="text-2xl font-bold text-slate-900">Mock journey preview generated</h2>
        <p className="text-sm text-slate-600">
          This is a simulated result for <strong>{serviceName}</strong>. It is not an approval, application receipt, legal decision, or government record.
        </p>
      </div>
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-left space-y-2 text-xs text-slate-700">
        <div className="flex justify-between gap-4 py-1 border-b border-slate-200"><span className="font-semibold text-slate-500">Service template:</span><span className="font-bold text-right text-slate-900">{serviceName}</span></div>
        {countryName && <div className="flex justify-between gap-4 py-1 border-b border-slate-200"><span className="font-semibold text-slate-500">Jurisdiction label:</span><span className="font-medium text-right text-slate-900">{countryName}</span></div>}
        {stateName && <div className="flex justify-between gap-4 py-1 border-b border-slate-200"><span className="font-semibold text-slate-500">Region label:</span><span className="font-medium text-right text-slate-900">{stateName}</span></div>}
        <div className="flex justify-between gap-4 py-1"><span className="font-semibold text-slate-500">Synthetic reference:</span><span className="font-mono font-bold text-[#1a365d]">{referenceNumber}</span></div>
      </div>
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-left text-xs leading-5 text-amber-950">
        No official service was contacted. No real application was created. Real requirements, processing times, legal decisions, and service availability depend on authorised systems and the responsible jurisdiction.
      </div>
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <button type="button" onClick={copySummary} className="flex-1 py-3 px-4 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-sm flex items-center justify-center gap-2 transition-all cursor-pointer"><Copy className="w-4 h-4" /><span>Copy demo summary</span></button>
        <button id="btn-done" type="button" onClick={onDone} className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] text-white font-bold text-sm shadow-md transition-all cursor-pointer">Done</button>
      </div>
      {copyMessage && <p role="status" className="text-xs text-slate-600">{copyMessage}</p>}
    </div>
  );
};
