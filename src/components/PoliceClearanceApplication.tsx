import { useState } from 'react';
import { ShieldCheck, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface PCC { certificate_id: string; applicant_name: string; status: string; fee_paid: boolean; issued_at: string | null; expires_at: string | null; }

export function PoliceClearanceApplication() {
  const [pcc, setPcc] = useState<PCC | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [certId, setCertId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [applicantName, setApplicantName] = useState('');
  const [fatherName, setFatherName] = useState('');
  const [address, setAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [purpose, setPurpose] = useState('employment');
  const [passportNumber, setPassportNumber] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/police-clearance/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, applicant_name: applicantName, father_name: fatherName, address, district, state, purpose, passport_number: passportNumber }),
      });
      setPcc(result); setCertId(result.certificate_id); alert('✅ Police clearance certificate application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!certId) { setError('Please enter a certificate ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<PCC>(`/police-clearance/status/${certId}`); setPcc(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', under_verification: 'bg-blue-100 text-blue-800', issued: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><ShieldCheck className="w-6 h-6 text-blue-600" />Police Clearance Certificate</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Applicant Name *</label><input type="text" value={applicantName} onChange={(e) => setApplicantName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Father's Name *</label><input type="text" value={fatherName} onChange={(e) => setFatherName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Purpose *</label><select value={purpose} onChange={(e) => setPurpose(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="employment">Employment</option><option value="immigration">Immigration</option><option value="visa">Visa</option><option value="other">Other</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Passport Number</label><input type="text" value={passportNumber} onChange={(e) => setPassportNumber(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Address</label><textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for Police Clearance'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Certificate Status</h3>
        <div className="flex gap-3">
          <input type="text" value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="Enter Certificate ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {pcc && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Certificate Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Certificate ID:</span> {pcc.certificate_id}</p>
            <p><span className="font-medium">Applicant:</span> {pcc.applicant_name}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(pcc.status)}`}>{pcc.status}</span></p>
            <p><span className="font-medium">Fee Paid:</span> {pcc.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {pcc.issued_at ? new Date(pcc.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {pcc.expires_at ? new Date(pcc.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
