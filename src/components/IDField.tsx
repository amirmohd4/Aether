import React, { useState } from 'react';

interface IDFieldProps {
  onSubmitID: (demoReference: string) => void;
  onBack?: () => void;
}

export const IDField: React.FC<IDFieldProps> = ({ onSubmitID, onBack }) => {
  const [demoReference, setDemoReference] = useState('DEMO-CASE-001');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmitID(demoReference.trim() || 'DEMO-CASE-001');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-xl space-y-4 text-left">
      <div className="space-y-1">
        <label htmlFor="input-demo-reference" className="block text-sm font-bold text-slate-900">
          Fictional demo reference (optional)
        </label>
        <p className="text-xs leading-5 text-amber-800">
          Synthetic preview only. Never enter a national ID, passport number, Aadhaar/PAN, bank details, or any real personal identifier.
        </p>
      </div>
      <input
        id="input-demo-reference"
        type="text"
        maxLength={80}
        value={demoReference}
        onChange={(e) => setDemoReference(e.target.value)}
        placeholder="DEMO-CASE-001"
        autoFocus
        className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#1a365d] focus:ring-2 focus:ring-[#1a365d]/20 transition-all font-mono"
      />
      <div className="flex gap-3 pt-2">
        {onBack && <button type="button" onClick={onBack} className="px-4 py-3 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold text-sm transition-all cursor-pointer">Back</button>}
        <button id="btn-submit-demo-reference" type="submit" className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] text-white font-bold text-sm shadow-md transition-all cursor-pointer">
          Run synthetic preview
        </button>
      </div>
    </form>
  );
};
