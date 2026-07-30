import React, { useState } from 'react';
import { Search, Landmark, Car, Building2, Activity, Cpu, Database, ShieldCheck, ArrowRight, Zap, CheckCircle2, Clock } from 'lucide-react';
import { COUNTRIES_CONFIG, Service, Department, getCountryConfig } from '../configs/countriesData';
import { useTranslation } from '../hooks/useTranslation';

interface GlobalCatalogProps {
  countryCode: string;
  onSelectServiceForDemo?: (countryCode: string, serviceId: string) => void;
}

export const GlobalCatalog: React.FC<GlobalCatalogProps> = ({
  countryCode,
  onSelectServiceForDemo
}) => {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDeptId, setSelectedDeptId] = useState<string>('all');

  const country = getCountryConfig(countryCode);

  const getDepartmentIcon = (iconName: string) => {
    switch (iconName) {
      case 'Landmark': return <Landmark className="w-5 h-5 text-emerald-400" />;
      case 'Car': return <Car className="w-5 h-5 text-blue-400" />;
      case 'Building2': return <Building2 className="w-5 h-5 text-purple-400" />;
      case 'Activity': return <Activity className="w-5 h-5 text-rose-400" />;
      case 'Cpu': return <Cpu className="w-5 h-5 text-cyan-400" />;
      case 'Database': return <Database className="w-5 h-5 text-amber-400" />;
      default: return <ShieldCheck className="w-5 h-5 text-emerald-400" />;
    }
  };

  const filteredServices = country.services.filter((service) => {
    const matchesSearch = service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          service.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDept = selectedDeptId === 'all' || service.department_id === selectedDeptId;
    return matchesSearch && matchesDept;
  });

  return (
    <div id="section-global-catalog" className="space-y-6">
      {/* Country Header Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 opacity-10 text-9xl select-none pointer-events-none">
          {country.flag}
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-3">
              <span className="text-4xl">{country.flag}</span>
              <div>
                <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                  <span>{country.country_name} Sovereign Service Catalog</span>
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  ID System: <span className="text-emerald-400 font-medium">{country.id_system.name}</span> ({country.id_system.format}) • Currency: <span className="text-amber-400 font-medium">{country.currency.name} ({country.currency.symbol})</span>
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-slate-800/80 p-2 rounded-xl border border-slate-700">
            <Zap className="w-4 h-4 text-emerald-400 animate-pulse" />
            <span className="text-xs text-slate-300 font-medium">
              {country.services.length} Fully Automated Digital Services Available
            </span>
          </div>
        </div>
      </div>

      {/* Search and Department Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            id="input-search-services"
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={t('search_services', 'Search departments or services...')}
            className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          <button
            id="btn-dept-filter-all"
            onClick={() => setSelectedDeptId('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
              selectedDeptId === 'all'
                ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
            }`}
          >
            {t('all_departments', 'All Departments')}
          </button>
          {country.departments.map((dept) => (
            <button
              key={dept.id}
              id={`btn-dept-filter-${dept.id}`}
              onClick={() => setSelectedDeptId(dept.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all flex items-center gap-1.5 ${
                selectedDeptId === dept.id
                  ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
              }`}
            >
              <span>{dept.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Services Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredServices.map((service) => {
          const dept = country.departments.find((d) => d.id === service.department_id);
          return (
            <div
              key={service.id}
              id={`card-service-${service.id}`}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all hover:shadow-2xl hover:shadow-emerald-950/20 group"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="p-2.5 bg-slate-800 border border-slate-700/80 rounded-xl">
                    {getDepartmentIcon(dept?.icon || 'Landmark')}
                  </div>
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-950/80 border border-emerald-800/80 text-[10px] font-mono font-medium text-emerald-400">
                    <Clock className="w-3 h-3 text-emerald-400" />
                    {service.processing_time}
                  </span>
                </div>

                <div>
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    {dept?.name || 'Government Registry'}
                  </div>
                  <h3 className="text-base font-semibold text-white mt-0.5 group-hover:text-emerald-300 transition-colors">
                    {service.name}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
                    {service.description}
                  </p>
                </div>

                {/* Workflow Steps Preview */}
                <div className="bg-slate-950/70 rounded-xl p-3 border border-slate-800/80 space-y-1.5">
                  <div className="text-[10px] font-semibold uppercase text-slate-400 tracking-wider">
                    Automated Steps ({service.workflow_steps.length}):
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {service.workflow_steps.map((step, idx) => (
                      <span key={step.id} className="text-[10px] bg-slate-800/90 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                        {idx + 1}. {step.name}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Fees Breakdown */}
                <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-800/80">
                  <span className="text-slate-400">{t('fees_lbl', 'Base Fee')}:</span>
                  <span className="font-semibold text-amber-400">
                    {country.currency.symbol} {service.fees.base_fee.toLocaleString()}
                  </span>
                </div>
                {service.fees.stamp_duty_percentage > 0 && (
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400">{t('stamp_duty_lbl', 'Stamp Duty')}:</span>
                    <span className="font-semibold text-emerald-400">
                      {service.fees.stamp_duty_percentage}%
                    </span>
                  </div>
                )}
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-1 text-[11px] text-slate-400">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Sovereign Verified</span>
                </div>
                {onSelectServiceForDemo && (
                  <button
                    id={`btn-launch-demo-${service.id}`}
                    onClick={() => onSelectServiceForDemo(countryCode, service.id)}
                    className="flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold rounded-lg transition-all shadow-md shadow-emerald-500/20"
                  >
                    <span>Test In Demo</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {filteredServices.length === 0 && (
        <div className="text-center py-12 bg-slate-900 border border-slate-800 rounded-2xl">
          <p className="text-sm text-slate-400">No services found matching your filter criteria.</p>
        </div>
      )}
    </div>
  );
};
