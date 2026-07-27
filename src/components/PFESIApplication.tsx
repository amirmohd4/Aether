import { useState } from 'react';
import { Users, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface PFESI { registration_id: string; employer_name: string; registration_type: string; status: string; fee_paid: boolean; issued_at: string | null; expires_at: string | null; }

export function PFESIApplication() {
  const [reg, setReg] = useState<PFESI | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [regId, setRegId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [employerName, setEmployerName] = useState('');
  const [establishmentName, setEstablishmentName] = useState('');
  const [registrationType, setRegistrationType] = useState('pf');
  const [employeeCount, setEmployeeCount] = useState('');
  const [wageCeiling, setWageCeiling] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/pf-esi/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, employer_name: employerName, establishment_name: establishmentName, registration_type: registrationType, employee_count: parseFloat(employeeCount) || 0, wage_ceiling: parseFloat(wageCeiling) || 0 }),
      });
      setReg(result); setRegId(result.registration_id); alert('✅ PF/ESI registration submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!regId) { setError('Please enter a registration ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<PFESI>(`/pf-esi/status/${regId}`); setReg(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Users className="w-6 h-6 text-blue-600" />PF/ESI Registration</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Employer Name *</label><input type="text" value={employerName} onChange={(e) => setEmployerName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Establishment Name</label><input type="text" value={establishmentName} onChange={(e) => setEstablishmentName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Registration Type *</label><select value={registrationType} onChange={(e) => setRegistrationType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="pf">PF (Provident Fund)</option><option value="esi">ESI (Employee State Insurance)</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Employee Count</label><input type="number" value={employeeCount} onChange={(e) => setEmployeeCount(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Wage Ceiling (₹)</label><input type="number" value={wageCeiling} onChange={(e) => setWageCeiling(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for PF/ESI Registration'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Registration Status</h3>
        <div className="flex gap-3">
          <input type="text" value={regId} onChange={(e) => setRegId(e.target.value)} placeholder="Enter Registration ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {reg && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Registration Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Registration ID:</span> {reg.registration_id}</p>
            <p><span className="font-medium">Employer:</span> {reg.employer_name}</p>
            <p><span className="font-medium">Type:</span> {reg.registration_type}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(reg.status)}`}>{reg.status}</span></p>
            <p><span className="font-medium">Fee Paid:</span> {reg.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {reg.issued_at ? new Date(reg.issued_at).toLocaleDateString() : 'Not issued'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
