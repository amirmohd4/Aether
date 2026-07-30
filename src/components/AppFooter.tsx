import React from 'react';
import { Globe, Github, Shield, Heart, ExternalLink } from 'lucide-react';

interface AppFooterProps {
  onNavigate?: (view: string) => void;
}

export const AppFooter: React.FC<AppFooterProps> = ({ onNavigate }) => {
  return (
    <footer className="bg-slate-950 border-t border-slate-800 text-slate-400 text-xs pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Column */}
          <div className="space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/20">
                <Globe className="w-4 h-4" />
              </div>
              <span className="font-black text-base text-white tracking-tight">
                Aether<span className="text-emerald-400">.</span>
              </span>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed">
              Global Sovereign Governance Platform. Connecting citizens, businesses, and governments across 195 UN member states.
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              Repository: amirmohd4/Aether
            </div>
          </div>

          {/* Core Navigation */}
          <div className="space-y-2">
            <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider">Platform</h4>
            <ul className="space-y-1.5 text-slate-400">
              <li>
                <button 
                  onClick={() => onNavigate?.('demo')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  Global Demo
                </button>
              </li>
              <li>
                <button 
                  onClick={() => onNavigate?.('catalog')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  195 Nations Catalog
                </button>
              </li>
              <li>
                <button 
                  onClick={() => onNavigate?.('developer')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  Developer API Marketplace
                </button>
              </li>
              <li>
                <button 
                  onClick={() => onNavigate?.('pricing')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  Sovereign Pricing
                </button>
              </li>
            </ul>
          </div>

          {/* Compliance & Standards */}
          <div className="space-y-2">
            <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider">Standards</h4>
            <ul className="space-y-1.5 text-slate-400">
              <li>GovStack 2.0 Compliant</li>
              <li>Sovereign Data Residency</li>
              <li>Zero-Trust Identity Engine</li>
              <li>Cross-Border Interoperability</li>
              <li>W3C Verifiable Credentials</li>
            </ul>
          </div>

          {/* GitHub Repo & Actions */}
          <div className="space-y-3">
            <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider">Open Source Repo</h4>
            <p className="text-slate-400 text-xs">
              Aether GovOS source code is maintained on GitHub.
            </p>
            <a
              id="link-footer-github"
              href="https://github.com/amirmohd4/Aether"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-white font-semibold text-xs transition-all shadow-sm"
            >
              <Github className="w-4 h-4 text-emerald-400" />
              <span>amirmohd4/Aether</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>
          </div>
        </div>

        {/* Bottom copyright line */}
        <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <div>
            © {new Date().getFullYear()} Aether GovOS. Built for 195 Sovereign UN Nations.
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-emerald-400" />
              <span>GovStack 2.0 Certified</span>
            </span>
            <span>•</span>
            <span>amirmohd4/Aether</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
