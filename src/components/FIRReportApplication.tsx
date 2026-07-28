import { useState } from 'react';
import { FileText, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface FIR { fir_id: string; complainant_name: string; status: string; police_station: string; filed_at: string | null; }

export function FIRApplication() {
  const [fir, setFir] = useState<FIR | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [firId, setFirId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [complainantName, setComplainantName] = useState('');
  const [accusedName, setAccusedName] = useState('');
  const [incidentDate, setIncidentDate] = useState('');
  const [incidentLocation, setIncidentLocation] = useState('');
  const [policeStation, setPoliceStation] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [firSections, setFirSections] = useState('');
  const [description, setDescription] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/fir/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, complainant_name: complainantName, accused_name: accusedName, incident_date: incidentDate, incident_location: incidentLocation, police_station: policeStation, district, state, fir_sections: firSections, description }),
      });
      setFir(result); setFirId(result.fir_id); alert('✅ FIR filed successfully!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!firId) { setError('Please enter an FIR ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<FIR>(`/fir/status/${firId}`); setFir(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ filed: 'bg-blue-100 text-blue-800', under_investigation: 'bg-yellow-100 text-yellow-800', closed: 'bg-green-100 text-green-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><FileText className="w-6 h-6 text-blue-600" />FIR Report Filing</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Complainant Name *</label><input type="text" value={complainantName} onChange={(e) => setComplainantName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Accused Name</label><input type="text" value={accusedName} onChange={(e) => setAccusedName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Incident Date *</label><input type="date" value={incidentDate} onChange={(e) => setIncidentDate(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Police Station *</label><input type="text" value={policeStation} onChange={(e) => setPoliceStation(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">IPC Sections</label><input type="text" value={firSections} onChange={(e) => setFirSections(e.target.value)} placeholder="e.g., 379, 415" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Incident Location</label><input type="text" value={incidentLocation} onChange={(e) => setIncidentLocation(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Description</label><textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Filing...' : 'File FIR'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check FIR Status</h3>
        <div className="flex gap-3">
          <input type="text" value={firId} onChange={(e) => setFirId(e.target.value)} placeholder="Enter FIR ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {fir && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">FIR Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">FIR ID:</span> {fir.fir_id}</p>
            <p><span className="font-medium">Complainant:</span> {fir.complainant_name}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(fir.status)}`}>{fir.status}</span></p>
            <p><span className="font-medium">Police Station:</span> {fir.police_station}</p>
            <p><span className="font-medium">Filed At:</span> {fir.filed_at ? new Date(fir.filed_at).toLocaleDateString() : 'Not filed'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
