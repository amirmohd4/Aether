import { useState } from 'react';
import { Hop as Home, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface PMAY { application_id: string; applicant_name: string; category: string; status: string; subsidy_amount: number; sanctioned_at: string | null; }

export function PMAYApplication() {
  const [app, setApp] = useState<PMAY | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [appId, setAppId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [applicantName, setApplicantName] = useState('');
  const [spouseName, setSpouseName] = useState('');
  const [address, setAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [annualIncome, setAnnualIncome] = useState('');
  const [category, setCategory] = useState('EWS');
  const [carpetArea, setCarpetArea] = useState('');
  const [aadhaarNumber, setAadhaarNumber] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/pmay/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, applicant_name: applicantName, spouse_name: spouseName, address, district, state, annual_income: parseFloat(annualIncome) || 0, category, carpet_area_required: parseFloat(carpetArea) || 0, aadhaar_number: aadhaarNumber }),
      });
      setApp(result); setAppId(result.application_id); alert('✅ PMAY application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!appId) { setError('Please enter an application ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<PMAY>(`/pmay/status/${appId}`); setApp(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-blue-100 text-blue-800', sanctioned: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Home className="w-6 h-6 text-blue-600" />PMAY Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Applicant Name *</label><input type="text" value={applicantName} onChange={(e) => setApplicantName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Spouse Name</label><input type="text" value={spouseName} onChange={(e) => setSpouseName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Category *</label><select value={category} onChange={(e) => setCategory(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="EWS">EWS (Economically Weaker Section)</option><option value="LIG">LIG (Low Income Group)</option><option value="MIG_I">MIG-I (Middle Income Group I)</option><option value="MIG_II">MIG-II (Middle Income Group II)</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Annual Income (₹)</label><input type="number" value={annualIncome} onChange={(e) => setAnnualIncome(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Carpet Area Required (sq.ft)</label><input type="number" value={carpetArea} onChange={(e) => setCarpetArea(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Aadhaar Number</label><input type="text" value={aadhaarNumber} onChange={(e) => setAadhaarNumber(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Address</label><textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for PMAY'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Application Status</h3>
        <div className="flex gap-3">
          <input type="text" value={appId} onChange={(e) => setAppId(e.target.value)} placeholder="Enter Application ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {app && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Application Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Application ID:</span> {app.application_id}</p>
            <p><span className="font-medium">Applicant:</span> {app.applicant_name}</p>
            <p><span className="font-medium">Category:</span> {app.category}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(app.status)}`}>{app.status}</span></p>
            <p><span className="font-medium">Subsidy Amount:</span> ₹{app.subsidy_amount}</p>
            <p><span className="font-medium">Sanctioned At:</span> {app.sanctioned_at ? new Date(app.sanctioned_at).toLocaleDateString() : 'Not sanctioned'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
