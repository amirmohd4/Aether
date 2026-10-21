import React, { useCallback, useEffect, useState } from 'react';
import { Activity, AlertTriangle, ArrowRight, ClipboardList, RefreshCw, ShieldCheck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8081';

type CaseItem = {
  case_id: string;
  objective: string;
  service_name?: string | null;
  status: string;
};

type ActionItem = {
  idempotency_key: string;
  title: string;
  department: string;
  priority: string;
  execution_mode: string;
  required_evidence: string[];
  requires_human_decision: boolean;
};

type DeliveryReport = {
  case_id: string;
  mode: string;
  risk_assessment: {
    summary: { finding_count: number; critical_count: number; warning_count: number; progress_blocker_count: number };
    findings: Array<{ code: string; severity: string; title: string; message: string; evidence_needed: string[] }>;
  };
  cross_department_orchestration: {
    department_count: number;
    task_count: number;
    open_handoff_count: number;
    human_authority_count: number;
    handoffs: Array<{ task_id: string; task: string; department: string; status: string; blocked_by: string[]; next_action: string; human_authority_required: boolean }>;
  };
  administrative_action_plan: { count: number; mode: string; actions: ActionItem[]; note: string };
};

export const DeliveryOpsConsole: React.FC = () => {
  const { session, loading: authLoading, required: authRequired } = useAuth();
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [selectedCase, setSelectedCase] = useState('');
  const [report, setReport] = useState<DeliveryReport | null>(null);
  const [loadingCases, setLoadingCases] = useState(false);
  const [loadingReport, setLoadingReport] = useState(false);
  const [error, setError] = useState('');

  const headers = useCallback(() => (
    session?.access_token ? { Authorization: `Bearer ${session.access_token}` } : {}
  ), [session?.access_token]);

  const loadCases = useCallback(async () => {
    if (authRequired && !session) return;
    setLoadingCases(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/api/aether/v2/cases?limit=50`, { headers: headers() });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Case list returned ${response.status}`);
      const items = (body.cases || []) as CaseItem[];
      setCases(items);
      setSelectedCase((current) => current && items.some((item) => item.case_id === current) ? current : (items[0]?.case_id || ''));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load cases');
    } finally {
      setLoadingCases(false);
    }
  }, [authRequired, session, headers]);

  const analyzeCase = useCallback(async (caseId: string) => {
    if (!caseId) return;
    setLoadingReport(true);
    setError('');
    try {
      const response = await fetch(
        `${API_BASE}/api/aether/v2/cases/${encodeURIComponent(caseId)}/delivery-intelligence`,
        { headers: headers() }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Delivery analysis returned ${response.status}`);
      setReport(body as DeliveryReport);
    } catch (err) {
      setReport(null);
      setError(err instanceof Error ? err.message : 'Unable to analyze delivery case');
    } finally {
      setLoadingReport(false);
    }
  }, [headers]);

  useEffect(() => {
    void loadCases();
  }, [loadCases]);

  useEffect(() => {
    if (selectedCase) void analyzeCase(selectedCase);
  }, [selectedCase, analyzeCase]);

  if (authLoading || (authRequired && !session)) return null;

  return (
    <section className="mx-auto max-w-7xl space-y-5 bg-slate-950 px-5 py-10 text-slate-100 md:px-8">
      <div className="rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-300/[0.08] to-white/[0.02] p-6 md:p-8">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold text-cyan-200">
              <Activity className="h-3.5 w-3.5" /> Cross-department delivery operations
            </div>
            <h2 className="mt-4 text-2xl font-bold md:text-3xl">Developer & contractor control room</h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              Surface project risks, identify blocked department handoffs, and prepare a prioritized administrative action list from an existing Aether case.
            </p>
          </div>
          <button onClick={() => void loadCases()} disabled={loadingCases} className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-semibold hover:bg-white/5 disabled:opacity-50">
            <RefreshCw className={`h-4 w-4 ${loadingCases ? 'animate-spin' : ''}`} /> Refresh cases
          </button>
        </div>
        <div className="mt-6 grid gap-3 md:grid-cols-[minmax(0,1fr)_auto]">
          <label className="space-y-2 text-xs font-semibold text-slate-400">
            Active case
            <select value={selectedCase} onChange={(event) => setSelectedCase(event.target.value)} className="w-full rounded-xl border border-white/10 bg-slate-900 px-3 py-3 text-sm text-slate-100">
              {cases.length === 0 && <option value="">No accessible cases</option>}
              {cases.map((item) => <option key={item.case_id} value={item.case_id}>{item.service_name || item.objective} · {item.case_id}</option>)}
            </select>
          </label>
          <button onClick={() => void analyzeCase(selectedCase)} disabled={!selectedCase || loadingReport} className="inline-flex items-center justify-center gap-2 self-end rounded-xl bg-cyan-300 px-4 py-3 text-sm font-bold text-slate-950 disabled:opacity-50">
            {loadingReport ? 'Analyzing…' : 'Analyze delivery'} <ArrowRight className="h-4 w-4" />
          </button>
        </div>
        {error && <p role="alert" className="mt-4 rounded-xl border border-red-300/20 bg-red-300/5 p-3 text-sm text-red-200">{error}</p>}
      </div>

      {report && (
        <>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            <Metric label="Risk findings" value={report.risk_assessment.summary.finding_count} />
            <Metric label="Critical risks" value={report.risk_assessment.summary.critical_count} />
            <Metric label="Progress blockers" value={report.risk_assessment.summary.progress_blocker_count} />
            <Metric label="Open handoffs" value={report.cross_department_orchestration.open_handoff_count} />
            <Metric label="Proposed admin actions" value={report.administrative_action_plan.count} />
          </div>

          <div className="grid gap-5 lg:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
              <div className="flex items-center gap-2"><AlertTriangle className="h-5 w-5 text-amber-300" /><h3 className="font-semibold">Risk register</h3></div>
              {report.risk_assessment.findings.length === 0 ? (
                <p className="mt-4 text-sm text-slate-400">No findings from the supplied inputs. Missing inputs are not proof of safety or compliance.</p>
              ) : (
                <div className="mt-4 space-y-3">
                  {report.risk_assessment.findings.map((finding, index) => (
                    <article key={finding.code + index} className="rounded-xl border border-white/5 bg-black/10 p-3">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <h4 className="text-sm font-semibold">{finding.title}</h4>
                        <span className={`rounded-full px-2 py-1 text-[10px] uppercase ${finding.severity === 'critical' ? 'bg-red-300/10 text-red-200' : finding.severity === 'warning' ? 'bg-amber-300/10 text-amber-200' : 'bg-slate-300/10 text-slate-300'}`}>{finding.severity}</span>
                      </div>
                      <p className="mt-2 text-xs leading-5 text-slate-400">{finding.message}</p>
                      {finding.evidence_needed.length > 0 && <p className="mt-2 text-[10px] text-cyan-200/80">Evidence needed: {finding.evidence_needed.join(', ')}</p>}
                    </article>
                  ))}
                </div>
              )}
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
              <div className="flex items-center gap-2"><ClipboardList className="h-5 w-5 text-cyan-300" /><h3 className="font-semibold">Administrative action plan</h3></div>
              <p className="mt-2 text-xs leading-5 text-slate-500">{report.administrative_action_plan.note}</p>
              {report.administrative_action_plan.actions.length === 0 ? (
                <p className="mt-4 text-sm text-slate-400">No action proposals from the current findings and handoffs.</p>
              ) : (
                <div className="mt-4 space-y-3">
                  {report.administrative_action_plan.actions.map((action) => (
                    <article key={action.idempotency_key} className="rounded-xl border border-white/5 bg-black/10 p-3">
                      <div className="flex flex-wrap items-start justify-between gap-2">
                        <h4 className="text-sm font-semibold">{action.title}</h4>
                        <span className={`rounded-full px-2 py-1 text-[10px] uppercase ${action.priority === 'critical' ? 'bg-red-300/10 text-red-200' : action.priority === 'high' ? 'bg-amber-300/10 text-amber-200' : 'bg-slate-300/10 text-slate-300'}`}>{action.priority}</span>
                      </div>
                      <p className="mt-1 text-xs text-slate-400">Department: {action.department}</p>
                      {action.required_evidence.length > 0 && <p className="mt-2 text-[10px] text-slate-500">Required evidence: {action.required_evidence.join(', ')}</p>}
                      <p className="mt-2 text-[10px] text-violet-200">{action.requires_human_decision ? 'Human decision boundary applies' : 'Administrative preparation candidate'} · Not yet queued</p>
                    </article>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <div className="flex items-center gap-2"><ShieldCheck className="h-5 w-5 text-emerald-300" /><h3 className="font-semibold">Cross-department handoffs</h3></div>
            <p className="mt-2 text-xs text-slate-500">{report.cross_department_orchestration.task_count} tasks across {report.cross_department_orchestration.department_count} departments · {report.cross_department_orchestration.human_authority_count} require human/physical authority.</p>
            {report.cross_department_orchestration.handoffs.length === 0 ? (
              <p className="mt-4 text-sm text-slate-400">No open task handoffs in the recorded case state.</p>
            ) : (
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {report.cross_department_orchestration.handoffs.map((handoff) => (
                  <article key={handoff.task_id} className="rounded-xl border border-white/5 bg-black/10 p-3">
                    <div className="flex items-start justify-between gap-2"><h4 className="text-sm font-semibold">{handoff.task}</h4><span className="text-[10px] text-slate-500">{handoff.status}</span></div>
                    <p className="mt-1 text-xs text-slate-400">{handoff.department}</p>
                    <p className="mt-2 text-xs text-cyan-100">{handoff.next_action}</p>
                    {handoff.blocked_by.length > 0 && <p className="mt-1 text-[10px] text-amber-200">Blocked by: {handoff.blocked_by.join(', ')}</p>}
                  </article>
                ))}
              </div>
            )}
          </div>
        </>
      )}
      <p className="text-[10px] leading-5 text-slate-600">Advisory and controlled-MVP view. It does not independently verify official systems, submit statutory filings, approve construction, or release payments.</p>
    </section>
  );
};

const Metric = ({ label, value }: { label: string; value: number }) => (
  <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
    <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
    <p className="mt-2 text-2xl font-bold">{value}</p>
  </div>
);
