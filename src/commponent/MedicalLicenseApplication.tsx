import { useState } from 'react';
import { Stethoscope, Search, AlertCircle } from 'lucide-react';

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

interface MedicalLicense {
  license_id: string;
  doctor_name: string;
  status: string;
  fee_paid: boolean;
  issued_at: string | null;
  expires_at: string | null;
}

export function MedicalLicenseApplication() {
  const [license, setLicense] = useState<MedicalLicense | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [licenseId, setLicenseId] = useState('');

  const [doctorName, setDoctorName] = useState('');
  const [doctorId, setDoctorId] = useState('');
  const [qualification, setQualification] = useState('');
  const [institution, setInstitution] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/medical-license/apply', {
        method: 'POST',
        body: JSON.stringify({
          doctor_name: doctorName,
          doctor_id: doctorId,
          qualification: qualification,
          institution: institution,
        }),
      });
      setLicense(result);
      setLicenseId(result.license_id);
      alert('✅ Medical license application submitted!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!licenseId) {
      setError('Please enter a license ID');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<MedicalLicense>(`/medical-license/status/${licenseId}`);
      setLicense(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const map: Record<string, string> = {
      applied: 'bg-yellow-100 text-yellow-800',
      under_review: 'bg-blue-100 text-blue-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return map[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Stethoscope className="w-6 h-6 text-teal-600" />
          Medical License Application
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}

        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Doctor Name *</label>
              <input type="text" value={doctorName} onChange={(e) => setDoctorName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Doctor ID</label>
              <input type="text" value={doctorId} onChange={(e) => setDoctorId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Qualification *</label>
              <input type="text" value={qualification} onChange={(e) => setQualification(e.target.value)} placeholder="e.g., MBBS, MD" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Institution</label>
              <input type="text" value={institution} onChange={(e) => setInstitution(e.target.value)} placeholder="Medical college name" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50">
            {loading ? 'Submitting...' : 'Apply for Medical License'}
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check License Status</h3>
        <div className="flex gap-3">
          <input type="text" value={licenseId} onChange={(e) => setLicenseId(e.target.value)} placeholder="Enter License ID (e.g., ML-XXXXXXXX)" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 disabled:opacity-50 flex items-center gap-2">
            <Search className="w-4 h-4" /> Check
          </button>
        </div>
      </div>

      {license && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">License Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">License ID:</span> {license.license_id}</p>
            <p><span className="font-medium">Doctor Name:</span> {license.doctor_name}</p>
            <p><span className="font-medium">Status:</span> <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(license.status)}`}>{license.status}</span></p>
            <p><span className="font-medium">Fee Paid:</span> {license.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {license.issued_at ? new Date(license.issued_at).toLocaleDateString() : 'Not issued yet'}</p>
            <p><span className="font-medium">Expires At:</span> {license.expires_at ? new Date(license.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
