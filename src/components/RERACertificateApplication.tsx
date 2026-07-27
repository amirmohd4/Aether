import { useState } from 'react';
import { ScrollText, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface RERACert { certificate_id: string; project_name: string; developer_name: string; status: string; rera_number: string | null; fee_paid: boolean; issued_at: string | null; expires_at: string | null; }

export function RERACertificateApplication() {
  const [cert, setCert] = useState<RERACert | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [certId, setCertId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [projectName, setProjectName] = useState('');
  const [developerName, setDeveloperName] = useState('');
  const [projectId, setProjectId] = useState('');
  const [certificateType, setCertificateType] = useState('registration');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/rera-certificate/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, project_name: projectName, developer_name: developerName, project_id: projectId, certificate_type: certificateType }),
      });
      setCert(result); setCertId(result.certificate_id); alert('✅ RERA certificate application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!certId) { setError('Please enter a certificate ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<RERACert>(`/rera-certificate/status/${certId}`); setCert(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', issued: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><ScrollText className="w-6 h-6 text-blue-600" />RERA Certificate Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Project Name *</label><input type="text" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Developer Name</label><input type="text" value={developerName} onChange={(e) => setDeveloperName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Project ID</label><input type="text" value={projectId} onChange={(e) => setProjectId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Certificate Type</label><select value={certificateType} onChange={(e) => setCertificateType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="registration">Registration</option><option value="extension">Extension</option><option value="amendment">Amendment</option></select></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for RERA Certificate'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Certificate Status</h3>
        <div className="flex gap-3">
          <input type="text" value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="Enter Certificate ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {cert && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Certificate Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Certificate ID:</span> {cert.certificate_id}</p>
            <p><span className="font-medium">Project:</span> {cert.project_name}</p>
            <p><span className="font-medium">Developer:</span> {cert.developer_name}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(cert.status)}`}>{cert.status}</span></p>
            <p><span className="font-medium">RERA Number:</span> {cert.rera_number || 'Not assigned'}</p>
            <p><span className="font-medium">Issued At:</span> {cert.issued_at ? new Date(cert.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {cert.expires_at ? new Date(cert.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
