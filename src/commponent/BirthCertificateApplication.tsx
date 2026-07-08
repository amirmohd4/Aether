import { useState } from 'react';
import { Baby, Search, AlertCircle } from 'lucide-react';

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

interface BirthCertificate {
  certificate_id: string;
  child_name: string;
  status: string;
  issued_at: string | null;
}

export function BirthCertificateApplication() {
  const [cert, setCert] = useState<BirthCertificate | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [certId, setCertId] = useState('');

  const [childName, setChildName] = useState('');
  const [fatherName, setFatherName] = useState('');
  const [motherName, setMotherName] = useState('');
  const [hospitalId, setHospitalId] = useState('HOSP-001');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [gender, setGender] = useState('Male');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/birth/register', {
        method: 'POST',
        body: JSON.stringify({
          child_name: childName,
          father_name: fatherName,
          mother_name: motherName,
          hospital_id: hospitalId,
          date_of_birth: dateOfBirth,
          gender: gender,
          citizen_id: citizenId,
        }),
      });
      setCert(result);
      setCertId(result.certificate_id);
      alert('✅ Birth registered successfully!');
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
      const result = await directFetch<BirthCertificate>(`/birth/status/${certId}`);
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
          <Baby className="w-6 h-6 text-blue-600" />
          Birth Certificate Registration
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
              <label className="block text-sm font-medium text-gray-700">Child Name *</label>
              <input type="text" value={childName} onChange={(e) => setChildName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Gender *</label>
              <select value={gender} onChange={(e) => setGender(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Father's Name *</label>
              <input type="text" value={fatherName} onChange={(e) => setFatherName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Mother's Name *</label>
              <input type="text" value={motherName} onChange={(e) => setMotherName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Date of Birth *</label>
              <input type="date" value={dateOfBirth} onChange={(e) => setDateOfBirth(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Hospital ID</label>
              <input type="text" value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? 'Registering...' : 'Register Birth'}
          </button>
        </form>
      </div>

      {/* Status Check */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Certificate Status</h3>
        <div className="flex gap-3">
          <input type="text" value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="Enter Certificate ID (e.g., BC-XXXXXXXX)" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
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
            <p><span className="font-medium">Child Name:</span> {cert.child_name}</p>
            <p><span className="font-medium">Status:</span> <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(cert.status)}`}>{cert.status}</span></p>
            <p><span className="font-medium">Issued At:</span> {cert.issued_at ? new Date(cert.issued_at).toLocaleDateString() : 'Not issued yet'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
