import { useState } from 'react';
import { Building, Search, AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(err.message || `HTTP ${res.status}`);
  }
  return await res.json();
}

interface BuildingPermit {
  id: string;
  status: string;
  nocs: Record<string, string>;
  scrutiny_score: number;
  scrutiny_issues: string[];
  fee_paid: boolean;
  issued_at: string | null;
}

export function BuildingPermitApplication() {
  const [permit, setPermit] = useState<BuildingPermit | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [permitId, setPermitId] = useState('');

  const [propertyId, setPropertyId] = useState('');
  const [projectName, setProjectName] = useState('');
  const [projectType, setProjectType] = useState('residential');
  const [planUrl, setPlanUrl] = useState('');
  const [developerId] = useState('DEV-DEMO');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/building-permit/apply', {
        method: 'POST',
        body: JSON.stringify({
          property_id: propertyId,
          developer_id: developerId,
          project_name: projectName,
          project_type: projectType,
          plan_url: planUrl,
        }),
      });
      setPermit(result);
      setPermitId(result.permit_id);
      alert('✅ Building permit application submitted!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!permitId) {
      setError('Please enter a permit ID');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<BuildingPermit>(`/building-permit/status/${permitId}`);
      setPermit(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const map: Record<string, string> = {
      applied: 'bg-yellow-100 text-yellow-800',
      scrutiny: 'bg-purple-100 text-purple-800',
      nocs_approved: 'bg-blue-100 text-blue-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return map[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Building className="w-6 h-6 text-blue-600" />
          Building Permit Application
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}

        <form onSubmit={handleApply} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Property ID *</label>
            <input
              type="text"
              value={propertyId}
              onChange={(e) => setPropertyId(e.target.value)}
              placeholder="e.g., KAR-PROP-0001"
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Project Name *</label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Project Type *</label>
            <select
              value={projectType}
              onChange={(e) => setProjectType(e.target.value)}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="residential">Residential</option>
              <option value="commercial">Commercial</option>
              <option value="industrial">Industrial</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Plan URL</label>
            <input
              type="url"
              value={planUrl}
              onChange={(e) => setPlanUrl(e.target.value)}
              placeholder="https://example.com/plans/project.pdf"
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Submitting...' : 'Apply for Building Permit'}
          </button>
        </form>
      </div>

      {/* Status Check */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Permit Status</h3>
        <div className="flex gap-3">
          <input
            type="text"
            value={permitId}
            onChange={(e) => setPermitId(e.target.value)}
            placeholder="Enter Permit ID (e.g., BP-XXXXXXXX)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleStatusCheck}
            disabled={loading}
            className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 disabled:opacity-50 flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            Check
          </button>
        </div>
      </div>

      {permit && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Permit Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Permit ID:</span> {permit.id}</p>
            <p>
              <span className="font-medium">Status:</span>
              <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(permit.status)}`}>
                {permit.status}
              </span>
            </p>
            <p><span className="font-medium">Fee Paid:</span> {permit.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Scrutiny Score:</span> {permit.scrutiny_score}/100</p>
            <p><span className="font-medium">Issued At:</span> {permit.issued_at ? new Date(permit.issued_at).toLocaleDateString() : 'Not issued yet'}</p>
          </div>
          {permit.scrutiny_issues && permit.scrutiny_issues.length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold">Scrutiny Issues</h4>
              <ul className="list-disc list-inside text-sm text-red-600">
                {permit.scrutiny_issues.map((issue, i) => (
                  <li key={i}>{issue}</li>
                ))}
              </ul>
            </div>
          )}
          <div className="mt-4">
            <h4 className="font-semibold mb-2">NOC Status</h4>
            <div className="grid grid-cols-2 gap-2">
              {permit.nocs && Object.entries(permit.nocs).map(([dept, status]) => (
                <div key={dept} className="flex justify-between p-2 bg-gray-50 rounded border">
                  <span className="capitalize">{dept}</span>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    status === 'approved' ? 'bg-green-100 text-green-800' :
                    status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
