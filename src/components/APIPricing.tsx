import React, { useState } from 'react';
import { Check, Shield, Zap, Sparkles, Server, DollarSign, ArrowRight } from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';

export const APIPricing: React.FC = () => {
  const { t } = useTranslation();
  const [requestVolume, setRequestVolume] = useState<number>(25000);

  const tiers = [
    {
      id: 'free',
      name: t('pricing_free_tier', 'Free Sandbox'),
      price: '$0',
      period: 'forever',
      requests: '100 requests / mo',
      desc: 'Ideal for developers testing integrations, proof of concepts, and sandboxes.',
      features: ['Access to Sandbox Nodes', 'Community Support', 'Standard Rate Limit', '1 Key'],
      highlight: false,
      btnText: 'Start Free'
    },
    {
      id: 'starter',
      name: t('pricing_starter', 'Starter Tier'),
      price: '$99',
      period: 'per month',
      requests: '10,000 requests / mo',
      desc: 'For local conveyancers, fintech startups, and proptech applications.',
      features: ['Production Node SLA', 'Email Support', '100 req/min Rate Limit', 'Up to 5 Keys', 'Encumbrance API'],
      highlight: false,
      btnText: 'Choose Starter'
    },
    {
      id: 'pro',
      name: t('pricing_pro', 'Pro Tier'),
      price: '$499',
      period: 'per month',
      requests: '50,000 requests / mo',
      desc: 'Institutional grade for Commercial Banks, Mortgage Lenders, and Insurers.',
      features: ['99.99% Uptime Guarantee', 'Dedicated Slack Channel', '1,000 req/min Rate Limit', 'Unlimited Keys', 'AI Fraud Risk Scoring', 'Automated Valuation API'],
      highlight: true,
      btnText: 'Subscribe Pro'
    },
    {
      id: 'enterprise',
      name: t('pricing_enterprise', 'Sovereign Enterprise'),
      price: 'Custom',
      period: 'annual license',
      requests: 'Unlimited Sovereign Calls',
      desc: 'For National Ministries, Central Banks, and International System Integrators.',
      features: ['On-Premise GovCloud Deployment', 'GDPR / DPDP Compliance Enclave', 'Custom Country Engine Setup', '24/7 Sovereign Incident Team', 'Full GovStack 2.0 Mediator'],
      highlight: false,
      btnText: 'Contact Government Team'
    }
  ];

  return (
    <div id="section-api-pricing" className="space-y-8">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold">
          <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
          <span>Transparent Usage-Based Billing</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white tracking-tight">
          Flexible Pricing for Banks, Insurers & Governments
        </h2>
        <p className="text-slate-400 text-sm leading-relaxed">
          Unlock instant title verification, encumbrance audits, and AI land fraud risk scoring at scale.
        </p>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {tiers.map((tier) => (
          <div
            key={tier.id}
            id={`card-pricing-tier-${tier.id}`}
            className={`rounded-3xl p-6 shadow-xl flex flex-col justify-between transition-all relative ${
              tier.highlight
                ? 'bg-slate-900 border-2 border-emerald-500 shadow-2xl shadow-emerald-950/40 ring-1 ring-emerald-500/50'
                : 'bg-slate-900/90 border border-slate-800 hover:border-slate-700'
            }`}
          >
            {tier.highlight && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-emerald-500 text-slate-950 font-bold text-[10px] uppercase tracking-wider">
                Most Popular
              </div>
            )}

            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-bold text-white">{tier.name}</h3>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{tier.desc}</p>
              </div>

              <div className="py-2 border-y border-slate-800">
                <div className="flex items-baseline gap-1">
                  <span className="text-3xl font-extrabold text-white">{tier.price}</span>
                  <span className="text-xs text-slate-400">/ {tier.period}</span>
                </div>
                <div className="text-xs font-mono text-emerald-400 mt-1 font-semibold">
                  {tier.requests}
                </div>
              </div>

              <ul className="space-y-2.5 text-xs text-slate-300">
                {tier.features.map((feat, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>

            <button
              id={`btn-select-tier-${tier.id}`}
              className={`w-full mt-6 py-3 rounded-xl text-xs font-bold transition-all ${
                tier.highlight
                  ? 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-lg shadow-emerald-500/20'
                  : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-700'
              }`}
            >
              {tier.btnText}
            </button>
          </div>
        ))}
      </div>

      {/* Interactive Volume Cost Estimator */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl max-w-2xl mx-auto space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
          <Zap className="w-4 h-4 text-emerald-400" />
          <span>Interactive Volume Calculator</span>
        </h3>

        <div className="space-y-2">
          <div className="flex justify-between text-xs text-slate-300 font-semibold">
            <span>Monthly API Request Volume:</span>
            <span className="text-emerald-400 font-mono">{requestVolume.toLocaleString()} calls</span>
          </div>
          <input
            id="range-volume-calculator"
            type="range"
            min="100"
            max="100000"
            step="500"
            value={requestVolume}
            onChange={(e) => setRequestVolume(Number(e.target.value))}
            className="w-full accent-emerald-500 bg-slate-950 h-2 rounded-lg cursor-pointer"
          />
        </div>

        <div className="flex justify-between items-center p-4 bg-slate-950 rounded-2xl border border-slate-800 text-xs">
          <span className="text-slate-400">Estimated Recommended Plan:</span>
          <span className="font-bold text-white text-sm">
            {requestVolume <= 100 ? "Free Sandbox ($0)" : requestVolume <= 10000 ? "Starter Tier ($99/mo)" : requestVolume <= 50000 ? "Pro Tier ($499/mo)" : "Sovereign Enterprise"}
          </span>
        </div>
      </div>
    </div>
  );
};
