import { useState } from 'react';
import { Skull, Search, AlertCircle } from 'lucide-react';

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

interface DeathCertificate {
  certificate_id: string;
  deceased_name: string;
  status: string;
  issued_at: string | null;
}

export function DeathCertificateApplication() {
  const [cert, setCert] = useState<DeathCertificate | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [certId, setCertId] = useState('');

  const [deceasedName, setDeceasedName] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [hospitalId, setHospitalId] = useState('HOSP-001');
  const [dateOfDeath, setDateOfDeath] = useState('');
  const [causeOfDeath, setCauseOfDeath] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/death/register', {
        method: 'POST',
        body: JSON.stringify({
          deceased_name: deceasedName,
          citizen_id: citizenId,
          hospital_id: hospitalId,
          date_of_death: dateOfDeath,
          cause_of_death: causeOfDeath,
        }),
      });
      setCert(result);
      setCertId(result.certificate_id);
      alert('✅ Death registered successfully!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!certId) {
      setError('Please enter a certificate ID');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<DeathCertificate>(`/death/status/${certId}`);
      setCert(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    return status === 'issued' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Skull className="w-6 h-6 text-gray-600" />
          Death Certificate Registration
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Deceased Name *</label>
              <input type="text" value={deceasedName} onChange={(e) => setDeceasedName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Citizen ID</label>
              <input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Date of Death *</label>
              <input type="date" value={dateOfDeath} onChange={(e) => setDateOfDeath(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Cause of Death</label>
              <input type="text" value={causeOfDeath} onChange={(e) => setCauseOfDeath(e.target.value)} placeholder="e.g., Cardiac arrest" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Hospital ID</label>
              <input type="text" value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-800 disabled:opacity-50">
            {loading ? 'Registering...' : 'Register Death'}
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Certificate Status</h3>
        <div className="flex gap-3">
          <input type="text" value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="Enter Certificate ID (e.g., DC-XXXXXXXX)" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 disabled:opacity-50 flex items-center gap-2">
            <Search className="w-4 h-4" /> Check
          </button>
        </div>
      </div>

      {cert && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Certificate Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Certificate ID:</span> {cert.certificate_id}</p>
            <p><span className="font-medium">Deceased Name:</span> {cert.deceased_name}</p>
            <p><span className="font-medium">Status:</span> <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(cert.status)}`}>{cert.status}</span></p>
            <p><span className="font-medium">Issued At:</span> {cert.issued_at ? new Date(cert.issued_at).toLocaleDateString() : 'Not issued yet'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
