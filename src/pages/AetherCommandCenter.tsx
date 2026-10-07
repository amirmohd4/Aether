import React, { useMemo, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  Activity, ArrowRight, CheckCircle2, CircleAlert, FileText,
  Globe2, Loader2, ShieldCheck, UserRound, RefreshCw
} from 'lucide-react';

type Task = {
  id: string;
  name: string;
  department: string;
  worker: string;
  dependencies: string[];
  status: string;
  result?: Record<string, unknown> | null;
  error?: string | null;
  attempts?: number;
};

type Requirement = {
  name: string;
  documents: string[];
  source?: string | null;
  confidence?: string;
};

type CaseResponse = {
  summary: {
    case_id: string;
    objective: string;
    customer_type: string;
    service_id?: string | null;
    service_name?: string | null;
    service_department?: string | null;
    status: string;
    tasks_total: number;
    tasks_completed: number;
    tasks_running: number;
    tasks_waiting: number;
    human_actions: number;
    exceptions: number;
    ready: number;
    critical_path: string[];
    human_work_remaining: number;
  };
  requirements: Requirement[];
  human_actions: Array<{ task_id: string; task: string; reason: string }>;
  exceptions: Array<{ type?: string; severity?: string; message?: string; error?: string }>;
  evidence: Array<{ source: string; request_id?: string; operation?: string }>;
  tasks: Record<string, Omit<Task, 'id'>> | Task[];
  outcome?: Record<string, unknown> | null;
};

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8081';

const DEMO_DOCUMENTS = [
  'identity_document',
  'address_proof',
  'lease_or_ownership',
  'business_registration',
  'food_business_details',
  'site_plan',
  'building_plan',
  'floor_plan',
  'fire_safety_details',
  'legal_occupancy',
  'parking_plan',
  'premises_photo',
  'rent_deed_or_affidavit',
  'employer_photo',
  'tax_details',
  'sale_deed',
  'property_record',
  'loan_application',
  'land_record',
  'vehicle_record',
  'birth_record',
  'death_record',
  'education_record',
  'passport_document',
  'income_or_eligibility_proof',
];

function taskList(tasks: CaseResponse['tasks']): Task[] {
  return Array.isArray(tasks)
    ? tasks
    : Object.entries(tasks || {}).map(([id, task]) => ({ id, ...task }));
}

