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

type Understanding = {
  service_id?: string | null;
  service_name?: string | null;
  confidence: number;
  matched_keywords: string[];
  candidates: Array<{
    service_id: string;
    service_name: string;
    department: string;
    score: number;
    matched_keywords: string[];
  }>;
  ambiguous: boolean;
  missing_context: string[];
};

type CaseListItem = CaseResponse['summary'];

type Principal = {
  subject: string;
  role: string;
  tenant_id?: string | null;
  department?: string | null;
  jurisdiction?: Record<string, string>;
  auth_mode: string;
};

type TenantOption = {
  tenant_id: string;
  role: string;
  department?: string | null;
  jurisdiction?: Record<string, string>;
};

type OperatorBrief = {
  summary: {
    automated_completed: number;
    automation_eligible_total: number;
    human_or_physical_total: number;
    exceptions: number;
    blocked: number;
    waiting: number;
    employee_attention_required: number;
  };
  time: {
    estimated_admin_minutes_if_manual: number;
    estimated_aether_admin_minutes: number;
    estimated_minutes_saved: number;
    note: string;
  };
  attention_items: Array<{ priority: string; type: string; task_id?: string | null; title: string; action: string }>;
  next_best_actions: Array<{ priority: number; type: string; task_id?: string | null; owner: string; action: string }>;
  customer_actions: Array<{ type: string; document: string; action: string }>;
  revenue_signals: Array<{ type: string; status: string; action: string }>;
  friction?: {
    citizen_effort_score: number;
    employee_effort_score: number;
    friction_sources: Array<{ type: string; impact: string; count: number; aether_action: string }>;
    recovery_plan: {
      recovery_required: boolean;
      retry_tasks: string[];
      replan_tasks: string[];
      preserve_case_state: boolean;
      preserve_verified_evidence: boolean;
      ask_user_to_reenter_data: boolean;
      compare_only_changed_inputs: boolean;
    };
    bottleneck?: {
      top_bucket: string;
      counts: Record<string, number>;
      tasks: Array<{ task_id: string; owner: string; reason: string }>;
      user_message: string;
    };
  };
  process?: {
    profile: string;
    label: string;
    employee_work_recipe: string[];
    work_atoms: Record<string, { label: string; automation: string; human_boundary: boolean }>;
    journey_playbook?: {
      stages: string[];
      employee_work: string[];
      parallelizable: string[];
      citizen_wait_points: string[];
      human_boundary: string[];
    };
  };
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
  understanding?: Understanding;
  human_actions: Array<{ task_id: string; task: string; reason: string }>;
  exceptions: Array<{ type?: string; severity?: string; message?: string; error?: string }>;
  evidence: Array<{ source: string; request_id?: string; operation?: string }>;
  tasks: Record<string, Omit<Task, 'id'>> | Task[];
  outcome?: Record<string, unknown> | null;
  execution_events?: Array<{
    sequence?: number;
    timestamp?: string;
    action: string;
    actor?: string;
  }>;
  operator?: OperatorBrief;
  documents?: Array<{
    document_id: string;
    document_type: string;
    filename: string;
    mime_type: string;
    size_bytes: number;
    sha256: string;
    extraction_mode: string;
    created_at?: string | null;
  }>;
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
  const [preflightSimulation, setPreflightSimulation] = useState<{
    status: string;
    blockers: Array<{ code: string; document_type?: string; fields?: string[]; message: string }>;
    warnings: Array<{ code: string; message: string }>;
    next_steps: string[];
  } | null>(null);
  const [understanding, setUnderstanding] = useState<Understanding | null>(null);
  const [recentCases, setRecentCases] = useState<CaseListItem[]>([]);
  const [officerQueue, setOfficerQueue] = useState<CaseListItem[]>([]);
  const [operatorWorkload, setOperatorWorkload] = useState<{
    case_count: number;
    workload: {
      departments: Array<{
        department: string;
        active_work: number;
        pending: number;
        running: number;
        human_review: number;
        exceptions: number;
        management_attention: string;
      }>;
      critical_cases: Array<{
        case_id: string;
        status: string;
        exceptions: number;
        human_actions: number;
      }>;
    };
  } | null>(null);
  const [operatorBatches, setOperatorBatches] = useState<Array<{
    batch_key: string;
    task_id: string;
    owner: string;
    case_count: number;
    suggested_action: string;
  }>>([]);
  const [apiKeys, setApiKeys] = useState<Array<{ key_prefix: string; role: string; scopes: string[]; status: string; created_at?: string | null }>>([]);
  const [newApiKey, setNewApiKey] = useState('');
  const [notifications, setNotifications] = useState<Array<{ id: number; event_type: string; case_id?: string | null; status: string; created_at?: string | null }>>([]);
  const [marketplace, setMarketplace] = useState<Array<{ service_id: string; name: string; department: string; outcome: string; sandbox: boolean }>>([]);
  const [analytics, setAnalytics] = useState<{ case_count: number; completion_rate: number; human_actions_pending: number; exceptions: number } | null>(null);
  const [payments, setPayments] = useState<Array<{ payment_id: string; amount_minor: number; currency: string; provider: string; status: string; created_at?: string | null }>>([]);
  const [tenantOptions, setTenantOptions] = useState<TenantOption[]>([]);
  const [selectedTenantId, setSelectedTenantId] = useState('');
  const [paymentAmount, setPaymentAmount] = useState('0');
  const [paymentMessage, setPaymentMessage] = useState('');
  const [humanNotes, setHumanNotes] = useState<Record<string, string>>({});
  const [principal, setPrincipal] = useState<Principal | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authMode, setAuthMode] = useState<'signin' | 'signup'>('signin');
  const [authMessage, setAuthMessage] = useState('');
  const [useDemoEvidence, setUseDemoEvidence] = useState(true);
  const [missingDocuments, setMissingDocuments] = useState<string[]>([]);
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [uploadDocumentType, setUploadDocumentType] = useState('');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [intakeNotice, setIntakeNotice] = useState('');
  const { session, loading: authLoading, required: authRequired, signIn, signUp, signOut } = useAuth();

  React.useEffect(() => {
    if (session?.access_token) {
      const storedTenant = window.localStorage.getItem('aether.tenant_id') || '';
      setSelectedTenantId(storedTenant);
    }
  }, [session?.access_token]);

  React.useEffect(() => {
    if (!authRequired || session) {
      loadWorkspace();
    }
  }, [authRequired, session?.access_token, selectedTenantId]);

  async function simulateProcess() {
    try {
      const response = await fetch(API_BASE + '/api/aether/v2/process/simulate', {
        method: 'POST',
        headers: { ...authHeaders(), 'Content-Type': 'application/json' },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country, state, district },
          inputs: { documents: selectedDocuments },
        }),
      });
      if (!response.ok) return;
      setPreflightSimulation(await response.json());
    } catch {
      // Dry-run is optional; case creation remains available.
    }
  }

  async function loadWorkspace() {
    try {
      const response = await fetch(API_BASE + '/api/aether/v2/me', {
        headers: authHeaders(),
      });
      if (response.status === 409) {
        const body = await response.json().catch(() => ({}));
        const detail = body.detail;
        if (detail?.code === 'multiple_active_memberships') {
          setTenantOptions(Array.isArray(detail.memberships) ? detail.memberships : []);
          setPrincipal(null);
          setRecentCases([]);
          return;
        }
      }
      if (response.status === 403 && selectedTenantId) {
        setSelectedTenantId('');
        window.localStorage.removeItem('aether.tenant_id');
        return;
      }
      if (!response.ok) return;
      const body = await response.json() as Principal;
      setPrincipal(body);
      setTenantOptions([]);
      await loadRecentCases();

      const keyReadRoles = ['user', 'citizen', 'business', 'bank', 'developer', 'insurer', 'enterprise', 'admin'];
      if (keyReadRoles.includes(body.role.toLowerCase())) {
        const keysResponse = await fetch(API_BASE + '/api/aether/v2/api-keys', {
          headers: authHeaders(),
        });
        if (keysResponse.ok) {
          const keysBody = await keysResponse.json();
          setApiKeys(keysBody.keys || []);
        }
        const notificationResponse = await fetch(API_BASE + '/api/aether/v2/notifications', {
          headers: authHeaders(),
        });
        if (notificationResponse.ok) {
          const notificationBody = await notificationResponse.json();
          setNotifications((notificationBody.notifications || []).slice(0, 6));
        }

        const marketplaceResponse = await fetch(API_BASE + '/api/aether/v2/marketplace', {
          headers: authHeaders(),
        });
        if (marketplaceResponse.ok) {
          const marketplaceBody = await marketplaceResponse.json();
          setMarketplace((marketplaceBody.apis || []).slice(0, 12));
        }
      }

      const operator = ['officer', 'department_admin', 'admin'].includes(body.role.toLowerCase());
      if (!operator) {
        setOfficerQueue([]);
        setAnalytics(null);
        return;
      }

      const analyticsResponse = await fetch(API_BASE + '/api/aether/v2/analytics', {
        headers: authHeaders(),
      });
      if (analyticsResponse.ok) {
        setAnalytics(await analyticsResponse.json());
      }

      const queueResponse = await fetch(
        API_BASE + '/api/aether/v2/cases?status=waiting_for_human&limit=12',
        { headers: authHeaders() }
      );
      if (queueResponse.ok) {
        const queueBody = await queueResponse.json();
        setOfficerQueue(queueBody.cases || []);
      }

      const workloadResponse = await fetch(
        API_BASE + '/api/aether/v2/operator/workload?limit=100',
        { headers: authHeaders() }
      );
      if (workloadResponse.ok) {
        setOperatorWorkload(await workloadResponse.json());
      }

      const batchesResponse = await fetch(
        API_BASE + '/api/aether/v2/operator/batches?limit=12',
        { headers: authHeaders() }
      );
      if (batchesResponse.ok) {
        const batchesBody = await batchesResponse.json();
        setOperatorBatches(batchesBody.batches || []);
      }
    } catch {
      // The command center remains usable even when workspace metadata is unavailable.
    }
  }

  const completedPercent = useMemo(() => {
    if (!caseData?.summary.tasks_total) return 0;
    return Math.round((caseData.summary.tasks_completed / caseData.summary.tasks_total) * 100);
  }, [caseData]);

  const authHeaders = () => {
    if (!session?.access_token) return {};
    return {
      Authorization: `Bearer ${session.access_token}`,
      ...(selectedTenantId ? { 'X-Aether-Tenant-ID': selectedTenantId } : {}),
    };
  };

  const tenantSelectionRequired = tenantOptions.length > 1 && !selectedTenantId;

  function selectTenant(tenantId: string) {
    setSelectedTenantId(tenantId);
    setCaseData(null);
    setUnderstanding(null);
    setMissingDocuments([]);
    setSelectedDocuments([]);
    setIntakeNotice('');
    setError('');
    if (tenantId) {
      window.localStorage.setItem('aether.tenant_id', tenantId);
    } else {
      window.localStorage.removeItem('aether.tenant_id');
    }
  }

  async function loadRecentCases() {
    try {
      const params = new URLSearchParams({ limit: '12' });
      const response = await fetch(`${API_BASE}/api/aether/v2/cases?${params.toString()}`, {
        headers: authHeaders(),
      });
      if (!response.ok) return;
      const body = await response.json();
      setRecentCases(body.cases || []);
    } catch {
      // The active case remains usable when case history cannot be loaded.
    }
  }

  async function analyzeObjective() {
    setError('');
    try {
      const response = await fetch(`${API_BASE}/api/aether/v2/understand`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country, state, district },
          inputs: {},
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Understanding returned ${response.status}`);
      setUnderstanding(body);
      if (body.ambiguous) {
        setError('Aether found more than one plausible service. Choose a clearer objective before execution.');
      }
      return body as Understanding;
    } catch (err) {
      setUnderstanding(null);
      setError(err instanceof Error ? err.message : 'Unable to understand objective');
      return null;
    }
  }

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
      const analyzed = await analyzeObjective();
      if (!analyzed || analyzed.ambiguous || !analyzed.service_id) return;
      const response = await fetch(`${API_BASE}/api/aether/v2/cases`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country, state, district },
          inputs: {
            documents: useDemoEvidence ? DEMO_DOCUMENTS : selectedDocuments,
            owner_name: 'Demo Owner',
            parcel_id: 'PARCEL-DEMO-001',
            property_id: 'PROPERTY-DEMO-001',
            company_id: 'COMPANY-DEMO-001',
            project_id: 'PROJECT-DEMO-001',
            demo_mode: useDemoEvidence,
          },
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Aether API returned ${response.status}`);
      setCaseData(body);
      setUnderstanding(body.understanding || analyzed);
      setMissingDocuments(body.missing_documents || []);
      setSelectedDocuments([]);
      setIntakeNotice(
        body.status === 'needs_documents'
          ? 'Aether created a durable intake case. Supply the missing document types to continue.'
          : ''
      );
      await loadRecentCases();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to start Aether case');
    } finally {
      setLoading(false);
    }
  }

  async function refreshIntake(caseId: string) {
    const response = await fetch(
      API_BASE + '/api/aether/v2/cases/' + caseId + '/intake',
      { headers: authHeaders() }
    );
    if (!response.ok) return;
    const body = await response.json();
    setMissingDocuments(body.missing_documents || []);
  }

  async function uploadDocument() {
    if (!caseData || !uploadDocumentType || !uploadFile) return;
    setLoading(true);
    setError('');
    try {
      const form = new FormData();
      form.append('document_type', uploadDocumentType);
      form.append('file', uploadFile);
      const response = await fetch(
        API_BASE + '/api/aether/v2/cases/' + caseData.summary.case_id + '/documents/upload?document_type=' + encodeURIComponent(uploadDocumentType),
        {
          method: 'POST',
          headers: authHeaders(),
          body: form,
        }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'Document upload failed');
      setCaseData(body.case || caseData);
      setUploadDocumentType('');
      setUploadFile(null);
      setIntakeNotice('Document uploaded and hashed successfully.');
      await refreshIntake(caseData.summary.case_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to upload document');
    } finally {
      setLoading(false);
    }
  }

  async function createApiKey() {
    setLoading(true);
    setError('');
    setNewApiKey('');
    try {
      const response = await fetch(API_BASE + '/api/aether/v2/api-keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({
          role: 'developer',
          scopes: ['cases:read', 'cases:write', 'documents:read', 'documents:write', 'payments:read', 'payments:write', 'analytics:read'],
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'API key creation failed');
      setNewApiKey(body.key || '');
      await loadWorkspace();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create API key');
    } finally {
      setLoading(false);
    }
  }

  async function revokeApiKey(keyPrefix: string) {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(
        API_BASE + '/api/aether/v2/api-keys/' + encodeURIComponent(keyPrefix) + '/revoke',
        { method: 'POST', headers: authHeaders() }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'API key revocation failed');
      await loadWorkspace();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to revoke API key');
    } finally {
      setLoading(false);
    }
  }

  async function submitDocuments() {
    if (!caseData || selectedDocuments.length === 0) return;
    setLoading(true);
    setError('');
    try {
      const response = await fetch(
        `${API_BASE}/api/aether/v2/cases/${caseData.summary.case_id}/documents`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...authHeaders() },
          body: JSON.stringify({ documents: selectedDocuments }),
        }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Document submission returned ${response.status}`);
      setCaseData(body);
      setMissingDocuments(body.missing_documents || []);
      await loadPayments(caseData.summary.case_id);
      setSelectedDocuments([]);
      setIntakeNotice(
        body.status === 'needs_documents'
          ? 'Some required evidence is still missing.'
          : 'Required intake evidence recorded. Aether continued the case.'
      );
      await loadRecentCases();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to submit documents');
    } finally {
      setLoading(false);
    }
  }

  async function openCase(caseId: string) {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/api/aether/v2/cases/${caseId}`, {
        headers: authHeaders(),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || `Case returned ${response.status}`);
      setCaseData(body);
      setUnderstanding(body.understanding || null);
      await loadPayments(caseId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to reopen case');
    } finally {
      setLoading(false);
    }
  }

  async function loadPayments(caseId: string) {
    try {
      const response = await fetch(
        API_BASE + '/api/aether/v2/cases/' + caseId + '/payments',
        { headers: authHeaders() }
      );
      if (!response.ok) return;
      const body = await response.json();
      setPayments(body.payments || []);
    } catch {
      // Payment history is optional for the active case.
    }
  }

  async function createPayment() {
    if (!caseData) return;
    const amount = Math.round(Number(paymentAmount) * 100);
    if (!Number.isFinite(amount) || amount <= 0) {
      setPaymentMessage('Enter a positive INR amount.');
      return;
    }
    setLoading(true);
    setError('');
    setPaymentMessage('');
    try {
      const key = caseData.summary.case_id + ':mvp-payment:' + amount;
      const response = await fetch(
        API_BASE + '/api/aether/v2/cases/' + caseData.summary.case_id
          + '/payments?amount_minor=' + amount
          + '&currency=INR&idempotency_key=' + encodeURIComponent(key),
        { method: 'POST', headers: authHeaders() }
      );
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'Payment creation failed');
      setPaymentMessage(
        'Payment ' + body.status + ' via ' + body.provider + ' · ' + body.payment_id
      );
      await loadPayments(caseData.summary.case_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create payment');
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
          body: JSON.stringify({
            approved,
            note: humanNotes[taskId] || (approved ? 'Approved by authorised operator.' : 'Rejected by authorised operator.'),
          }),
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
            type="button"
            onClick={simulateProcess}
            disabled={!objective.trim() || loading}
            className="mr-2 rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-[10px] font-semibold text-cyan-100 hover:bg-cyan-300/15 disabled:opacity-50"
          >
            Pre-check journey
          </button>
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
            {tenantOptions.length > 1 && (
              <select
                value={selectedTenantId}
                onChange={(e) => selectTenant(e.target.value)}
                className="max-w-56 rounded-lg border border-white/10 bg-slate-900 px-2 py-1 text-[10px] text-slate-200"
              >
                <option value="">Select tenant/workspace</option>
                {tenantOptions.map((tenant) => (
                  <option key={tenant.tenant_id} value={tenant.tenant_id}>
                    {tenant.tenant_id} · {tenant.role}
                  </option>
                ))}
              </select>
            )}
            {principal && (
              <span className="rounded-full border border-cyan-300/20 bg-cyan-300/5 px-2 py-1 text-cyan-200">
                {principal.role.replace('_', ' ')}{principal.department ? ' · ' + principal.department : ''}
              </span>
            )}
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

            <button
              onClick={analyzeObjective}
              disabled={loading || !objective.trim() || tenantSelectionRequired}
              className="mt-4 w-full rounded-xl border border-cyan-300/20 bg-cyan-300/5 px-4 py-2 text-xs font-semibold text-cyan-100 disabled:opacity-50"
            >
              Understand objective first
            </button>

            {understanding && (
              <div className="mt-3 rounded-xl border border-white/10 bg-black/10 p-3 text-[11px]">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-slate-400">Aether understanding</span>
                  <span className="font-semibold text-cyan-200">
                    {Math.round(understanding.confidence * 100)}% confidence
                  </span>
                </div>
                <p className="mt-1 text-sm font-semibold text-white">
                  {understanding.service_name || 'Needs clarification'}
                </p>
                {understanding.candidates.length > 1 && (
                  <div className="mt-2 space-y-1 text-slate-400">
                    {understanding.candidates.slice(0, 3).map((candidate) => (
                      <div key={candidate.service_id} className="flex justify-between gap-2">
                        <span className="truncate">{candidate.service_name}</span>
                        <span>{candidate.score}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

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
              <option value="enterprise">Enterprise</option>
              <option value="citizen">Citizen</option>
            </select>

            <div className="mt-4 grid grid-cols-3 gap-2">
              <input value={country} onChange={(e) => setCountry(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
              <input value={state} onChange={(e) => setState(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
              <input value={district} onChange={(e) => setDistrict(e.target.value)} className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs" />
            </div>

            <label className="mt-4 flex items-center gap-2 text-xs text-slate-300">
              <input
                type="checkbox"
                checked={useDemoEvidence}
                onChange={(e) => {
                  setUseDemoEvidence(e.target.checked);
                  if (e.target.checked) {
                    setSelectedDocuments([]);
                    setMissingDocuments([]);
                    setIntakeNotice('');
                  }
                }}
                className="h-4 w-4 rounded border-white/20 bg-slate-900"
              />
              Use demo evidence for a full synthetic run
            </label>
            <div className="mt-3 rounded-xl border border-cyan-300/10 bg-cyan-300/5 p-3 text-[11px] text-cyan-100">
              {useDemoEvidence
                ? 'Demo mode supplies synthetic document types so the execution graph can be exercised end-to-end.'
                : 'Guided intake mode creates the real case first and lets you record required document types before Aether executes.'}
            </div>

            <button
              onClick={startCase}
              disabled={loading || !objective.trim() || tenantSelectionRequired}
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

            {intakeNotice && <div className="mt-4 rounded-xl border border-cyan-300/20 bg-cyan-300/5 p-3 text-xs text-cyan-100">{intakeNotice}</div>}
            {error && <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/10 p-3 text-xs text-red-200">{error}</div>}

            {(principal && ['user', 'citizen', 'business', 'bank', 'developer', 'insurer', 'enterprise', 'admin'].includes(principal.role.toLowerCase())) && (
              <div className="mt-6 border-t border-white/10 pt-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-300">Developer access</h3>
                  <button
                    onClick={createApiKey}
                    disabled={loading}
                    className="rounded-lg border border-cyan-300/20 px-2 py-1 text-[10px] font-semibold text-cyan-200 disabled:opacity-50"
                  >
                    Create API key
                  </button>
                </div>
                {newApiKey && (
                  <div className="mt-2 rounded-lg border border-amber-300/20 bg-amber-300/5 p-2">
                    <p className="text-[9px] text-amber-100">Copy this key now. It will not be shown again.</p>
                    <div className="mt-1 break-all font-mono text-[9px] text-slate-200">{newApiKey}</div>
                    <button
                      onClick={() => navigator.clipboard?.writeText(newApiKey)}
                      className="mt-2 rounded border border-white/10 px-2 py-1 text-[9px] text-slate-300"
                    >
                      Copy key
                    </button>
                  </div>
                )}
                <div className="mt-2 space-y-2">
                  {apiKeys.length === 0 ? (
                    <p className="text-[10px] text-slate-500">No developer keys.</p>
                  ) : apiKeys.slice(0, 4).map((key) => (
                    <div key={key.key_prefix} className="flex items-center justify-between gap-2 rounded-lg border border-white/5 bg-black/10 p-2">
                      <div className="min-w-0">
                        <div className="truncate font-mono text-[9px] text-slate-200">{key.key_prefix}… · {key.status}</div>
                        <div className="mt-1 text-[8px] text-slate-500">{key.scopes.join(', ')}</div>
                      </div>
                      {key.status === 'active' && (
                        <button onClick={() => revokeApiKey(key.key_prefix)} className="shrink-0 text-[9px] text-red-300">
                          Revoke
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {marketplace.length > 0 && (
              <div className="mt-6 border-t border-white/10 pt-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-300">Developer API marketplace</h3>
                  <span className="text-[9px] text-cyan-200/70">{marketplace.length} services</span>
                </div>
                <div className="mt-2 space-y-2">
                  {marketplace.slice(0, 5).map((api) => (
                    <div key={api.service_id} className="rounded-lg border border-white/5 bg-black/10 p-2">
                      <div className="truncate text-[10px] font-medium text-slate-200">{api.name}</div>
                      <div className="mt-1 text-[8px] text-slate-500">{api.department} · sandbox API · {api.outcome}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {analytics && (
              <div className="mt-6 border-t border-white/10 pt-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-300">Officer analytics</h3>
                  <span className="text-[9px] text-slate-500">{analytics.case_count} cases</span>
                </div>
                <div className="mt-2 grid grid-cols-3 gap-2 text-[9px]">
                  <div className="rounded-lg bg-black/10 p-2"><span className="text-slate-500">Complete</span><div className="mt-1 font-bold text-cyan-200">{analytics.completion_rate}%</div></div>
                  <div className="rounded-lg bg-black/10 p-2"><span className="text-slate-500">Human</span><div className="mt-1 font-bold text-violet-200">{analytics.human_actions_pending}</div></div>
                  <div className="rounded-lg bg-black/10 p-2"><span className="text-slate-500">Exceptions</span><div className="mt-1 font-bold text-amber-200">{analytics.exceptions}</div></div>
                </div>
              </div>
            )}

            <div className="mt-6 border-t border-white/10 pt-5">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-semibold text-slate-300">Recent cases</h3>
                <button onClick={loadRecentCases} className="text-[10px] text-cyan-300 hover:text-cyan-200">Refresh</button>
              </div>
              {officerQueue.length > 0 && (
                <div className="mt-4 rounded-xl border border-violet-300/15 bg-violet-300/5 p-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[11px] font-semibold text-violet-100">Authority queue</h3>
                    <span className="text-[10px] text-violet-200">{officerQueue.length} waiting</span>
                  </div>
                  <div className="mt-2 space-y-2">
                    {officerQueue.slice(0, 4).map((item) => (
                      <button
                        key={item.case_id}
                        onClick={() => openCase(item.case_id)}
                        className="w-full rounded-lg border border-violet-300/10 bg-black/10 p-2 text-left hover:border-violet-300/20"
                      >
                        <div className="truncate text-[11px] font-medium text-violet-50">{item.service_name || item.objective}</div>
                        <div className="mt-1 text-[9px] text-violet-200/70">{item.human_actions || 0} action(s) · {item.case_id}</div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {operatorWorkload && (
                <div className="mt-4 rounded-xl border border-emerald-300/15 bg-emerald-300/5 p-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[11px] font-semibold text-emerald-100">Workload control tower</h3>
                    <span className="text-[9px] text-emerald-200">{operatorWorkload.case_count} cases</span>
                  </div>
                  <div className="mt-2 grid grid-cols-2 gap-2">
                    {operatorWorkload.workload.departments.slice(0, 4).map((item) => (
                      <div key={item.department} className="rounded-lg bg-black/10 p-2">
                        <div className="truncate text-[9px] font-medium text-slate-300">{item.department}</div>
                        <div className="mt-1 text-sm font-bold text-emerald-200">{item.active_work}</div>
                        <div className="text-[8px] text-slate-500">{item.management_attention} attention</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {operatorBatches.length > 0 && (
                <div className="mt-3 rounded-xl border border-cyan-300/15 bg-cyan-300/5 p-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[11px] font-semibold text-cyan-100">Batch opportunities</h3>
                    <span className="text-[9px] text-cyan-200">{operatorBatches.length}</span>
                  </div>
                  <div className="mt-2 space-y-2">
                    {operatorBatches.slice(0, 3).map((batch) => (
                      <div key={batch.batch_key} className="rounded-lg border border-white/5 bg-black/10 p-2">
                        <div className="flex items-center justify-between gap-2">
                          <span className="truncate text-[9px] font-medium text-slate-200">{batch.task_id.replaceAll('_', ' ')}</span>
                          <span className="text-[9px] text-emerald-200">{batch.case_count} cases</span>
                        </div>
                        <p className="mt-1 text-[8px] text-slate-500">{batch.suggested_action}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-2 space-y-2">
                {recentCases.length === 0 ? (
                  <p className="text-[11px] text-slate-500">No saved cases yet.</p>
                ) : recentCases.slice(0, 6).map((item) => (
                  <button
                    key={item.case_id}
                    onClick={() => openCase(item.case_id)}
                    className="w-full rounded-lg border border-white/5 bg-black/10 p-2 text-left hover:border-white/10"
                  >
                    <div className="truncate text-[11px] font-medium text-slate-200">{item.service_name || item.objective}</div>
                    <div className="mt-1 flex justify-between gap-2 text-[9px] text-slate-500">
                      <span>{item.status.replace('_', ' ')}</span>
                      <span>{item.case_id}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
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
                      {understanding?.matched_keywords?.length ? (
                        <p className="mt-1 text-[10px] text-cyan-300/70">Matched: {understanding.matched_keywords.join(', ')}</p>
                      ) : null}
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

                {caseData.operator?.friction?.bottleneck && (
                  <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                    <p className="text-[10px] uppercase tracking-[0.18em] text-slate-500">What happens next</p>
                    <p className="mt-2 text-sm font-medium text-slate-200">
                      {caseData.operator.friction.bottleneck.user_message}
                    </p>
                    <p className="mt-1 text-[10px] text-slate-500">
                      Aether keeps the case state and verified work intact; you do not restart the process.
                    </p>
                  </div>
                )}

                {caseData.operator && (
                  <div className="rounded-2xl border border-emerald-300/20 bg-emerald-300/5 p-5">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <div className="flex items-center gap-2">
                          <ShieldCheck className="h-5 w-5 text-emerald-300" />
                          <h3 className="font-semibold">Employee work automation</h3>
                        </div>
                        <p className="mt-1 text-xs text-slate-400">
                          Aether handles routine case work automatically and surfaces only the work that still needs a person.
                        </p>
                      </div>
                      <span className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-2.5 py-1 text-[10px] font-semibold text-emerald-200">
                        {caseData.operator.time.estimated_minutes_saved} min estimated saved
                      </span>
                    </div>

                    <div className="mt-4 grid gap-2 sm:grid-cols-4">
                      <div className="rounded-xl bg-black/10 p-3">
                        <p className="text-[10px] uppercase tracking-wide text-slate-500">Automated</p>
                        <p className="mt-1 text-lg font-bold text-emerald-200">{caseData.operator.summary.automated_completed}</p>
                      </div>
                      <div className="rounded-xl bg-black/10 p-3">
                        <p className="text-[10px] uppercase tracking-wide text-slate-500">Human / physical</p>
                        <p className="mt-1 text-lg font-bold text-violet-200">{caseData.operator.summary.human_or_physical_total}</p>
                      </div>
                      <div className="rounded-xl bg-black/10 p-3">
                        <p className="text-[10px] uppercase tracking-wide text-slate-500">Exceptions</p>
                        <p className="mt-1 text-lg font-bold text-amber-200">{caseData.operator.summary.exceptions}</p>
                      </div>
                      <div className="rounded-xl bg-black/10 p-3">
                        <p className="text-[10px] uppercase tracking-wide text-slate-500">Employee attention</p>
                        <p className="mt-1 text-lg font-bold text-cyan-200">{caseData.operator.summary.employee_attention_required}</p>
                      </div>
                    </div>

                    {caseData.operator.friction && (
                      <div className="mt-5 rounded-xl border border-fuchsia-300/10 bg-fuchsia-300/5 p-3">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div>
                            <p className="text-[11px] font-semibold text-fuchsia-100">Friction eliminated</p>
                            <p className="mt-1 text-[10px] text-fuchsia-100/70">
                              Aether targets repeat visits, rework, cross-department waiting and portal failures.
                            </p>
                          </div>
                          <span className="text-[9px] uppercase tracking-wide text-fuchsia-100/60">
                            {caseData.operator.friction.friction_sources.length} active signal(s)
                          </span>
                        </div>
                        <div className="mt-3 grid gap-2 sm:grid-cols-3">
                          <div className="rounded-lg bg-black/10 p-2.5">
                            <p className="text-[9px] uppercase tracking-wide text-slate-500">Citizen effort</p>
                            <p className="mt-1 text-base font-bold text-fuchsia-200">{caseData.operator.friction.citizen_effort_score}/100</p>
                          </div>
                          <div className="rounded-lg bg-black/10 p-2.5">
                            <p className="text-[9px] uppercase tracking-wide text-slate-500">Employee effort</p>
                            <p className="mt-1 text-base font-bold text-cyan-200">{caseData.operator.friction.employee_effort_score}/100</p>
                          </div>
                          <div className="rounded-lg bg-black/10 p-2.5">
                            <p className="text-[9px] uppercase tracking-wide text-slate-500">Restart user data</p>
                            <p className="mt-1 text-base font-bold text-emerald-200">
                              {caseData.operator.friction.recovery_plan.ask_user_to_reenter_data ? 'No' : 'Never'}
                            </p>
                          </div>
                        </div>
                        {caseData.operator.friction.bottleneck && (
                          <div className="mt-3 rounded-lg border border-white/5 bg-black/10 px-2.5 py-2">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                              <p className="text-[10px] font-medium text-slate-200">Current bottleneck</p>
                              <span className="rounded-full bg-white/5 px-2 py-1 text-[8px] uppercase tracking-wide text-slate-400">
                                {caseData.operator.friction.bottleneck.top_bucket.replaceAll('_', ' ')}
                              </span>
                            </div>
                            <p className="mt-1 text-[9px] text-slate-400">{caseData.operator.friction.bottleneck.user_message}</p>
                          </div>
                        )}

                        {caseData.operator.friction.friction_sources.slice(0, 3).map((signal, index) => (
                          <div key={signal.type + index} className="mt-2 rounded-lg border border-white/5 bg-black/10 px-2.5 py-2">
                            <p className="text-[10px] font-medium text-slate-200">{signal.type.replaceAll('_', ' ')}</p>
                            <p className="mt-0.5 text-[9px] text-slate-400">{signal.aether_action}</p>
                          </div>
                        ))}
                      </div>
                    )}

                    {caseData.operator.process && (
                      <div className="mt-5 rounded-xl border border-cyan-300/10 bg-cyan-300/5 p-3">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div>
                            <p className="text-[11px] font-semibold text-cyan-100">Government process recipe</p>
                            <p className="mt-1 text-[10px] text-cyan-100/70">
                              {caseData.operator.process.label} · {caseData.operator.process.profile}
                            </p>
                          </div>
                          <span className="text-[9px] uppercase tracking-wide text-cyan-100/60">
                            {caseData.operator.process.employee_work_recipe.length} work atoms
                          </span>
                        </div>
                        {caseData.operator.process.journey_playbook && (
                          <div className="mt-3">
                            <p className="text-[9px] uppercase tracking-wide text-slate-500">Journey stages</p>
                            <div className="mt-2 flex flex-wrap items-center gap-1">
                              {caseData.operator.process.journey_playbook.stages.map((stage, index) => (
                                <React.Fragment key={stage + index}>
                                  <span className="rounded-full border border-white/10 bg-black/10 px-2 py-1 text-[8px] text-slate-300">
                                    {stage}
                                  </span>
                                  {index < caseData.operator.process.journey_playbook!.stages.length - 1 && (
                                    <ArrowRight className="h-3 w-3 text-slate-600" />
                                  )}
                                </React.Fragment>
                              ))}
                            </div>
                          </div>
                        )}

                        <div className="mt-3 flex flex-wrap gap-1.5">
                          {caseData.operator.process.employee_work_recipe.slice(0, 8).map((atom) => (
                            <span key={atom} className="rounded-full border border-white/10 bg-black/10 px-2 py-1 text-[9px] text-slate-300">
                              {caseData.operator.process.work_atoms[atom]?.label || atom}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {caseData.operator.next_best_actions.length > 0 && (
                      <div className="mt-5">
                        <p className="text-[11px] font-semibold text-slate-300">Next best actions</p>
                        <div className="mt-2 space-y-2">
                          {caseData.operator.next_best_actions.slice(0, 5).map((action, index) => (
                            <div key={(action.task_id || 'action') + index} className="rounded-xl border border-white/5 bg-black/10 p-3">
                              <div className="flex flex-wrap items-center justify-between gap-2">
                                <span className="text-xs font-medium text-slate-200">{action.action}</span>
                                <span className="text-[9px] uppercase tracking-wide text-slate-500">{action.owner}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {caseData.operator.customer_actions.length > 0 && (
                      <div className="mt-5 rounded-xl border border-amber-300/15 bg-amber-300/5 p-3">
                        <p className="text-[11px] font-semibold text-amber-100">Customer action required</p>
                        <p className="mt-1 text-[10px] text-amber-100/70">
                          {caseData.operator.customer_actions.length} document action(s) remain.
                        </p>
                      </div>
                    )}

                    {caseData.operator.revenue_signals.length > 0 && (
                      <div className="mt-4 rounded-xl border border-cyan-300/15 bg-cyan-300/5 p-3">
                        <p className="text-[11px] font-semibold text-cyan-100">Government value signal</p>
                        {caseData.operator.revenue_signals.map((signal, index) => (
                          <p key={signal.type + index} className="mt-1 text-[10px] text-cyan-100/80">{signal.action}</p>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {caseData.summary.status === 'needs_documents' && missingDocuments.length > 0 && (
                  <div className="rounded-2xl border border-amber-300/20 bg-amber-300/5 p-5">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h3 className="font-semibold">Guided document intake</h3>
                        <p className="mt-1 text-xs text-slate-400">
                          Select the document types you have supplied. Aether records intake metadata, supports real file upload, and uses extracted text in the document worker when available.
                        </p>
                      </div>
                      <span className="text-xs text-amber-200">{missingDocuments.length} missing</span>
                    </div>
                    <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                      {missingDocuments.map((document) => (
                        <label key={document} className="flex items-center gap-2 rounded-lg border border-white/10 bg-black/10 p-2 text-xs">
                          <input
                            type="checkbox"
                            checked={selectedDocuments.includes(document)}
                            onChange={(e) => {
                              setSelectedDocuments((current) =>
                                e.target.checked
                                  ? [...current, document]
                                  : current.filter((item) => item !== document)
                              );
                            }}
                            className="h-4 w-4 rounded border-white/20 bg-slate-900"
                          />
                          <span className="truncate">{document}</span>
                        </label>
                      ))}
                    </div>
                    <button
                      onClick={submitDocuments}
                      disabled={loading || selectedDocuments.length === 0}
                      className="mt-4 rounded-lg bg-cyan-400 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50"
                    >
                      Record selected document types
                    </button>

                    <div className="mt-4 rounded-xl border border-white/10 bg-slate-950/40 p-3">
                      <p className="text-[11px] font-semibold text-slate-200">Upload actual document</p>
                      <div className="mt-2 grid gap-2 sm:grid-cols-[1fr_1fr_auto]">
                        <select
                          value={uploadDocumentType}
                          onChange={(e) => setUploadDocumentType(e.target.value)}
                          className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs"
                        >
                          <option value="">Choose required type</option>
                          {missingDocuments.map((document) => (
                            <option key={document} value={document}>{document}</option>
                          ))}
                        </select>
                        <input
                          type="file"
                          onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                          className="rounded-lg border border-white/10 bg-slate-900 p-2 text-xs text-slate-300"
                        />
                        <button
                          onClick={uploadDocument}
                          disabled={loading || !uploadDocumentType || !uploadFile}
                          className="rounded-lg border border-cyan-300/20 px-3 py-2 text-xs font-bold text-cyan-100 disabled:opacity-50"
                        >
                          Upload
                        </button>
                      </div>
                    </div>
                  </div>
                )}

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
                        {principal && ['officer', 'department_admin', 'admin'].includes(principal.role.toLowerCase()) ? (
                          <div className="w-full space-y-2 sm:max-w-md">
                            <textarea
                              value={humanNotes[action.task_id] || ''}
                              onChange={(e) =>
                                setHumanNotes((current) => ({
                                  ...current,
                                  [action.task_id]: e.target.value,
                                }))
                              }
                              placeholder="Decision note (optional)"
                              rows={2}
                              className="w-full rounded-lg border border-white/10 bg-slate-950 p-2 text-xs text-slate-200"
                            />
                            <div className="flex flex-wrap gap-2">
                              <button
                                onClick={() => continueHumanTask(action.task_id, true)}
                                disabled={loading}
                                className="rounded-lg bg-violet-300 px-4 py-2 text-xs font-bold text-slate-950 disabled:opacity-50"
                              >
                                Approve / continue
                              </button>
                              <button
                                onClick={() => continueHumanTask(action.task_id, false)}
                                disabled={loading}
                                className="rounded-lg border border-red-300/20 bg-red-300/10 px-4 py-2 text-xs font-bold text-red-100 disabled:opacity-50"
                              >
                                Reject
                              </button>
                            </div>
                          </div>
                        ) : null}
                      </div>
                    ))}
                  </div>
                )}

                <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <h3 className="font-semibold">Payments</h3>
                      <p className="mt-1 text-xs text-slate-500">
                        Controlled-MVP payment ledger. Live fees/providers are configured externally.
                      </p>
                    </div>
                    <span className="text-[10px] text-slate-500">{payments.length} recorded</span>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <input
                      inputMode="decimal"
                      value={paymentAmount}
                      onChange={(e) => setPaymentAmount(e.target.value)}
                      placeholder="Amount in INR"
                      className="w-40 rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-xs"
                    />
                    <button
                      onClick={createPayment}
                      disabled={loading}
                      className="rounded-lg border border-emerald-300/20 bg-emerald-300/10 px-3 py-2 text-xs font-bold text-emerald-100 disabled:opacity-50"
                    >
                      Create payment
                    </button>
                  </div>
                  {paymentMessage && <p className="mt-2 text-[10px] text-emerald-200">{paymentMessage}</p>}
                  {payments.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {payments.slice(0, 5).map((payment) => (
                        <div key={payment.payment_id} className="flex items-center justify-between rounded-lg border border-white/5 bg-black/10 p-2 text-[10px]">
                          <span className="font-mono text-slate-300">{payment.payment_id}</span>
                          <span className="text-slate-400">{(payment.amount_minor / 100).toFixed(2)} {payment.currency}</span>
                          <span className="text-cyan-200">{payment.status}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {notifications.length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                    <div className="flex items-center justify-between gap-2">
                      <h3 className="font-semibold">Workspace notifications</h3>
                      <span className="text-[10px] text-slate-500">{notifications.length} recent</span>
                    </div>
                    <div className="mt-3 space-y-2">
                      {notifications.map((notice) => (
                        <div key={notice.id} className="rounded-lg border border-white/5 bg-black/10 p-2">
                          <div className="flex justify-between gap-2 text-[10px]">
                            <span className="text-slate-200">{notice.event_type}</span>
                            <span className="text-slate-500">{notice.status}</span>
                          </div>
                          <p className="mt-1 text-[9px] text-slate-500">{notice.case_id || 'workspace'} · {notice.created_at || ''}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {caseData.documents && caseData.documents.length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                    <div className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-cyan-300" />
                      <h3 className="font-semibold">Document vault</h3>
                      <span className="text-[10px] text-slate-500">{caseData.documents.length} uploaded</span>
                    </div>
                    <div className="mt-4 space-y-2">
                      {caseData.documents.slice(-8).map((document) => (
                        <div key={document.document_id} className="rounded-xl border border-white/5 bg-black/10 p-3">
                          <div className="flex flex-wrap items-center justify-between gap-2">
                            <span className="text-xs font-medium text-slate-200">{document.document_type} · {document.filename}</span>
                            <span className="text-[10px] text-cyan-200">{document.extraction_mode}</span>
                          </div>
                          <p className="mt-1 break-all text-[9px] text-slate-500">SHA-256 {document.sha256}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {caseData.execution_events && caseData.execution_events.length > 0 && (
                  <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <h3 className="font-semibold">Audit trail</h3>
                        <p className="mt-1 text-xs text-slate-500">Recent tamper-evident execution events for this case.</p>
                      </div>
                      <span className="text-[10px] text-slate-500">{caseData.execution_events.length} events shown</span>
                    </div>
                    <div className="mt-4 space-y-2">
                      {caseData.execution_events.slice(-10).reverse().map((event) => (
                        <div key={String(event.sequence) + event.action} className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-white/5 bg-black/10 p-2 text-[10px]">
                          <div className="min-w-0">
                            <span className="font-medium text-slate-200">{event.action}</span>
                            {event.actor && <span className="ml-2 text-slate-500">by {event.actor}</span>}
                          </div>
                          <span className="text-slate-500">{event.timestamp || ''}</span>
                        </div>
                      ))}
                    </div>
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
