import { useState, useEffect } from 'react';
import { fraudAPI } from '../lib/api';
import { AlertTriangle, Shield, AlertCircle, CheckCircle, Search } from 'lucide-react';

interface Props {
  selectedState: string;
}

export function FraudDetection({ selectedState }: Props) {
  const [highRiskAlerts, setHighRiskAlerts] = useState<any[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHighRiskAlerts();
  }, []);

  const loadHighRiskAlerts = async () => {
    setLoading(true);
    try {
      const data = await fraudAPI.getHighRisk();
      setHighRiskAlerts(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadAlertDetails = async (fraudId: string) => {
    setLoading(true);
    try {
      const data = await fraudAPI.getAlert(fraudId);
      setSelectedAlert(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      case 'high':
        return <AlertCircle className="w-5 h-5 text-orange-600" />;
      case 'medium':
        return <Shield className="w-5 h-5 text-yellow-600" />;
      default:
        return <CheckCircle className="w-5 h-5 text-green-600" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 border-red-300 text-red-900';
      case 'high':
        return 'bg-orange-100 border-orange-300 text-orange-900';
      case 'medium':
        return 'bg-yellow-100 border-yellow-300 text-yellow-900';
      default:
        return 'bg-green-100 border-green-300 text-green-900';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">AI Fraud Detection</h2>
          <button
            onClick={loadHighRiskAlerts}
            disabled={loading}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
            data-testid="refresh-alerts-btn"
          >
            <Search className="w-4 h-4 inline mr-2" />
            Refresh Alerts
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            {error}
          </div>
        )}

        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-red-50 p-4 rounded-lg border border-red-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-700">Critical</p>
                <p className="text-2xl font-bold text-red-900">
                  {highRiskAlerts.filter(a => a.severity === 'critical').length}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
          </div>

          <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-700">High</p>
                <p className="text-2xl font-bold text-orange-900">
                  {highRiskAlerts.filter(a => a.severity === 'high').length}
                </p>
              </div>
              <AlertCircle className="w-8 h-8 text-orange-600" />
            </div>
          </div>

          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-yellow-700">Medium</p>
                <p className="text-2xl font-bold text-yellow-900">
                  {highRiskAlerts.filter(a => a.severity === 'medium').length}
                </p>
              </div>
              <Shield className="w-8 h-8 text-yellow-600" />
            </div>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-700">Total Alerts</p>
                <p className="text-2xl font-bold text-blue-900">{highRiskAlerts.length}</p>
              </div>
              <Search className="w-8 h-8 text-blue-600" />
            </div>
          </div>
        </div>

        {loading && !selectedAlert ? (
          <div className="text-center py-8 text-gray-500">Loading alerts...</div>
        ) : (
          <div className="space-y-3">
            {highRiskAlerts.map((alert) => (
              <div
                key={alert.fraud_id}
                onClick={() => loadAlertDetails(alert.fraud_id)}
                className={`p-4 rounded-lg border-2 cursor-pointer hover:shadow-lg transition-shadow ${
                  getSeverityColor(alert.severity)
                }`}
                data-testid="fraud-alert-card"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    {getSeverityIcon(alert.severity)}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-semibold">Property: {alert.property_id}</h3>
                        <span className="text-xs px-2 py-1 rounded-full bg-white/50 uppercase font-bold">
                          {alert.severity}
                        </span>
                      </div>
                      <p className="text-sm mb-2">{alert.description}</p>
                      <p className="text-xs opacity-75">
                        Flagged: {new Date(alert.flagged_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{alert.fraud_score.toFixed(1)}</div>
                    <div className="text-xs">Fraud Score</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedAlert && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Fraud Alert Details</h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Fraud ID</p>
                <p className="font-medium">{selectedAlert.fraud_id}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Property ID</p>
                <p className="font-medium">{selectedAlert.property_id}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Severity</p>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-bold uppercase ${getSeverityColor(selectedAlert.severity)}`}>
                  {selectedAlert.severity}
                </span>
              </div>
              <div>
                <p className="text-sm text-gray-600">Fraud Score</p>
                <p className="text-2xl font-bold" style={{ color: selectedAlert.severity_color }}>
                  {selectedAlert.fraud_score.toFixed(1)}/100
                </p>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">AI Explanation</p>
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <p className="text-sm">{selectedAlert.explanation}</p>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">Evidence</p>
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 max-h-60 overflow-auto">
                <pre className="text-xs">{JSON.stringify(selectedAlert.evidence, null, 2)}</pre>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t">
              <p className="text-sm text-gray-600">
                Flagged: {new Date(selectedAlert.flagged_at).toLocaleString()}
              </p>
              <span className={`px-3 py-1 rounded text-sm ${selectedAlert.resolved ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                {selectedAlert.resolved ? 'Resolved' : 'Pending Review'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}