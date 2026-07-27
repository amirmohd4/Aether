import { useState } from 'react';
import { Monitor, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface ECourt { e_court_id: string; case_number: string; court_name: string; petitioner: string; respondent: string; status: string; hearing_date: string | null; }

export function ECourtApplication() {
  const [eCourt, setECourt] = useState<ECourt | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [eCourtId, setECourtId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [caseNumber, setCaseNumber] = useState('');
  const [courtName, setCourtName] = useState('');
  const [petitioner, setPetitioner] = useState('');
  const [respondent, setRespondent] = useState('');
  const [hearingDate, setHearingDate] = useState('');
  const [notes, setNotes] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/e-court/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, case_number: caseNumber, court_name: courtName, petitioner, respondent, hearing_date: hearingDate, notes }),
      });
      setECourt(result); setECourtId(result.e_court_id); alert('✅ E-Court hearing scheduled!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!eCourtId) { setError('Please enter an E-Court ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<ECourt>(`/e-court/status/${eCourtId}`); setECourt(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ scheduled: 'bg-blue-100 text-blue-800', adjourned: 'bg-yellow-100 text-yellow-800', completed: 'bg-green-100 text-green-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Monitor className="w-6 h-6 text-blue-600" />E-Court Hearing</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Case Number *</label><input type="text" value={caseNumber} onChange={(e) => setCaseNumber(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Court Name</label><input type="text" value={courtName} onChange={(e) => setCourtName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Hearing Date</label><input type="datetime-local" value={hearingDate} onChange={(e) => setHearingDate(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Petitioner</label><input type="text" value={petitioner} onChange={(e) => setPetitioner(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Respondent</label><input type="text" value={respondent} onChange={(e) => setRespondent(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Notes</label><textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Scheduling...' : 'Schedule E-Court Hearing'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check E-Court Status</h3>
        <div className="flex gap-3">
          <input type="text" value={eCourtId} onChange={(e) => setECourtId(e.target.value)} placeholder="Enter E-Court ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {eCourt && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">E-Court Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">E-Court ID:</span> {eCourt.e_court_id}</p>
            <p><span className="font-medium">Case Number:</span> {eCourt.case_number}</p>
            <p><span className="font-medium">Court:</span> {eCourt.court_name}</p>
            <p><span className="font-medium">Petitioner:</span> {eCourt.petitioner}</p>
            <p><span className="font-medium">Respondent:</span> {eCourt.respondent}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(eCourt.status)}`}>{eCourt.status}</span></p>
            <p><span className="font-medium">Hearing Date:</span> {eCourt.hearing_date ? new Date(eCourt.hearing_date).toLocaleString() : 'Not scheduled'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
