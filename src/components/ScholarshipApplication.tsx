import { useState } from 'react';
import { GraduationCap, Search, AlertCircle } from 'lucide-react';

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

export function ScholarshipApplication() {
  const [app, setApp] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [appId, setAppId] = useState('');

  const [studentName, setStudentName] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [income, setIncome] = useState('');
  const [caste, setCaste] = useState('');
  const [marks, setMarks] = useState('');
  const [collegeId, setCollegeId] = useState('COL-001');
  const [course, setCourse] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/scholarship/apply', {
        method: 'POST',
        body: JSON.stringify({
          student_name: studentName,
          citizen_id: citizenId,
          income: parseFloat(income) || 0,
          caste,
          marks: parseFloat(marks) || 0,
          college_id: collegeId,
          course,
        }),
      });
      setApp(result);
      setAppId(result.application_id);
      alert('✅ Scholarship applied!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!appId) { setError('Enter application ID'); return; }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>(`/scholarship/status/${appId}`);
      setApp(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <GraduationCap className="w-6 h-6 text-blue-600" />
          Scholarship Application
        </h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Student Name *</label><input type="text" value={studentName} onChange={(e) => setStudentName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Income (Lakhs)</label><input type="number" step="0.1" value={income} onChange={(e) => setIncome(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Caste</label><select value={caste} onChange={(e) => setCaste(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option>General</option><option>OBC</option><option>SC</option><option>ST</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Marks (%)</label><input type="number" step="0.1" value={marks} onChange={(e) => setMarks(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">College ID</label><input type="text" value={collegeId} onChange={(e) => setCollegeId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Course</label><input type="text" value={course} onChange={(e) => setCourse(e.target.value)} placeholder="e.g., B.Sc, B.Tech" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Status</h3>
        <div className="flex gap-3">
          <input type="text" value={appId} onChange={(e) => setAppId(e.target.value)} placeholder="Enter Application ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {app && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Details</h3>
          <p><span className="font-medium">Application ID:</span> {app.application_id}</p>
          <p><span className="font-medium">Student:</span> {app.student_name}</p>
          <p><span className="font-medium">Status:</span> <span className={`px-2 py-1 rounded text-xs ${app.status === 'disbursed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>{app.status}</span></p>
          <p><span className="font-medium">Amount:</span> {app.amount || 'Not yet'}</p>
          <p><span className="font-medium">Disbursed At:</span> {app.disbursed_at ? new Date(app.disbursed_at).toLocaleDateString() : 'Not yet'}</p>
        </div>
      )}
    </div>
  );
}
