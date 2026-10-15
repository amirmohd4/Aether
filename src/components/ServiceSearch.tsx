import React, { useState, useMemo } from 'react';
import { 
  Search, Shield, Home, Briefcase, Car, Wheat, 
  FileText, Sparkles, ChevronRight, X, UserCheck, ShieldCheck
} from 'lucide-react';

export interface ServiceItem {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: string;
  processingTime: string;
}

export const MASTER_GLOBAL_SERVICES: ServiceItem[] = servicesConfig.map((service) => ({
  id: service.id,
  name: service.label,
  category: service.id === 'birth-certificate' || service.id === 'death-certificate' || service.id === 'passport' || service.id === 'visa'
    ? 'Identity & Documents'
    : /property|mutation|encumbrance|land|title|building|housing|pmay|rera/.test(service.id)
      ? 'Property & Land'
      : /driving|vehicle/.test(service.id)
        ? 'Transport & Driving'
        : /scholarship|admission|transfer|ration|pds|farmer|crop/.test(service.id)
          ? 'Health & Welfare'
          : 'Business & Licenses',
  description: `Synthetic workflow template. Requirements and service availability depend on the jurisdiction; no official system is connected.`,
  icon: service.icon,
  processingTime: 'Mock only',
}));
interface ServiceSearchProps {
  onSelectService: (service: ServiceItem) => void;
  autoFocus?: boolean;
}

export const ServiceSearch: React.FC<ServiceSearchProps> = ({
  onSelectService,
  autoFocus = true
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = [
    { label: 'All', icon: Sparkles },
    { label: 'Identity & Documents', icon: Shield },
    { label: 'Property & Land', icon: Home },
    { label: 'Business & Licenses', icon: Briefcase },
    { label: 'Transport & Driving', icon: Car },
    { label: 'Health & Welfare', icon: Wheat },
  ];

  const filteredServices = useMemo(() => {
    return MASTER_GLOBAL_SERVICES.filter(service => {
      const matchesSearch = 
        service.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        service.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        service.category.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesCategory = selectedCategory === 'All' || service.category === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, selectedCategory]);

  return (
    <div className="w-full space-y-4">
      {/* Search Input Box */}
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-2xl blur-md opacity-75 group-hover:opacity-100 transition-opacity" />
        <div className="relative bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl flex items-center p-2">
          <Search className="w-5 h-5 text-emerald-400 ml-3 mr-2 flex-shrink-0" />
          <input
            id="input-global-service-search"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for a service (e.g. birth certificate, property registration)..."
            autoFocus={autoFocus}
            className="w-full bg-transparent text-white placeholder-slate-400 text-sm sm:text-base px-2 py-2 focus:outline-none"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 mr-1"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Category Pills Filter */}
      <div className="flex gap-1.5 overflow-x-auto pb-2 pt-1 scrollbar-none">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const isSelected = selectedCategory === cat.label;
          return (
            <button
              key={cat.label}
              id={`btn-cat-${cat.label.toLowerCase().replace(/[^a-z0-9]/g, '-')}`}
              onClick={() => setSelectedCategory(cat.label)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                isSelected
                  ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                  : 'bg-slate-900/90 text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{cat.label}</span>
            </button>
          );
        })}
      </div>

      {/* Results List */}
      <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
        {filteredServices.length === 0 ? (
          <div className="p-8 text-center bg-slate-900/50 rounded-2xl border border-slate-800 space-y-2">
            <p className="text-sm font-medium text-slate-300">No matching services found for "{searchQuery}"</p>
            <p className="text-xs text-slate-500">Try searching for 'birth certificate', 'property registration', or 'business license'.</p>
          </div>
        ) : (
          filteredServices.map((service) => (
            <button
              key={service.id}
              id={`btn-select-srv-${service.id}`}
              onClick={() => onSelectService(service)}
              className="w-full text-left p-4 rounded-2xl bg-slate-900 hover:bg-slate-800/90 border border-slate-800 hover:border-emerald-500/50 transition-all group flex items-start justify-between gap-4 shadow-sm"
            >
              <div className="flex items-start gap-3.5">
                <span className="text-2xl p-2 rounded-xl bg-slate-950 border border-slate-800 flex-shrink-0 group-hover:scale-110 transition-transform">
                  {service.icon}
                </span>
                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold text-sm text-white group-hover:text-emerald-400 transition-colors">
                      {service.name}
                    </span>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-950 text-slate-400 border border-slate-800">
                      {service.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                    {service.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 flex-shrink-0 self-center">
                <span className="text-[10px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 hidden sm:inline-block">
                  {service.processingTime}
                </span>
                <div className="w-8 h-8 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-400 group-hover:text-emerald-400 group-hover:border-emerald-500/50 group-hover:translate-x-0.5 transition-all">
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
};
