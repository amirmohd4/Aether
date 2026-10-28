import React from 'react';
import { ChevronRight } from 'lucide-react';

export interface ServiceItem {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: string;
}

import { servicesConfig } from '../servicesConfig';

export const INDIA_32_SERVICES: ServiceItem[] = servicesConfig.map(service => ({
  id: service.id,
  name: service.label,
  category: /property|mutation|encumbrance|land|title|building|housing|pmay|rera/.test(service.id) ? 'Property & Land'
    : /birth|death|passport|visa/.test(service.id) ? 'Identity & Documents'
    : /driving|vehicle/.test(service.id) ? 'Transport & Driving'
    : /scholarship|admission|transfer|ration|pds|farmer|crop/.test(service.id) ? 'Health & Welfare'
    : /water/.test(service.id) ? 'Utilities & Power'
    : /police|fir/.test(service.id) ? 'Public Safety & Records'
    : /gst|pf-esi|pds|ration|pmay|rera|company/.test(service.id) ? 'India-specific reference'
    : 'Business & Licenses',
  description: 'Synthetic workflow template; actual requirements and availability depend on the selected jurisdiction.',
  icon: service.icon,
}));

/** Kept as a compatibility export; all jurisdictions use the same canonical 32-template list. */
export const GENERIC_SERVICES: ServiceItem[] = INDIA_32_SERVICES;

interface ServiceListProps {
  countryCode: string;
  searchQuery?: string;
  onSelectService: (service: ServiceItem) => void;
}

export const ServiceList: React.FC<ServiceListProps> = ({
  countryCode,
  searchQuery = '',
  onSelectService
}) => {
  const isIndia = countryCode.toUpperCase() === 'IN';
  const rawServices = INDIA_32_SERVICES;

  const filteredServices = searchQuery.trim()
    ? rawServices.filter(
        s => s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
             s.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
             s.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : rawServices;

  return (
    <div className="w-full space-y-3 text-left">
      <div className="flex items-center justify-between px-1">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
          {isIndia ? '32 synthetic service templates · India references included' : '32 synthetic service templates · jurisdiction configurable'}
        </span>
        <span className="text-xs text-slate-400 font-medium">
          {filteredServices.length} service{filteredServices.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="grid grid-cols-1 gap-2.5 max-h-80 overflow-y-auto pr-1">
        {filteredServices.length === 0 ? (
          <div className="p-4 text-center bg-slate-50 border border-slate-200 rounded-xl text-slate-500 text-sm">
            No service templates match "{searchQuery}".
          </div>
        ) : (
          filteredServices.map((service) => (
            <button
              key={service.id}
              id={`btn-service-${service.id}`}
              onClick={() => onSelectService(service)}
              className="w-full text-left p-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-[#1a365d] transition-all flex items-center justify-between gap-3 group shadow-xs cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl flex-shrink-0 p-2 rounded-lg bg-slate-100">
                  {service.icon}
                </span>
                <div>
                  <div className="font-bold text-sm text-slate-900 group-hover:text-[#1a365d] transition-colors">
                    {service.name}
                  </div>
                  <div className="text-xs text-slate-500 line-clamp-1">
                    {service.description}
                  </div>
                </div>
              </div>

              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-[#1a365d] group-hover:translate-x-0.5 transition-all flex-shrink-0" />
            </button>
          ))
        )}
      </div>
    </div>
  );
};
