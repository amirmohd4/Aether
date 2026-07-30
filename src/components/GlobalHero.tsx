import React from 'react';
import { Globe, ArrowRight, Play, Sparkles, Shield, Zap } from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';

interface GlobalHeroProps {
  onStart: () => void;
}

export const GlobalHero: React.FC<GlobalHeroProps> = ({ onStart }) => {
  const { t } = useTranslation();

  return (
    <div id="section-global-hero" className="relative overflow-hidden pt-12 pb-16 sm:pt-16 sm:pb-20">
      {/* Background Radial Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[650px] bg-gradient-to-tr from-emerald-500/15 to-teal-500/10 rounded-full blur-[140px] pointer-events-none" />

      <div className="max-w-4xl mx-auto text-center space-y-6 relative z-10 px-4">
        
        {/* Subtle Sovereign Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-emerald-500/30 text-emerald-300 text-xs font-semibold shadow-xl">
          <Globe className="w-3.5 h-3.5 text-emerald-400" />
          <span>Universal Sovereign GovOS • 195 UN Member States Ready</span>
        </div>

        {/* Hero Headline */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-black text-white tracking-tight leading-[1.1]">
          Government services, <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">simplified.</span>
        </h1>

        {/* Hero Subtitle */}
        <p className="text-slate-300 text-base sm:text-xl max-w-2xl mx-auto leading-relaxed font-normal">
          Aether connects citizens, businesses, and governments in one seamless platform.
        </p>

        {/* The Single "Start" CTA Button Flow */}
        <div className="pt-4 flex items-center justify-center">
          <button
            id="btn-hero-start"
            onClick={onStart}
            className="group relative inline-flex items-center justify-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-base shadow-2xl shadow-emerald-500/30 hover:shadow-emerald-500/50 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <Play className="w-5 h-5 fill-current text-slate-950 group-hover:scale-110 transition-transform" />
            <span>Start Service Request</span>
            <ArrowRight className="w-5 h-5 text-slate-950 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {/* Key Metrics Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-12 border-t border-slate-800/80 max-w-3xl mx-auto">
          <div className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">195 UN</div>
            <div className="text-xs text-slate-400 mt-1 font-medium">Nations Configurable</div>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">15+</div>
            <div className="text-xs text-slate-400 mt-1 font-medium">Governments Active</div>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">&lt; 3 mins</div>
            <div className="text-xs text-slate-400 mt-1 font-medium">Average Processing</div>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">99.99%</div>
            <div className="text-xs text-slate-400 mt-1 font-medium">Sovereign Uptime</div>
          </div>
        </div>

      </div>
    </div>
  );
};
