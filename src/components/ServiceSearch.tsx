import React, { useState, useMemo } from 'react';
import { 
  Search, Shield, Home, Briefcase, Car, Wheat, Scale, 
  FileText, Sparkles, ChevronRight, X, UserCheck, ShieldCheck
} from 'lucide-react';

export interface ServiceItem {
  id: string;
  name: string;
  category: 'Identity & Documents' | 'Property & Land' | 'Business & Licenses' | 'Transport & Driving' | 'Health & Welfare' | 'Legal & Courts';
  description: string;
  icon: string;
  processingTime: string;
}

export const MASTER_GLOBAL_SERVICES: ServiceItem[] = [
  {
    id: 'birth_cert',
    name: 'Birth Certificate',
    category: 'Identity & Documents',
    description: 'Instant vital statistics registration, civil registry verification, and e-Birth Certificate issuance.',
    icon: '🆔',
    processingTime: '< 3 minutes'
  },
  {
    id: 'prop_reg',
    name: 'Property Registration',
    category: 'Property & Land',
    description: 'Cadastral land registry audit, instant title verification, stamp duty settlement, and digital title deed issuance.',
    icon: '🏠',
    processingTime: '< 30 seconds'
  },
  {
    id: 'biz_license',
    name: 'Business License',
    category: 'Business & Licenses',
    description: 'Automated company incorporation, trade name reservation, municipal clearance, and commercial license.',
    icon: '📄',
    processingTime: '< 2 minutes'
  },
  {
    id: 'driving_license',
    name: 'Driving License',
    category: 'Transport & Driving',
    description: 'Biometric driver record verification, citation audit, and digital driving permit pass.',
    icon: '🚗',
    processingTime: '< 1 minute'
  },
  {
    id: 'crop_insurance',
    name: 'Crop Insurance',
    category: 'Health & Welfare',
    description: 'Satellite agricultural land parcel check, weather index audit, and instant claim payout clearance.',
    icon: '🌾',
    processingTime: '< 5 minutes'
  },
  {
    id: 'court_filing',
    name: 'Court Case Filing',
    category: 'Legal & Courts',
    description: 'E-filing judicial petitions, case clearance verification, and digital court order issuance.',
    icon: '⚖️',
    processingTime: '< 2 minutes'
  },
  {
    id: 'passport_renew',
    name: 'Passport Renewal',
    category: 'Identity & Documents',
    description: 'Consular database audit, identity verification, and diplomatic passport re-issuance pass.',
    icon: '🛂',
    processingTime: '< 4 minutes'
  },
  {
    id: 'tax_clearance',
    name: 'Tax Clearance Certificate',
    category: 'Business & Licenses',
    description: 'Revenue authority audit, zero-liability calculation, and official tax compliance certificate.',
    icon: '🧾',
    processingTime: '< 30 seconds'
  },
  {
    id: 'building_permit',
    name: 'Building & Construction Permit',
    category: 'Property & Land',
    description: 'Zoning compliance check, architectural AI safety audit, and municipal construction pass.',
    icon: '🏗️',
    processingTime: '< 10 minutes'
  }
];

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
    { label: 'Legal & Courts', icon: Scale },
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
