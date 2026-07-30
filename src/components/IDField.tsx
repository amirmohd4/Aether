import React, { useState } from 'react';

interface IDFieldProps {
  onSubmitID: (idValue: string) => void;
  onBack?: () => void;
}

export const IDField: React.FC<IDFieldProps> = ({
  onSubmitID,
  onBack
}) => {
  const [idValue, setIdValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!idValue.trim()) return;
    onSubmitID(idValue);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-xl space-y-4 text-left"
    >
      <div className="space-y-1">
        <label className="block text-sm font-bold text-slate-900">
          Enter your National ID / Digital ID
        </label>
        <p className="text-xs text-slate-500">
          Your identification is securely encrypted to verify identity
        </p>
      </div>

      <input
        id="input-national-id"
        type="text"
        required
        value={idValue}
        onChange={(e) => setIdValue(e.target.value)}
        placeholder="Enter your National ID / Digital ID"
        autoFocus
        className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#1a365d] focus:ring-2 focus:ring-[#1a365d]/20 transition-all font-mono"
      />

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
          id="btn-submit-national-id"
          type="submit"
          disabled={!idValue.trim()}
          className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] disabled:opacity-50 text-white font-bold text-sm shadow-md transition-all cursor-pointer"
        >
          Submit
        </button>
      </div>
    </form>
  );
};
