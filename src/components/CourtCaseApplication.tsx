import { useState } from 'react';
import { Gavel, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface CourtCase { case_id: string; petitioner_name: string; respondent_name: string; case_type: string; status: string; case_number: string | null; next_hearing: string | null; filed_at: string | null; }

export function CourtCaseApplication() {
  const [caseData, setCaseData] = useState<CourtCase | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [caseId, setCaseId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [petitionerName, setPetitionerName] = useState('');
  const [respondentName, setRespondentName] = useState('');
  const [caseType, setCaseType] = useState('civil');
  const [courtName, setCourtName] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [subject, setSubject] = useState('');
  const [description, setDescription] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/court-case/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, petitioner_name: petitionerName, respondent_name: respondentName, case_type: caseType, court_name: courtName, district, state, subject, description }),
      });
      setCaseData(result); setCaseId(result.case_id); alert('✅ Court case filed successfully!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!caseId) { setError('Please enter a case ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<CourtCase>(`/court-case/status/${caseId}`); setCaseData(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ filed: 'bg-blue-100 text-blue-800', under_hearing: 'bg-yellow-100 text-yellow-800', disposed: 'bg-green-100 text-green-800', dismissed: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Gavel className="w-6 h-6 text-blue-600" />Court Case Filing</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Petitioner Name *</label><input type="text" value={petitionerName} onChange={(e) => setPetitionerName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Respondent Name</label><input type="text" value={respondentName} onChange={(e) => setRespondentName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Case Type *</label><select value={caseType} onChange={(e) => setCaseType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="civil">Civil</option><option value="criminal">Criminal</option><option value="family">Family</option><option value="property">Property</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Court Name</label><input type="text" value={courtName} onChange={(e) => setCourtName(e.target.value)} placeholder="e.g., District Court Bengaluru" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Subject</label><input type="text" value={subject} onChange={(e) => setSubject(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Description</label><textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Filing...' : 'File Court Case'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Case Status</h3>
        <div className="flex gap-3">
          <input type="text" value={caseId} onChange={(e) => setCaseId(e.target.value)} placeholder="Enter Case ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {caseData && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Case Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Case ID:</span> {caseData.case_id}</p>
            <p><span className="font-medium">Petitioner:</span> {caseData.petitioner_name}</p>
            <p><span className="font-medium">Respondent:</span> {caseData.respondent_name}</p>
            <p><span className="font-medium">Case Type:</span> {caseData.case_type}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(caseData.status)}`}>{caseData.status}</span></p>
            <p><span className="font-medium">Case Number:</span> {caseData.case_number || 'Not assigned'}</p>
            <p><span className="font-medium">Next Hearing:</span> {caseData.next_hearing ? new Date(caseData.next_hearing).toLocaleDateString() : 'Not scheduled'}</p>
            <p><span className="font-medium">Filed At:</span> {caseData.filed_at ? new Date(caseData.filed_at).toLocaleDateString() : 'Not filed'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
