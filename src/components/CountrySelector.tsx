import React from 'react';
import { ALL_UN_COUNTRIES } from '../configs/countriesData';

interface CountrySelectorProps {
  selectedCountryCode: string;
  onSelectCountry: (countryCode: string) => void;
  onContinue?: () => void;
  onBack?: () => void;
}

export const CountrySelector: React.FC<CountrySelectorProps> = ({
  selectedCountryCode,
  onSelectCountry,
  onContinue,
  onBack
}) => {
  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-xl space-y-4 text-left">
      <div className="space-y-1">
        <label className="block text-sm font-bold text-slate-900">
          Select your country
        </label>
        <p className="text-xs text-slate-500">
          Choose your country to view available government services
        </p>
      </div>

      <select
        id="select-country-dropdown"
        value={selectedCountryCode}
        onChange={(e) => onSelectCountry(e.target.value)}
        className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-sm font-medium text-slate-900 focus:outline-none focus:border-[#1a365d] focus:ring-2 focus:ring-[#1a365d]/20 transition-all cursor-pointer"
      >
        <option value="">Select your country</option>
        {ALL_UN_COUNTRIES.map((c) => (
          <option key={c.code} value={c.code}>
            {c.flag} {c.name}
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
        {onContinue && (
          <button
            id="btn-country-continue"
            type="button"
            disabled={!selectedCountryCode}
            onClick={onContinue}
            className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] disabled:opacity-50 text-white font-bold text-sm shadow-md transition-all cursor-pointer"
          >
            Continue
          </button>
        )}
      </div>
    </div>
  );
};
