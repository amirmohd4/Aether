import { useState } from 'react';
import { HardHat, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface RERAProject { project_id: string; project_name: string; developer_name: string; status: string; rera_number: string | null; fee_paid: boolean; issued_at: string | null; }

export function RERAProjectApplication() {
  const [project, setProject] = useState<RERAProject | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [projectId, setProjectId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [developerName, setDeveloperName] = useState('');
  const [projectName, setProjectName] = useState('');
  const [projectType, setProjectType] = useState('residential');
  const [projectAddress, setProjectAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [landArea, setLandArea] = useState('');
  const [totalUnits, setTotalUnits] = useState('');
  const [estimatedCost, setEstimatedCost] = useState('');
  const [completionDate, setCompletionDate] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/rera-project/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, developer_name: developerName, project_name: projectName, project_type: projectType, project_address: projectAddress, district, state, land_area: parseFloat(landArea) || 0, total_units: parseFloat(totalUnits) || 0, estimated_cost: parseFloat(estimatedCost) || 0, completion_date: completionDate }),
      });
      setProject(result); setProjectId(result.project_id); alert('✅ RERA project registration submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!projectId) { setError('Please enter a project ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<RERAProject>(`/rera-project/status/${projectId}`); setProject(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><HardHat className="w-6 h-6 text-blue-600" />RERA Project Registration</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Developer Name *</label><input type="text" value={developerName} onChange={(e) => setDeveloperName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Project Name *</label><input type="text" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Project Type *</label><select value={projectType} onChange={(e) => setProjectType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="residential">Residential</option><option value="commercial">Commercial</option><option value="mixed">Mixed Use</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Land Area (sq.m)</label><input type="number" value={landArea} onChange={(e) => setLandArea(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Total Units</label><input type="number" value={totalUnits} onChange={(e) => setTotalUnits(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Estimated Cost (₹)</label><input type="number" value={estimatedCost} onChange={(e) => setEstimatedCost(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Completion Date</label><input type="date" value={completionDate} onChange={(e) => setCompletionDate(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Project Address</label><textarea value={projectAddress} onChange={(e) => setProjectAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Register RERA Project'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Project Status</h3>
        <div className="flex gap-3">
          <input type="text" value={projectId} onChange={(e) => setProjectId(e.target.value)} placeholder="Enter Project ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {project && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Project Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Project ID:</span> {project.project_id}</p>
            <p><span className="font-medium">Project Name:</span> {project.project_name}</p>
            <p><span className="font-medium">Developer:</span> {project.developer_name}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(project.status)}`}>{project.status}</span></p>
            <p><span className="font-medium">RERA Number:</span> {project.rera_number || 'Not assigned'}</p>
            <p><span className="font-medium">Issued At:</span> {project.issued_at ? new Date(project.issued_at).toLocaleDateString() : 'Not issued'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
