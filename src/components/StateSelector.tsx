import React from 'react';
import { getCountryStates } from '../configs/countriesData';

interface StateSelectorProps {
  countryCode: string;
  selectedState: string;
  onSelectState: (state: string) => void;
  onContinue: () => void;
  onBack?: () => void;
}

export const StateSelector: React.FC<StateSelectorProps> = ({
  countryCode,
  selectedState,
  onSelectState,
  onContinue,
  onBack
}) => {
  const states = getCountryStates(countryCode) || [];

  if (states.length === 0) return null;

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-xl space-y-4 text-left">
      <div className="space-y-1">
        <label className="block text-sm font-bold text-slate-900">
          Select your state/region
        </label>
        <p className="text-xs text-slate-500">
          Select your administrative state or province
        </p>
      </div>

      <select
        id="select-state-dropdown"
        value={selectedState}
        onChange={(e) => onSelectState(e.target.value)}
        className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-sm font-medium text-slate-900 focus:outline-none focus:border-[#1a365d] focus:ring-2 focus:ring-[#1a365d]/20 transition-all cursor-pointer"
      >
        <option value="">Select your state/region</option>
        {states.map((st) => (
          <option key={st} value={st}>
            {st}
          </option>
        ))}
      </select>

      <div className="flex gap-3 pt-2">
        {onBack && (
          <button
            type="button"
            onClick={onBack}
            className="px-4 py-3 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold text-sm transition-all cursor-pointer"
          >
            Back
          </button>
        )}
        <button
          id="btn-state-continue"
          type="button"
          disabled={!selectedState}
          onClick={onContinue}
          className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] disabled:opacity-50 text-white font-bold text-sm shadow-md transition-all cursor-pointer"
        >
          Continue
        </button>
      </div>
    </div>
  );
};