export const AetherCommandCenter: React.FC = () => {
  const [objective, setObjective] = useState('I want to open a restaurant');
  const [customerType, setCustomerType] = useState('business');
  const [country, setCountry] = useState('India');
  const [state, setState] = useState('Jammu and Kashmir');
  const [district, setDistrict] = useState('Jammu');
  const [caseData, setCaseData] = useState<CaseResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authMode, setAuthMode] = useState<'signin' | 'signup'>('signin');
  const [authMessage, setAuthMessage] = useState('');
  const { session, loading: authLoading, required: authRequired, signIn, signUp, signOut } = useAuth();

  const completedPercent = useMemo(() => {
    if (!caseData?.summary.tasks_total) return 0;
    return Math.round((caseData.summary.tasks_completed / caseData.summary.tasks_total) * 100);
  }, [caseData]);

  const authHeaders = () => session?.access_token ? { Authorization: `Bearer ${session.access_token}` } : {};

  async function submitAuth() {
    setAuthMessage('');
    const message = authMode === 'signin'
      ? await signIn(authEmail, authPassword)
      : await signUp(authEmail, authPassword);
    setAuthMessage(message || (authMode === 'signin' ? 'Signed in.' : 'Account created. Check your email if confirmation is enabled.'));
  }

  async function startCase() {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/api/aether/v2/cases`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country, state, district },
          inputs: {
            documents: DEMO_DOCUMENTS,
            owner_name: 'Demo Owner',
            parcel_id: 'PARCEL-DEMO-001',
            property_id: 'PROPERTY-DEMO-001',
            company_id: 'COMPANY-DEMO-001',
            project_id: 'PROJECT-DEMO-001',
            demo_mode: true,
          },
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Aether API returned ${response.status}`);
      setCaseData(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to start Aether case');
    } finally {
      setLoading(false);
    }
  }

  async function continueHumanTask(taskId: string, approved = true) {
    if (!caseData) return;
    setLoading(true);
    setError('');
    try {
      const response = await fetch(
        `${API_BASE}/api/aether/v2/cases/${caseData.summary.case_id}/human/${taskId}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...authHeaders() },
          body: JSON.stringify({ approved, note: 'MVP authorised-human action' }),
        }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Human action returned ${response.status}`);
      setCaseData(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to continue case');
    } finally {
      setLoading(false);
    }
  }

  const tasks = caseData ? taskList(caseData.tasks) : [];

  if (authRequired && !session) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 px-5 text-slate-100">
        <section className="w-full max-w-md rounded-2xl border border-white/10 bg-white/[0.04] p-6">
          <div className="mb-6">
            <p className="text-sm font-semibold text-cyan-300">Aether GovOS</p>
            <h1 className="mt-2 text-2xl font-bold">Secure workspace</h1>
            <p className="mt-2 text-sm text-slate-400">Sign in before accessing government case data.</p>
          </div>
          <input
            type="email"
            value={authEmail}
            onChange={(e) => setAuthEmail(e.target.value)}
            placeholder="Email"
            className="mb-3 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm"
          />
          <input
            type="password"
            value={authPassword}
            onChange={(e) => setAuthPassword(e.target.value)}
            placeholder="Password"
            className="w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm"
          />
          {authMessage && <p className="mt-3 text-xs text-cyan-200">{authMessage}</p>}
          <button
            onClick={submitAuth}
            disabled={authLoading || !authEmail || !authPassword}
            className="mt-5 w-full rounded-xl bg-cyan-400 px-4 py-3 text-sm font-bold text-slate-950 disabled:opacity-50"
          >
            {authMode === 'signin' ? 'Sign in' : 'Create account'}
          </button>
          <button
            onClick={() => setAuthMode(authMode === 'signin' ? 'signup' : 'signin')}
            className="mt-3 w-full rounded-xl border border-white/10 px-4 py-2 text-xs text-slate-300"
          >
            {authMode === 'signin' ? 'Create a new account' : 'Back to sign in'}
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-5 py-8 lg:px-8">
        <header className="mb-8 flex flex-col gap-4 border-b border-white/10 pb-6 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-cyan-300">
              <Globe2 className="h-4 w-4" /> Aether GovOS
            </div>
            <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
              Tell Aether the outcome. Aether executes the work.
            </h1>
            <p className="mt-2 max-w-3xl text-sm text-slate-400">
              Objective → understanding → requirements → work graph → parallel execution → verification → human authority → outcome.
            </p>
          </div>
          <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-xs text-slate-300">
            <span>MVP mode: synthetic government systems</span>
            {session && (
              <button onClick={signOut} className="rounded-lg border border-white/10 px-2 py-1 text-[10px] hover:bg-white/5">
                Sign out
              </button>
            )}
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-[380px_1fr]">
          <aside className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
            <h2 className="text-lg font-semibold">Start a case</h2>
            <p className="mt-1 text-xs text-slate-400">
              Describe the real-world objective instead of navigating department forms.
            </p>

            <label className="mt-5 block text-xs font-semibold text-slate-300">Objective</label>
            <textarea
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              className="mt-2 h-24 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm outline-none focus:border-cyan-400"
            />

            <label className="mt-4 block text-xs font-semibold text-slate-300">Customer</label>
            <select
              value={customerType}
              onChange={(e) => setCustomerType(e.target.value)}
              className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm"
            >
              <option value="business">Business</option>
              <option value="bank">Bank / Lender</option>
              <option value="developer">Developer</option>
              <option value="insurer">Insurer</option>
              <option value="citizen">Citizen</option>
            </select>

            <div className="mt-4 grid grid-cols-3 gap-2">
              <input value={country} onChange={(e) => setCountry(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
              <input value={state} onChange={(e) => setState(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
              <input value={district} onChange={(e) => setDistrict(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
            </div>

            <div className="mt-4 rounded-xl border border-cyan-300/10 bg-cyan-300/5 p-3 text-[11px] text-cyan-100">
              Demo evidence is supplied automatically so the prototype can exercise the execution engine. Production Aether will collect and verify real documents instead.
            </div>

            <button
              onClick={startCase}
              disabled={loading || !objective.trim()}
              className="mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-4 py-3 text-sm font-bold text-slate-950 disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
              Start Aether execution
            </button>

            {caseData && (
              <button
                onClick={startCase}
                disabled={loading}
                className="mt-2 flex w-full items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold text-slate-200 disabled:opacity-50"
              >
                <RefreshCw className="h-3.5 w-3.5" /> Run another case
              </button>
            )}

            {error && <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/10 p-3 text-xs text-red-200">{error}</div>}
          </aside>

          <section className="space-y-6">
            {!caseData ? (
              <div className="flex min-h-[520px] items-center justify-center rounded-2xl border border-dashed border-white/10 bg-white/[0.02] text-center">
                <div className="max-w-md">
                  <Activity className="mx-auto h-10 w-10 text-cyan-300" />
                  <h2 className="mt-4 text-xl font-semibold">No active case</h2>
                  <p className="mt-2 text-sm text-slate-400">
                    Try a restaurant, property-loan, factory/project, licence, certificate, or other service from the 34-service MVP catalog.
                  </p>
                </div>
              </div>
            ) : (
              <>
                <div className="grid gap-3 sm:grid-cols-5">
                  <Metric label="Service" value={caseData.summary.service_name || 'Unresolved'} />
                  <Metric label="Tasks" value={`${caseData.summary.tasks_completed}/${caseData.summary.tasks_total}`} />
                  <Metric label="Progress" value={`${completedPercent}%`} />
                  <Metric label="Exceptions" value={String(caseData.summary.exceptions)} />
                  <Metric label="Human actions" value={String(caseData.summary.human_actions)} />
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-xs text-slate-500">CASE {caseData.summary.case_id}</p>
                      <h2 className="mt-1 text-xl font-semibold">{caseData.summary.objective}</h2>
                      <p className="mt-1 text-xs text-slate-500">{caseData.summary.service_department || 'Aether'} · critical path: {caseData.summary.critical_path.join(' → ') || 'none'}</p>
                    </div>
                    <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold text-cyan-200">{caseData.summary.status}</span>
                  </div>
                  <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/10">
                    <div className="h-full bg-cyan-400 transition-all" style={{ width: `${completedPercent}%` }} />
                  </div>
                  <div className="mt-4 grid gap-2 text-xs text-slate-400 sm:grid-cols-3">
                    <div>Ready: <span className="text-slate-200">{caseData.summary.ready}</span></div>
                    <div>Waiting: <span className="text-slate-200">{caseData.summary.tasks_waiting}</span></div>
                    <div>Human work remaining: <span className="text-slate-200">{caseData.summary.human_work_remaining} min (demo estimate)</span></div>
                  </div>
                </div>

                {caseData.requirements.length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                    <h3 className="font-semibold">Requirements and evidence</h3>
                    <div className="mt-4 grid gap-2 sm:grid-cols-2">
                      {caseData.requirements.map((r) => (
                        <div key={r.name} className="rounded-xl bg-white/[0.04] p-3">
                          <div className="flex gap-2">
                            <FileText className="h-4 w-4 text-cyan-300" />
                            <span className="text-sm">{r.name}</span>
                          </div>
                          <p className="mt-1 text-[11px] text-slate-500">{r.documents.join(', ') || 'No document input'}</p>
                          {r.source && <p className="mt-2 truncate text-[10px] text-cyan-300/70">Source-backed: {r.source}</p>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                  <h3 className="font-semibold">Aether work graph</h3>
                  <div className="mt-4 grid gap-2 md:grid-cols-2">
                    {tasks.map((task) => <TaskRow key={task.id} task={task} />)}
                  </div>
                </div>

                {caseData.exceptions.length > 0 && (
                  <div className="rounded-2xl border border-amber-300/20 bg-amber-300/5 p-5">
                    <div className="flex items-center gap-2">
                      <CircleAlert className="h-5 w-5 text-amber-300" />
                      <h3 className="font-semibold">Exception detected</h3>
                    </div>
                    {caseData.exceptions.map((e, i) => (
                      <p key={i} className="mt-2 text-sm text-amber-100">{e.message || e.error || e.type || 'Exception'}</p>
                    ))}
                  </div>
                )}

                {caseData.human_actions.length > 0 && (
                  <div className="rounded-2xl border border-violet-300/20 bg-violet-300/5 p-5">
                    <div className="flex items-center gap-2">
                      <UserRound className="h-5 w-5 text-violet-300" />
                      <h3 className="font-semibold">Human authority boundary</h3>
                    </div>
                    {caseData.human_actions.map((action) => (
                      <div key={action.task_id} className="mt-4 flex flex-col gap-3 rounded-xl bg-black/20 p-4 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                          <p className="text-sm font-medium">{action.task}</p>
                          <p className="mt-1 text-xs text-slate-400">{action.reason}</p>
                        </div>
                        <button
                          onClick={() => continueHumanTask(action.task_id)}
                          disabled={loading}
                          className="rounded-lg bg-violet-300 px-4 py-2 text-xs font-bold text-slate-950"
                        >
                          Approve / continue
                        </button>
                      </div>
                    ))}
                  </div>
                )}

                <div className="rounded-2xl border border-emerald-300/20 bg-emerald-300/5 p-5">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="h-5 w-5 text-emerald-300" />
                    <h3 className="font-semibold">Evidence ledger</h3>
                  </div>
                  <p className="mt-2 text-xs text-slate-400">
                    {caseData.evidence.length} evidence entries recorded. Execution events remain auditable on the case.
                  </p>
                </div>
              </>
            )}
          </section>
        </section>
      </div>
    </main>
  );
};

const Metric = ({ label, value }: { label: string; value: string }) => (
  <div className="rounded-xl border border-white/10 bg-white/[0.04] p-4">
    <p className="text-[11px] uppercase tracking-wide text-slate-500">{label}</p>
    <p className="mt-1 truncate text-xl font-bold">{value}</p>
  </div>
);

const TaskRow = ({ task }: { task: Task }) => {
  const done = task.status === 'completed';
  const human = task.status === 'human_review';
  const exception = task.status === 'exception';
  return (
    <div className="rounded-xl border border-white/5 bg-black/10 p-3">
      <div className="flex items-start gap-3">
        {done
          ? <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-300" />
          : exception
            ? <CircleAlert className="mt-0.5 h-4 w-4 shrink-0 text-amber-300" />
            : human
              ? <UserRound className="mt-0.5 h-4 w-4 shrink-0 text-violet-300" />
              : <Activity className="mt-0.5 h-4 w-4 shrink-0 text-cyan-300" />}
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium">{task.name}</p>
          <p className="mt-1 text-[11px] text-slate-500">{task.department} · {task.worker} · attempts {task.attempts ?? 0}</p>
        </div>
        <span className="text-[10px] uppercase text-slate-500">{task.status.replace('_', ' ')}</span>
      </div>
    </div>
  );
};
