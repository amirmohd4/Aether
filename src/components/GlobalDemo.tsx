import { useMemo, useState } from 'react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com';

type Task = {
  name: string;
  department: string;
  worker: string;
  dependencies: string[];
  status: string;
  authority_required: boolean;
  physical_action: boolean;
  result?: Record<string, unknown> | null;
  error?: string | null;
};

type CaseResponse = {
  summary: {
    case_id: string;
    objective: string;
    status: string;
    tasks_total: number;
    tasks_completed: number;
    tasks_running: number;
    tasks_waiting: number;
    exceptions: number;
    human_actions: number;
  };
  requirements: Array<{ id: string; name: string; documents?: string[] }>;
  tasks: Record<string, Task>;
  human_actions: Array<{ task_id: string; task?: string; reason?: string }>;
  exceptions: Array<{ type?: string; message?: string; error?: string }>;
  evidence: Array<{ source?: string; operation?: string; request_id?: string }>;
  outcome?: Record<string, unknown> | null;
};

export function GlobalDemo() {
  const [objective, setObjective] = useState('I want to open a restaurant');
  const [customerType, setCustomerType] = useState('business');
  const [state, setState] = useState('Jammu and Kashmir');
  const [district, setDistrict] = useState('Jammu');
  const [documents, setDocuments] = useState('identity_document, lease_or_ownership, floor_plan');
  const [caseData, setCaseData] = useState<CaseResponse | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState('');

  const tasks = useMemo(() => Object.entries(caseData?.tasks || {}), [caseData]);
  const pendingHuman = caseData?.human_actions || [];

  const startCase = async () => {
    setIsRunning(true);
    setError('');
    setCaseData(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/aether/v2/cases`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country: 'India', state, district },
          inputs: {
            documents: documents.split(',').map((item) => item.trim()).filter(Boolean),
            fields: { applicant_type: customerType }
          }
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Unable to start Aether case');
      setCaseData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to start case');
    } finally {
      setIsRunning(false);
    }
  };

  const decide = async (taskId: string, approved: boolean) => {
    if (!caseData) return;
    setIsRunning(true);
    setError('');
    try {
      const response = await fetch(`${BACKEND_URL}/api/aether/v2/cases/${caseData.summary.case_id}/human/${taskId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ approved, note: approved ? 'Approved by authorised demo officer' : 'Rejected by demo officer' })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Unable to record decision');
      setCaseData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to record decision');
    } finally {
      setIsRunning(false);
    }
  };

  const statusLabel = (status: string) => status.replaceAll('_', ' ');

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
        <div className="flex items-start justify-between gap-4 mb-5">
          <div>
            <p className="text-xs font-semibold tracking-widest text-blue-600 uppercase">Aether GovOS V2</p>
            <h2 className="text-2xl font-bold text-gray-900 mt-1">Tell Aether the outcome you need</h2>
            <p className="text-sm text-gray-500 mt-1">Aether builds and executes the work graph instead of merely tracking an application.</p>
          </div>
          {caseData && <span className="px-3 py-1 rounded-full bg-gray-100 text-xs font-semibold uppercase">{statusLabel(caseData.summary.status)}</span>}
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700">What do you want done?</label>
            <input value={objective} onChange={(e) => setObjective(e.target.value)} className="mt-1 w-full border rounded-lg p-3" placeholder="I want to open a restaurant" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Customer</label>
            <select value={customerType} onChange={(e) => setCustomerType(e.target.value)} className="mt-1 w-full border rounded-lg p-3">
              <option value="business">Business</option>
              <option value="bank">Bank</option>
              <option value="developer">Developer</option>
              <option value="citizen">Citizen</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">State</label>
            <input value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full border rounded-lg p-3" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">District</label>
            <input value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full border rounded-lg p-3" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Submitted documents</label>
            <input value={documents} onChange={(e) => setDocuments(e.target.value)} className="mt-1 w-full border rounded-lg p-3" />
          </div>
        </div>

        {error && <div className="mt-4 p-3 rounded-lg bg-red-50 text-red-700 text-sm">{error}</div>}

        <button onClick={startCase} disabled={isRunning || !objective.trim()} className="mt-5 px-6 py-3 rounded-lg font-semibold bg-blue-600 hover:bg-blue-700 text-white disabled:bg-gray-400">
          {isRunning ? 'Aether is executing…' : 'Start Aether Case'}
        </button>
      </div>

      {caseData && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {[
              ['Completed', caseData.summary.tasks_completed],
              ['Running', caseData.summary.tasks_running],
              ['Waiting', caseData.summary.tasks_waiting],
              ['Human actions', caseData.summary.human_actions],
              ['Exceptions', caseData.summary.exceptions],
            ].map(([label, value]) => (
              <div key={label} className="bg-white border rounded-xl p-4">
                <div className="text-2xl font-bold">{value}</div>
                <div className="text-xs text-gray-500 mt-1">{label}</div>
              </div>
            ))}
          </div>

          <div className="bg-white rounded-2xl shadow-lg border p-6">
            <h3 className="font-bold text-lg">Aether work graph</h3>
            <p className="text-sm text-gray-500 mb-4">Green tasks have completed digital work. Human and physical boundaries remain explicit.</p>
            <div className="space-y-2">
              {tasks.map(([id, task]) => (
                <div key={id} className="border rounded-lg p-3 flex flex-col md:flex-row md:items-center gap-2">
                  <div className="flex-1">
                    <div className="font-medium">{task.name}</div>
                    <div className="text-xs text-gray-500">{task.department} · {task.worker}</div>
                  </div>
                  <div className="text-xs px-2 py-1 rounded bg-gray-100 uppercase font-semibold">{statusLabel(task.status)}</div>
                  {task.physical_action && <div className="text-xs px-2 py-1 rounded bg-amber-50 text-amber-700">Physical</div>}
                  {task.authority_required && <div className="text-xs px-2 py-1 rounded bg-purple-50 text-purple-700">Authority</div>}
                </div>
              ))}
            </div>
          </div>

          {caseData.requirements.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border p-6">
              <h3 className="font-bold text-lg">Requirements Aether identified</h3>
              <div className="grid md:grid-cols-2 gap-3 mt-4">
                {caseData.requirements.map((requirement) => (
                  <div key={requirement.id} className="border rounded-lg p-3">
                    <div className="font-medium">{requirement.name}</div>
                    <div className="text-xs text-gray-500 mt-1">Documents: {(requirement.documents || []).join(', ') || 'None specified'}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {pendingHuman.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6">
              <h3 className="font-bold text-lg text-amber-900">Human action required</h3>
              <p className="text-sm text-amber-800 mt-1">Aether has paused only at a declared authority or physical boundary.</p>
              <div className="space-y-3 mt-4">
                {pendingHuman.map((action) => (
                  <div key={action.task_id} className="bg-white rounded-lg border p-4 flex flex-col md:flex-row md:items-center gap-3">
                    <div className="flex-1">
                      <div className="font-medium">{action.task || action.task_id}</div>
                      <div className="text-xs text-gray-500">{action.reason}</div>
                    </div>
                    <button disabled={isRunning} onClick={() => decide(action.task_id, true)} className="px-4 py-2 rounded-lg bg-green-600 text-white text-sm font-semibold disabled:bg-gray-400">Approve & Resume</button>
                    <button disabled={isRunning} onClick={() => decide(action.task_id, false)} className="px-4 py-2 rounded-lg bg-white border text-red-600 text-sm font-semibold disabled:opacity-50">Reject</button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {caseData.evidence.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border p-6">
              <h3 className="font-bold text-lg">Execution evidence</h3>
              <div className="mt-3 text-sm space-y-2">
                {caseData.evidence.slice(-8).map((item, index) => (
                  <div key={`${item.request_id}-${index}`} className="flex gap-3 border-b pb-2">
                    <span className="text-green-600">✓</span>
                    <span>{item.operation || 'operation'} · {item.source || 'Aether worker'} · {item.request_id || 'internal'}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {caseData.outcome && (
            <div className="bg-green-50 border border-green-200 rounded-2xl p-6">
              <h3 className="font-bold text-lg text-green-900">Final outcome</h3>
              <pre className="text-xs mt-3 whitespace-pre-wrap">{JSON.stringify(caseData.outcome, null, 2)}</pre>
            </div>
          )}
        </>
      )}
    </div>
  );
}
