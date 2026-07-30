import React from 'react';
import { ShieldCheck, Globe, Cpu, CheckCircle2, Zap } from 'lucide-react';

export const TrustSignals: React.FC = () => {
  const items = [
    {
      icon: ShieldCheck,
      label: "Trusted by 15+ governments",
      highlight: "15+ Nations"
    },
    {
      icon: Globe,
      label: "195 UN countries ready",
      highlight: "195 Countries"
    },
    {
      icon: Zap,
      label: "99.99% Sovereign Uptime",
      highlight: "99.99% Uptime"
    },
    {
      icon: Cpu,
      label: "GovStack 2.0 Compliant",
      highlight: "GovStack 2.0"
    },
    {
      icon: CheckCircle2,
      label: "AI-Powered Fraud Detection",
      highlight: "AI Fraud Audit"
    }
  ];

  return (
    <div className="w-full bg-slate-900/60 border-y border-slate-800/80 backdrop-blur-md py-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 items-center justify-between text-center">
          {items.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div 
                key={idx} 
                className="flex items-center justify-center gap-2 p-2 rounded-xl bg-slate-950/40 border border-slate-800/50 hover:border-slate-700 transition-all"
              >
                <div className="w-7 h-7 rounded-lg bg-emerald-950/60 border border-emerald-800/60 flex items-center justify-center text-emerald-400 flex-shrink-0">
                  <Icon className="w-3.5 h-3.5" />
                </div>
                <div className="text-left">
                  <div className="text-[11px] font-bold text-slate-200 leading-none">
                    {item.highlight}
                  </div>
                  <div className="text-[10px] text-slate-400 font-medium truncate mt-0.5">
                    {item.label}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
