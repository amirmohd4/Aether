import { useState } from 'react';
import { Factory, Search, CircleAlert as AlertCircle } from 'lucide-react';

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

interface FactoryLicense {
  license_id: string;
  factory_name: string;
  status: string;
  nocs: Record<string, string>;
  fee_paid: boolean;
  issued_at: string | null;
  expires_at: string | null;
}

export function FactoryLicenseApplication() {
  const [license, setLicense] = useState<FactoryLicense | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [licenseId, setLicenseId] = useState('');

  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [factoryName, setFactoryName] = useState('');
  const [factoryType, setFactoryType] = useState('');
  const [address, setAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [employeeCount, setEmployeeCount] = useState('');
  const [machineryDetails, setMachineryDetails] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/factory-license/apply', {
        method: 'POST',
        body: JSON.stringify({
          citizen_id: citizenId,
          factory_name: factoryName,
          factory_type: factoryType,
          address,
          district,
          state,
          employee_count: parseFloat(employeeCount) || 0,
          machinery_details: machineryDetails,
        }),
      });
      setLicense(result);
      setLicenseId(result.license_id);
      alert('✅ Factory license application submitted!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!licenseId) { setError('Please enter a license ID'); return; }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<FactoryLicense>(`/factory-license/status/${licenseId}`);
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
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return map[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Factory className="w-6 h-6 text-blue-600" />
          Factory License Application
        </h2>
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />{error}
          </div>
        )}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label>
              <input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Factory Name *</label>
              <input type="text" value={factoryName} onChange={(e) => setFactoryName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Factory Type *</label>
              <select value={factoryType} onChange={(e) => setFactoryType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required>
                <option value="">Select</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="chemical">Chemical</option>
                <option value="textile">Textile</option>
                <option value="food_processing">Food Processing</option>
                <option value="hazardous">Hazardous</option>
              </select></div>
            <div><label className="block text-sm font-medium text-gray-700">Employee Count</label>
              <input type="number" value={employeeCount} onChange={(e) => setEmployeeCount(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label>
              <input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label>
              <input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Factory Address</label>
              <textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Machinery Details</label>
              <textarea value={machineryDetails} onChange={(e) => setMachineryDetails(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? 'Submitting...' : 'Apply for Factory License'}
          </button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check License Status</h3>
        <div className="flex gap-3">
          <input type="text" value={licenseId} onChange={(e) => setLicenseId(e.target.value)} placeholder="Enter License ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2">
            <Search className="w-4 h-4" /> Check
          </button>
        </div>
      </div>
      {license && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">License Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">License ID:</span> {license.license_id}</p>
            <p><span className="font-medium">Factory Name:</span> {license.factory_name}</p>
            <p><span className="font-medium">Status:</span>
              <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(license.status)}`}>{license.status}</span></p>
            <p><span className="font-medium">Fee Paid:</span> {license.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Issued At:</span> {license.issued_at ? new Date(license.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {license.expires_at ? new Date(license.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
          {license.nocs && Object.keys(license.nocs).length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold mb-2">NOC Status</h4>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(license.nocs).map(([dept, status]) => (
                  <div key={dept} className="flex justify-between p-2 bg-gray-50 rounded border">
                    <span className="capitalize">{dept}</span>
                    <span className={`px-2 py-0.5 rounded text-xs ${status === 'approved' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>{status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
