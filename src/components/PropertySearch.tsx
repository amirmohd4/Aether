import { useState } from 'react';
import { Search, Building, MapPin, AlertCircle } from 'lucide-react';

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

interface Property {
  property_id: string;
  district: string;
  owner: string;
  property_value: number;
  property_size: number;
  property_type: string;
  title_status: string;
}

export function PropertySearch() {
  const [property, setProperty] = useState<Property | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchId, setSearchId] = useState('');

  const handleSearch = async () => {
    if (!searchId.trim()) {
      setError('Please enter a property ID');
      return;
    }
    setLoading(true);
    setError('');
    setProperty(null);
    try {
      const data = await directFetch<Property>(`/property/${searchId.trim()}`);
      setProperty(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    return status === 'clear' ? 'bg-green-100 text-green-800' :
           status === 'disputed' ? 'bg-red-100 text-red-800' :
           'bg-yellow-100 text-yellow-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Centered Search Bar */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-2">Aether GovOS</h1>
        <p className="text-center text-gray-600 mb-6">One API for all government services</p>
        
        <div className="flex gap-3 max-w-2xl mx-auto">
          <input
            type="text"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Enter property ID (e.g., KAR-PROP-0001)"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Search className="w-5 h-5" />
            Search
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700 text-center">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}
      </div>

      {/* Property Details (shown only after search) */}
      {loading && (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      )}

      {property && !loading && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Property Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p><span className="font-medium">Property ID:</span> {property.property_id}</p>
              <p><span className="font-medium">District:</span> {property.district}</p>
              <p><span className="font-medium">Owner:</span> {property.owner}</p>
            </div>
            <div>
              <p><span className="font-medium">Value:</span> ₹{property.property_value.toLocaleString()}</p>
              <p><span className="font-medium">Size:</span> {property.property_size.toFixed(0)} sq ft</p>
              <p><span className="font-medium">Type:</span> {property.property_type}</p>
              <p>
                <span className="font-medium">Title Status:</span>
                <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(property.title_status)}`}>
                  {property.title_status}
                </span>
              </p>
            </div>
          </div>
          <div className="mt-6 flex gap-3">
            <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">Start Registration</button>
            <button className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700">Check Fraud</button>
          </div>
        </div>
      )}
    </div>
  );
}
