import { useState, useEffect } from 'react';
import { workflowAPI, systemAPI } from '../lib/api';
import { Users, CheckCircle, XCircle, Clock, AlertTriangle, TrendingUp } from 'lucide-react';

interface Props {
  selectedState: string;
}

export function OfficerDashboard({ selectedState }: Props) {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    setLoading(true);
    try {
      const data = await systemAPI.stats();
      setStats(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Officer Dashboard</h2>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading dashboard...</div>
        ) : stats ? (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-blue-900">Total Properties</h3>
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                </div>
                <p className="text-3xl font-bold text-blue-900">{stats.properties.total.toLocaleString()}</p>
                <p className="text-xs text-blue-700 mt-1">
                  Karnataka: {stats.properties.karnataka} | J&K: {stats.properties.jk}
                </p>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-green-900">Active Workflows</h3>
                  <Clock className="w-5 h-5 text-green-600" />
                </div>
                <p className="text-3xl font-bold text-green-900">{stats.workflows.active}</p>
                <p className="text-xs text-green-700 mt-1">
                  Total: {stats.workflows.total} | Completed: {stats.workflows.completed}
                </p>
              </div>

              <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-lg border border-red-200">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-red-900">High Risk Alerts</h3>
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                </div>
                <p className="text-3xl font-bold text-red-900">{stats.fraud_alerts.high_risk}</p>
                <p className="text-xs text-red-700 mt-1">
                  Total Alerts: {stats.fraud_alerts.total} | Unresolved: {stats.fraud_alerts.unresolved}
                </p>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Workflow Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-gray-900">{stats.workflows.completed}</p>
                  <p className="text-xs text-gray-600">Completed</p>
                </div>
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <Clock className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-gray-900">{stats.workflows.active}</p>
                  <p className="text-xs text-gray-600">In Progress</p>
                </div>
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <AlertTriangle className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.workflows.total - stats.workflows.completed - stats.workflows.active}
                  </p>
                  <p className="text-xs text-gray-600">Manual Review</p>
                </div>
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-center">
                  <XCircle className="w-8 h-8 text-red-600 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-gray-900">0</p>
                  <p className="text-xs text-gray-600">Rejected</p>
                </div>
              </div>
            </div>

            <div className="mt-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h4 className="font-semibold text-blue-900 mb-2">State: {selectedState === 'karnataka' ? 'Karnataka' : 'Jammu & Kashmir'}</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-blue-700">Properties Registered:</p>
                  <p className="font-bold text-blue-900">
                    {selectedState === 'karnataka' ? stats.properties.karnataka : stats.properties.jk}
                  </p>
                </div>
                <div>
                  <p className="text-blue-700">Active in State:</p>
                  <p className="font-bold text-blue-900">{Math.floor(stats.workflows.active / 2)}</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">No data available</div>
        )}
      </div>
    </div>
  );
}