import React, { useState } from 'react';
import { Clock, Zap, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';

interface ExampleItem {
  service: string;
  before: string;
  after: string;
  speedup: string;
}

interface CountryExample {
  code: string;
  country: string;
  flag: string;
  tagline: string;
  items: ExampleItem[];
}

export const REAL_EXAMPLES: CountryExample[] = [
  {
    code: 'IN',
    country: 'India',
    flag: '🇮🇳',
    tagline: 'Aadhaar & Digital India DPI Integration',
    items: [
      {
        service: 'Property Registration',
        before: 'In months (60–90 days)',
        after: 'In days (2–3 days)',
        speedup: '30x Faster'
      },
      {
        service: 'Birth Certificate',
        before: 'In weeks (14–21 days)',
        after: 'In minutes (< 3 mins)',
        speedup: 'Instant'
      },
      {
        service: 'Driving License',
        before: 'In months (30–60 days)',
        after: 'In minutes (< 2 mins)',
        speedup: 'Instant'
      }
    ]
  },
  {
    code: 'US',
    country: 'USA',
    flag: '🇺🇸',
    tagline: 'Login.gov & Municipal County Land Registry',
    items: [
      {
        service: 'Property Title Search',
        before: 'In days (5–7 days)',
        after: 'In seconds (< 10 secs)',
        speedup: 'Real-time'
      },
      {
        service: 'Building Permit',
        before: 'In months (3–6 months)',
        after: 'In days (3–5 days)',
        speedup: '20x Faster'
      }
    ]
  },
  {
    code: 'AE',
    country: 'UAE',
    flag: '🇦🇪',
    tagline: 'UAE Pass & Dubai Land Department (DLD)',
    items: [
      {
        service: 'Property Registration',
        before: 'In days (5–7 days)',
        after: 'In minutes (< 5 mins)',
        speedup: 'Instant'
      },
      {
        service: 'RERA Registration',
        before: 'In weeks (2–3 weeks)',
        after: 'In days (1–2 days)',
        speedup: '15x Faster'
      }
    ]
  }
];

export const RealExamples: React.FC = () => {
  const genericRows = [
    { service: 'Property Registration', before: 'In months', after: 'In days', speedup: '30x Faster' },
    { service: 'Birth Certificate', before: 'In weeks', after: 'In minutes', speedup: 'Instant' },
    { service: 'Driving License', before: 'In months', after: 'In minutes', speedup: 'Instant' },
    { service: 'Building Permit', before: 'In months', after: 'In days', speedup: '20x Faster' },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Real Velocity Impact</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Real Examples & Turnaround Times
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Comparing traditional manual processing vs. Aether's automated sovereign workflow.
        </p>
      </div>

      {/* Comparison Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[500px]">
          <thead>
            <tr className="border-b border-slate-800 text-xs text-slate-400">
              <th className="py-3.5 px-4 font-bold text-slate-300">Service</th>
              <th className="py-3.5 px-4 font-bold text-rose-400">Without Aether</th>
              <th className="py-3.5 px-4 font-bold text-emerald-400 bg-emerald-950/30 rounded-t-xl border-x border-t border-emerald-800/40">
                With Aether
              </th>
              <th className="py-3.5 px-4 font-bold text-slate-400 text-right">Improvement</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {genericRows.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-4 px-4 font-bold text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400" />
                  <span>{row.service}</span>
                </td>
                <td className="py-4 px-4 font-semibold text-rose-300">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-rose-950/40 border border-rose-900/40">
                    <Clock className="w-3 h-3 text-rose-400" />
                    <span>{row.before}</span>
                  </span>
                </td>
                <td className="py-4 px-4 font-bold text-emerald-300 bg-emerald-950/20 border-x border-emerald-900/30">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-900/40 border border-emerald-700/50">
                    <Zap className="w-3 h-3 text-emerald-400 fill-current" />
                    <span>{row.after}</span>
                  </span>
                </td>
                <td className="py-4 px-4 text-right">
                  <span className="font-mono text-[11px] font-bold px-2.5 py-1 rounded-lg bg-slate-950 text-emerald-400 border border-slate-800">
                    {row.speedup}
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
