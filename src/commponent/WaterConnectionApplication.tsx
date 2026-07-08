import { useState } from 'react';
import { Droplets, Search, AlertCircle } from 'lucide-react';

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

interface WaterConnection {
  id: string;
  status: string;
  fee_paid: boolean;
  connected_at: string | null;
}

export function WaterConnectionApplication() {
  const [connection, setConnection] = useState<WaterConnection | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [connectionId, setConnectionId] = useState('');

  const [propertyId, setPropertyId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [connectionType, setConnectionType] = useState('residential');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<any>('/water-connection/apply', {
        method: 'POST',
        body: JSON.stringify({
          property_id: propertyId,
          citizen_id: citizenId,
          connection_type: connectionType,
        }),
      });
      setConnection(result);
      setConnectionId(result.connection_id);
      alert('✅ Water connection application submitted!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!connectionId) {
      setError('Please enter a connection ID');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const result = await directFetch<WaterConnection>(`/water-connection/status/${connectionId}`);
      setConnection(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const map: Record<string, string> = {
      applied: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-blue-100 text-blue-800',
      connected: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return map[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Droplets className="w-6 h-6 text-blue-600" />
          Water Connection Application
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}

        <form onSubmit={handleApply} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Property ID *</label>
            <input
              type="text"
              value={propertyId}
              onChange={(e) => setPropertyId(e.target.value)}
              placeholder="e.g., KAR-PROP-0001"
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Citizen ID *</label>
            <input
              type="text"
              value={citizenId}
              onChange={(e) => setCitizenId(e.target.value)}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Connection Type *</label>
            <select
              value={connectionType}
              onChange={(e) => setConnectionType(e.target.value)}
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="residential">Residential</option>
              <option value="commercial">Commercial</option>
              <option value="industrial">Industrial</option>
            </select>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Submitting...' : 'Apply for Water Connection'}
          </button>
        </form>
      </div>

      {/* Status Check */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Connection Status</h3>
        <div className="flex gap-3">
          <input
            type="text"
            value={connectionId}
            onChange={(e) => setConnectionId(e.target.value)}
            placeholder="Enter Connection ID (e.g., WC-XXXXXXXX)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleStatusCheck}
            disabled={loading}
            className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 disabled:opacity-50 flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            Check
          </button>
        </div>
      </div>

      {connection && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Connection Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Connection ID:</span> {connection.id}</p>
            <p>
              <span className="font-medium">Status:</span>
              <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(connection.status)}`}>
                {connection.status}
              </span>
            </p>
            <p><span className="font-medium">Fee Paid:</span> {connection.fee_paid ? '✅ Yes' : '❌ No'}</p>
            <p><span className="font-medium">Connected At:</span> {connection.connected_at ? new Date(connection.connected_at).toLocaleDateString() : 'Not connected yet'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
