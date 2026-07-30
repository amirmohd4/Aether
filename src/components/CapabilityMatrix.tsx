import React from 'react';
import { Check, X, Shield, Cpu, Layers } from 'lucide-react';

export const CapabilityMatrix: React.FC = () => {
  const capabilities = [
    { title: "Title verification & Cadastral Audit", aether: true, legacy: false },
    { title: "Cross-department workflow orchestration", aether: true, legacy: false },
    { title: "Complete transaction (write-back ledger)", aether: true, legacy: false },
    { title: "AI-powered fraud detection & risk scoring", aether: true, legacy: false },
    { title: "All government services (Identity, Land, Biz, Tax, Driving)", aether: true, legacy: false },
    { title: "Any country engine (195 UN Nations configurable)", aether: true, legacy: false },
    { title: "Developer marketplace & Open API ecosystem", aether: true, legacy: false },
    { title: "GovStack 2.0 compliant DPI standard", aether: true, legacy: false },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-2">
          <Shield className="w-3.5 h-3.5" />
          <span>Capability Benchmark</span>
        </div>
        <h2 className="text-2xl font-black text-white">
          Aether vs. Legacy Government Systems
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          How Aether's autonomous GovOS compares to traditional fragmented portal architecture.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[500px]">
          <thead>
            <tr className="border-b border-slate-800 text-xs text-slate-400">
              <th className="py-3 px-4 font-bold text-slate-300">Capability</th>
              <th className="py-3 px-4 font-bold text-emerald-400 text-center w-36 bg-emerald-950/30 rounded-t-xl border-x border-t border-emerald-800/40">
                Aether GovOS
              </th>
              <th className="py-3 px-4 font-bold text-slate-500 text-center w-36">
                Legacy Portals
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {capabilities.map((cap, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-medium text-slate-200">
                  {cap.title}
                </td>
                <td className="py-3.5 px-4 text-center bg-emerald-950/20 border-x border-emerald-900/30">
                  <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20">
                    <Check className="w-3.5 h-3.5 stroke-[3]" />
                  </span>
                </td>
                <td className="py-3.5 px-4 text-center">
                  <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-slate-800 text-slate-500">
                    <X className="w-3 h-3 stroke-[2.5]" />
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
