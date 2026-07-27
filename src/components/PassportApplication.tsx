import { useState } from 'react';
import { BookOpen, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface Passport { application_id: string; applicant_name: string; passport_type: string; status: string; passport_number: string | null; fee_paid: boolean; issued_at: string | null; expires_at: string | null; }

export function PassportApplication() {
  const [passport, setPassport] = useState<Passport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [appId, setAppId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [applicantName, setApplicantName] = useState('');
  const [passportType, setPassportType] = useState('fresh');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [placeOfBirth, setPlaceOfBirth] = useState('');
  const [address, setAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [aadhaarNumber, setAadhaarNumber] = useState('');
  const [purpose, setPurpose] = useState('travel');
  const [travelCountry, setTravelCountry] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/passport/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, applicant_name: applicantName, passport_type: passportType, date_of_birth: dateOfBirth, place_of_birth: placeOfBirth, address, district, state, aadhaar_number: aadhaarNumber, purpose, travel_country: travelCountry }),
      });
      setPassport(result); setAppId(result.application_id); alert('✅ Passport application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!appId) { setError('Please enter an application ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<Passport>(`/passport/status/${appId}`); setPassport(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', police_verification: 'bg-blue-100 text-blue-800', issued: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><BookOpen className="w-6 h-6 text-blue-600" />Passport Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Applicant Name *</label><input type="text" value={applicantName} onChange={(e) => setApplicantName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Passport Type *</label><select value={passportType} onChange={(e) => setPassportType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="fresh">Fresh</option><option value="renewal">Renewal</option><option value="tatkal">Tatkal</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Date of Birth *</label><input type="date" value={dateOfBirth} onChange={(e) => setDateOfBirth(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Place of Birth</label><input type="text" value={placeOfBirth} onChange={(e) => setPlaceOfBirth(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Aadhaar Number</label><input type="text" value={aadhaarNumber} onChange={(e) => setAadhaarNumber(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Purpose *</label><select value={purpose} onChange={(e) => setPurpose(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="travel">Travel</option><option value="employment">Employment</option><option value="education">Education</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Travel Country</label><input type="text" value={travelCountry} onChange={(e) => setTravelCountry(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Address</label><textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for Passport'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Application Status</h3>
        <div className="flex gap-3">
          <input type="text" value={appId} onChange={(e) => setAppId(e.target.value)} placeholder="Enter Application ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {passport && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Application Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Application ID:</span> {passport.application_id}</p>
            <p><span className="font-medium">Applicant:</span> {passport.applicant_name}</p>
            <p><span className="font-medium">Type:</span> {passport.passport_type}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(passport.status)}`}>{passport.status}</span></p>
            <p><span className="font-medium">Passport No:</span> {passport.passport_number || 'Not assigned'}</p>
            <p><span className="font-medium">Fee Paid:</span> {passport.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {passport.issued_at ? new Date(passport.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {passport.expires_at ? new Date(passport.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
