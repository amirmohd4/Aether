import { useState, useEffect } from 'react';
import { systemAPI } from '../lib/api';
import { Code, DollarSign, Zap, Lock, Activity } from 'lucide-react';

export function APIMarketplace() {
  const [marketplace, setMarketplace] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMarketplace();
  }, []);

  const loadMarketplace = async () => {
    setLoading(true);
    try {
      const data = await systemAPI.marketplace();
      setMarketplace(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getMethodColor = (method: string) => {
    switch (method) {
      case 'GET':
        return 'bg-green-100 text-green-800';
      case 'POST':
        return 'bg-blue-100 text-blue-800';
      case 'PUT':
        return 'bg-yellow-100 text-yellow-800';
      case 'DELETE':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">API Marketplace</h2>
          <p className="text-gray-600">Explore and integrate Aether GovOS APIs into your applications</p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading marketplace...</div>
        ) : marketplace ? (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200">
                <Code className="w-8 h-8 text-purple-600 mb-2" />
                <p className="text-3xl font-bold text-purple-900">{marketplace.total_apis}</p>
                <p className="text-sm text-purple-700">Available APIs</p>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                <Lock className="w-8 h-8 text-blue-600 mb-2" />
                <p className="text-lg font-bold text-blue-900">API Key</p>
                <p className="text-sm text-blue-700">Authentication Required</p>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                <Activity className="w-8 h-8 text-green-600 mb-2" />
                <p className="text-lg font-bold text-green-900">REST API</p>
                <p className="text-sm text-green-700">JSON Responses</p>
              </div>
            </div>

            <div className="space-y-4">
              {marketplace.marketplace.map((api: any, index: number) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-5 hover:shadow-lg transition-shadow"
                  data-testid="api-card"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${getMethodColor(api.method)}`}>
                          {api.method}
                        </span>
                        <h3 className="text-lg font-semibold text-gray-900">{api.api_name}</h3>
                      </div>
                      <code className="text-sm bg-gray-100 px-3 py-1 rounded text-blue-600 font-mono">
                        {api.endpoint}
                      </code>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center gap-1 text-green-600 font-bold">
                        {api.pricing === 'Free' ? (
                          <span className="text-lg">FREE</span>
                        ) : (
                          <>
                            <DollarSign className="w-4 h-4" />
                            <span>{api.pricing}</span>
                          </>
                        )}
                      </div>
                      <div className="flex items-center gap-1 text-xs text-gray-500 mt-1">
                        <Zap className="w-3 h-3" />
                        {api.rate_limit}
                      </div>
                    </div>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-3">{api.description}</p>
                  
                  <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                    <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                      View Documentation →
                    </button>
                    <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700">
                      Try It Out
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 bg-blue-50 p-6 rounded-lg border border-blue-200">
              <h3 className="text-lg font-semibold text-blue-900 mb-3">Getting Started</h3>
              <div className="space-y-2 text-sm text-blue-800">
                <p><span className="font-medium">1.</span> Obtain your API key from the developer portal</p>
                <p><span className="font-medium">2.</span> Include the API key in your request headers</p>
                <p><span className="font-medium">3.</span> Make requests to the endpoints listed above</p>
                <p><span className="font-medium">4.</span> Check the documentation for detailed examples: {marketplace.documentation}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">No APIs available</div>
        )}
      </div>
    </div>
  );
}