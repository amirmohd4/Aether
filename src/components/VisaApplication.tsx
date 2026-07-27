import { useState } from 'react';
import { Plane, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface Visa { application_id: string; applicant_name: string; visa_type: string; destination_country: string; status: string; visa_number: string | null; fee_paid: boolean; issued_at: string | null; expires_at: string | null; }

export function VisaApplication() {
  const [visa, setVisa] = useState<Visa | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [appId, setAppId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [applicantName, setApplicantName] = useState('');
  const [passportNumber, setPassportNumber] = useState('');
  const [visaType, setVisaType] = useState('tourist');
  const [destinationCountry, setDestinationCountry] = useState('');
  const [durationDays, setDurationDays] = useState('30');
  const [purpose, setPurpose] = useState('');
  const [entryType, setEntryType] = useState('single');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/visa/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, applicant_name: applicantName, passport_number: passportNumber, visa_type: visaType, destination_country: destinationCountry, duration_days: parseFloat(durationDays) || 30, purpose, entry_type: entryType }),
      });
      setVisa(result); setAppId(result.application_id); alert('✅ Visa application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!appId) { setError('Please enter an application ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<Visa>(`/visa/status/${appId}`); setVisa(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-blue-100 text-blue-800', issued: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Plane className="w-6 h-6 text-blue-600" />Visa Services</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Applicant Name *</label><input type="text" value={applicantName} onChange={(e) => setApplicantName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Passport Number *</label><input type="text" value={passportNumber} onChange={(e) => setPassportNumber(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Visa Type *</label><select value={visaType} onChange={(e) => setVisaType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="tourist">Tourist</option><option value="business">Business</option><option value="student">Student</option><option value="work">Work</option><option value="transit">Transit</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Destination Country *</label><input type="text" value={destinationCountry} onChange={(e) => setDestinationCountry(e.target.value)} placeholder="e.g., USA, UK, Germany" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Duration (Days)</label><input type="number" value={durationDays} onChange={(e) => setDurationDays(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Entry Type</label><select value={entryType} onChange={(e) => setEntryType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="single">Single Entry</option><option value="multiple">Multiple Entry</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Purpose</label><input type="text" value={purpose} onChange={(e) => setPurpose(e.target.value)} placeholder="e.g., Tourism, Business meeting" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for Visa'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Visa Status</h3>
        <div className="flex gap-3">
          <input type="text" value={appId} onChange={(e) => setAppId(e.target.value)} placeholder="Enter Application ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {visa && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Visa Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Application ID:</span> {visa.application_id}</p>
            <p><span className="font-medium">Applicant:</span> {visa.applicant_name}</p>
            <p><span className="font-medium">Visa Type:</span> {visa.visa_type}</p>
            <p><span className="font-medium">Destination:</span> {visa.destination_country}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(visa.status)}`}>{visa.status}</span></p>
            <p><span className="font-medium">Visa Number:</span> {visa.visa_number || 'Not assigned'}</p>
            <p><span className="font-medium">Fee Paid:</span> {visa.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {visa.issued_at ? new Date(visa.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {visa.expires_at ? new Date(visa.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
