import React from 'react';
import { CheckCircle2, Download } from 'lucide-react';

interface ResultsViewProps {
  serviceName: string;
  countryName?: string;
  stateName?: string;
  onDone: () => void;
}

export const ResultsView: React.FC<ResultsViewProps> = ({
  serviceName,
  countryName,
  stateName,
  onDone
}) => {
  const referenceNumber = `REF-${Math.floor(100000 + Math.random() * 900000)}`;

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xl text-center space-y-6">
      <div className="w-16 h-16 mx-auto rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
        <CheckCircle2 className="w-10 h-10" />
      </div>

      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-900">
          Request Completed
        </h2>
        <p className="text-sm text-slate-600">
          Your request for <strong>{serviceName}</strong> has been successfully processed and approved.
        </p>
      </div>

      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-left space-y-2 text-xs text-slate-700">
        <div className="flex justify-between py-1 border-b border-slate-200">
          <span className="font-semibold text-slate-500">Service:</span>
          <span className="font-bold text-slate-900">{serviceName}</span>
        </div>
        {countryName && (
          <div className="flex justify-between py-1 border-b border-slate-200">
            <span className="font-semibold text-slate-500">Country:</span>
            <span className="font-medium text-slate-900">{countryName}</span>
          </div>
        )}
        {stateName && (
          <div className="flex justify-between py-1 border-b border-slate-200">
            <span className="font-semibold text-slate-500">State/Region:</span>
            <span className="font-medium text-slate-900">{stateName}</span>
          </div>
        )}
        <div className="flex justify-between py-1">
          <span className="font-semibold text-slate-500">Reference Number:</span>
          <span className="font-mono font-bold text-[#1a365d]">{referenceNumber}</span>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <button
          type="button"
          onClick={() => alert(`Document ${referenceNumber} downloaded.`)}
          className="flex-1 py-3 px-4 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-sm flex items-center justify-center gap-2 transition-all cursor-pointer"
        >
          <Download className="w-4 h-4 text-[#1a365d]" />
          <span>Download Document</span>
        </button>

        <button
          id="btn-done"
          type="button"
          onClick={onDone}
          className="flex-1 py-3 px-6 rounded-xl bg-[#1a365d] hover:bg-[#122847] text-white font-bold text-sm shadow-md transition-all cursor-pointer"
        >
          Done
        </button>
      </div>
    </div>
  );
};
