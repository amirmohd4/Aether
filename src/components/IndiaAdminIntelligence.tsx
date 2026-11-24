import React, { useEffect, useMemo, useState } from 'react';
import { ArrowDown, Building2, ChevronRight, CircleAlert, Compass, GitBranch, Landmark, Loader2, RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8081').replace(/\/$/, '');

type Service = { id: string; name: string; department_label: string; customer_types: string[] };
type Department = {
  id: string; name: string; levels: string[]; domains: string[];
  examples: string[]; coordination_partners: string[]; service_count: number;
  services: Service[]; catalog_status: string; legal_completeness: string;
  jurisdiction_coverage: string;
};
type JourneyStep = { id: string; service_id: string; service_name: string; label: string; department: string; condition: string };
type JourneyEdge = { from: string; to: string; relationship: string; legal_basis_status: string; is_statutory_prerequisite: boolean | null };
type Journey = { id: string; name: string; description: string; status: string; warning: string; steps: JourneyStep[]; edges: JourneyEdge[]; customer_types: string[] };

export const IndiaAdminIntelligence: React.FC = () => {
  const { session, loading: authLoading, required: authRequired } = useAuth();
  const [departments, setDepartments] = useState<Department[]>([]);
  const [journeys, setJourneys] = useState<Journey[]>([]);
  const [selectedJourney, setSelectedJourney] = useState('');
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'departments' | 'journeys'>('departments');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [overview, setOverview] = useState<Record<string, unknown> | null>(null);

  const authHeaders = () => {
    if (!session?.access_token) return {};
    const tenant = window.localStorage.getItem('aether.tenant_id') || '';
    return {
      Authorization: `Bearer ${session.access_token}`,
      ...(tenant ? { 'X-Aether-Tenant-ID': tenant } : {}),
    };
  };

  async function load() {
    if (authRequired && !session?.access_token) return;
    setLoading(true);
    setError('');
    try {
      const [overviewResponse, departmentsResponse, journeysResponse] = await Promise.all([
        fetch(`${API_BASE}/api/aether/v2/admin-intelligence/overview`, { headers: authHeaders() }),
        fetch(`${API_BASE}/api/aether/v2/admin-intelligence/departments`, { headers: authHeaders() }),
        fetch(`${API_BASE}/api/aether/v2/admin-intelligence/journeys`, { headers: authHeaders() }),
      ]);
      const responses = [overviewResponse, departmentsResponse, journeysResponse];
      if (responses.some(response => !response.ok)) {
        const failed = responses.find(response => !response.ok)!;
        const body = await failed.json().catch(() => ({}));
        throw new Error(body.detail || `Administrative intelligence API returned ${failed.status}`);
      }
      const [overviewBody, departmentBody, journeyBody] = await Promise.all(responses.map(response => response.json()));
      setOverview(overviewBody);
      setDepartments(departmentBody.departments || []);
      setJourneys(journeyBody.journeys || []);
      setSelectedJourney(current => current || journeyBody.journeys?.[0]?.id || '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load administrative intelligence');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!authLoading) void load();
  }, [authLoading, session?.access_token, authRequired]);

  const filteredDepartments = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return departments;
    return departments.filter(department =>
      [department.name, ...department.domains, ...department.examples, ...department.services.map(service => service.name)]
        .join(' ').toLowerCase().includes(term)
    );
  }, [departments, query]);

  const currentJourney = journeys.find(journey => journey.id === selectedJourney) || journeys[0];

  return (
    <section className="w-full bg-slate-950 text-slate-100 px-4 py-10 md:px-8">
      <div className="mx-auto max-w-7xl space-y-7">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.22em] text-cyan-300">
              <Landmark className="h-4 w-4" /> Aether India Intelligence
            </div>
            <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">Administrative operating map</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
              Explore department families, their registered service matches and cross-department journeys.
              This is a discovery layer, not a verified legal checklist.
            </p>
          </div>
          <button onClick={() => void load()} disabled={loading || (authRequired && !session?.access_token)}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-semibold hover:bg-slate-900 disabled:opacity-50">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />} Refresh map
          </button>
        </div>

        {error && <div className="flex items-start gap-3 rounded-xl border border-rose-900 bg-rose-950/40 p-4 text-sm text-rose-200"><CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />{error}</div>}
        {authRequired && !session?.access_token && !authLoading && (
          <div className="rounded-xl border border-amber-800 bg-amber-950/30 p-4 text-sm text-amber-100">
            Sign in to load your authorized Aether workspace and administrative intelligence.
          </div>
        )}

        <div className="grid gap-3 sm:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4"><div className="text-xs text-slate-400">Registered service families</div><div className="mt-2 text-3xl font-semibold">{String(overview?.service_registry_count ?? '—')}</div></div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4"><div className="text-xs text-slate-400">Department profiles</div><div className="mt-2 text-3xl font-semibold">{String(overview?.department_profiles ?? '—')}</div></div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4"><div className="text-xs text-slate-400">Cross-department journeys</div><div className="mt-2 text-3xl font-semibold">{String(overview?.journey_templates ?? '—')}</div></div>
        </div>

        <div className="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-3">
          <button onClick={() => setActiveTab('departments')} className={`rounded-lg px-4 py-2 text-sm font-semibold ${activeTab === 'departments' ? 'bg-cyan-300 text-slate-950' : 'text-slate-400 hover:bg-slate-900'}`}><Building2 className="mr-2 inline h-4 w-4" />Departments</button>
          <button onClick={() => setActiveTab('journeys')} className={`rounded-lg px-4 py-2 text-sm font-semibold ${activeTab === 'journeys' ? 'bg-cyan-300 text-slate-950' : 'text-slate-400 hover:bg-slate-900'}`}><GitBranch className="mr-2 inline h-4 w-4" />Project journeys</button>
          {activeTab === 'departments' && <label className="ml-auto flex min-w-[220px] flex-1 items-center gap-2 rounded-xl border border-slate-700 px-3 py-2 md:max-w-sm"><Search className="h-4 w-4 text-slate-500"/><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Search departments or services" className="w-full bg-transparent text-sm outline-none placeholder:text-slate-500"/></label>}
        </div>

        {activeTab === 'departments' && (
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {filteredDepartments.map(department => (
              <article key={department.id} className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div><h3 className="font-semibold">{department.name}</h3><p className="mt-1 text-xs text-slate-500">{department.levels.join(' · ')}</p></div>
                  <span className="rounded-full bg-slate-800 px-2.5 py-1 text-xs text-cyan-200">{department.service_count} matches</span>
                </div>
                <div className="mt-4 flex flex-wrap gap-1.5">{department.domains.map(domain => <span key={domain} className="rounded-md bg-slate-800 px-2 py-1 text-[11px] text-slate-300">{domain.replaceAll('_', ' ')}</span>)}</div>
                <div className="mt-4 space-y-2">{department.examples.map(example => <div key={example} className="flex gap-2 text-sm text-slate-300"><ChevronRight className="mt-0.5 h-4 w-4 shrink-0 text-cyan-300"/>{example}</div>)}</div>
                {department.services.length > 0 && <details className="mt-4 border-t border-slate-800 pt-3"><summary className="cursor-pointer text-xs font-semibold text-cyan-200">View matched registry services</summary><div className="mt-3 space-y-2">{department.services.map(service => <div key={service.id} className="text-sm"><div>{service.name}</div><div className="text-[11px] text-slate-500">{service.department_label} · {service.customer_types.join(', ')}</div></div>)}</div></details>}
                <div className="mt-4 flex items-center gap-2 text-[11px] text-amber-300"><ShieldCheck className="h-3.5 w-3.5"/> Legal completeness not assessed</div>
              </article>
            ))}
          </div>
        )}

        {activeTab === 'journeys' && currentJourney && (
          <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
            <div className="space-y-2">{journeys.map(journey => <button key={journey.id} onClick={() => setSelectedJourney(journey.id)} className={`w-full rounded-xl border p-3 text-left text-sm ${selectedJourney === journey.id ? 'border-cyan-400 bg-cyan-400/10 text-cyan-100' : 'border-slate-800 bg-slate-900 text-slate-300 hover:bg-slate-900/70'}`}>{journey.name}</button>)}</div>
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 md:p-7">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-cyan-300"><Compass className="h-4 w-4"/> Illustrative planning graph</div>
              <h3 className="mt-2 text-2xl font-semibold">{currentJourney.name}</h3>
              <p className="mt-2 text-sm text-slate-400">{currentJourney.description}</p>
              <div className="mt-5 space-y-2">{currentJourney.steps.map((step, index) => <React.Fragment key={step.id}><div className="rounded-xl border border-slate-700 bg-slate-950 p-4"><div className="flex items-center justify-between gap-3"><div className="font-medium">{index + 1}. {step.label}</div><span className="text-[11px] text-cyan-300">{step.department}</span></div><p className="mt-1 text-xs text-slate-400">{step.condition}</p><p className="mt-2 text-[11px] text-slate-500">Service family: {step.service_name}</p></div>{index < currentJourney.steps.length - 1 && <div className="flex justify-center text-slate-600"><ArrowDown className="h-4 w-4"/></div>}</React.Fragment>)}</div>
              <div className="mt-5 rounded-xl border border-amber-800/70 bg-amber-950/30 p-4 text-xs leading-5 text-amber-100">{currentJourney.warning}</div>
              <div className="mt-4 text-xs text-slate-500">{currentJourney.edges.length} planning relationships · legal basis not verified · not a statutory prerequisite map</div>
            </div>
          </div>
        )}
        {activeTab === 'departments' && filteredDepartments.length === 0 && <div className="rounded-xl border border-slate-800 p-8 text-center text-sm text-slate-400">No matching department or service found.</div>}
      </div>
    </section>
  );
};
