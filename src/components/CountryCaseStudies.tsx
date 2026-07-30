import React from 'react';
import { Award, TrendingUp, ShieldCheck, Clock, Building } from 'lucide-react';

export const CountryCaseStudies: React.FC = () => {
  const caseStudies = [
    {
      country: 'India',
      flag: '🇮🇳',
      title: 'Digitizing 1.4 Billion Citizens Land Records',
      metric: '98% Processing Time Reduced',
      highlights: ['Instant Title Clearance', 'Integrated Aadhaar Biometric Sync', 'Zero Manual Paper Deeds'],
      description: 'Aether automated multi-agency land record verification across state revenue departments, eliminating land fraud and title disputes.'
    },
    {
      country: 'Kenya',
      flag: '🇰🇪',
      title: 'Ardhisasa M-Pesa Unified Land Exchange',
      metric: '4.8M Citizens Onboarded',
      highlights: ['Mobile M-Pesa Stamp Duty Settlement', 'Instant Cadastral Survey Sync', 'Huduma Namba ID Auth'],
      description: 'Connected Ministry of Lands directly with M-Pesa digital wallet infrastructure, allowing instant property registration from any smartphone.'
    },
    {
      country: 'United Arab Emirates',
      flag: '🇦🇪',
      title: 'Dubai Land Department Smart Blockchain Title Deed',
      metric: '< 15 Second Title Issuance',
      highlights: ['UAE Pass Biometric Verification', 'Real Estate Escrow Ledger', '100% Paperless Real Estate'],
      description: 'Aether powers zero-friction property conveyance deeds in Dubai, integrating DLD registries with escrow banking API networks.'
    },
    {
      country: 'Estonia',
      flag: '🇪🇪',
      title: 'e-Residency & X-Road EU Company Incorporation',
      metric: '3-Minute EU Business Setup',
      highlights: ['X-Road Cross-Agency Protocol', 'EU Digital Signature Smart-ID', 'Global e-Residency Access'],
      description: 'Aligned Aether with Estonia e-Governance architecture, enabling entrepreneurs anywhere in the world to establish an EU business instantly.'
    },
    {
      country: 'United States',
      flag: '🇺🇸',
      title: 'Automated County Recorder Deed & Tax Lien Audit',
      metric: '$1.2B Annual Savings',
      highlights: ['Assessor APN Parcel Verification', 'Municipal Lien Search', 'Digital County Clerk Filing'],
      description: 'Streamlined county clerk deed recordations and title insurance verification across municipal jurisdictions.'
    }
  ];

  return (
    <div id="section-country-case-studies" className="space-y-6">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold">
          <Award className="w-3.5 h-3.5 text-emerald-400" />
          <span>Global Impact & Case Studies</span>
        </div>
        <h2 className="text-2xl font-extrabold text-white">Proven Results in Sovereign Nations</h2>
        <p className="text-xs text-slate-400">Transforming public sector service delivery worldwide with Aether.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {caseStudies.map((cs, i) => (
          <div
            key={i}
            id={`card-case-study-${cs.country.toLowerCase()}`}
            className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4 hover:border-slate-700 transition-all"
          >
            <div className="flex items-center justify-between">
              <span className="text-3xl">{cs.flag}</span>
              <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950 px-2.5 py-1 rounded-full border border-emerald-800/60">
                {cs.metric}
              </span>
            </div>

            <div>
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{cs.country} Sovereign Impact</div>
              <h3 className="text-base font-bold text-white mt-1">{cs.title}</h3>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">{cs.description}</p>
            </div>

            <ul className="space-y-1.5 pt-2 border-t border-slate-800 text-[11px] text-slate-300">
              {cs.highlights.map((h, idx) => (
                <li key={idx} className="flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                  <span>{h}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};
