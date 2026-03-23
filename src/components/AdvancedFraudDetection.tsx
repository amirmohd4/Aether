import { useState, useEffect } from 'react';
import { supabase, type FraudDetectionLog, type Application } from '../lib/supabase';
import { TriangleAlert as AlertTriangle, Shield, TrendingUp, Zap } from 'lucide-react';

type Props = {
  selectedState: string;
};

type FlaggedApp = {
  application: Application;
  fraudLogs: FraudDetectionLog[];
};

export function AdvancedFraudDetection({ selectedState }: Props) {
  const [flaggedApps, setFlaggedApps] = useState<FlaggedApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    resolved: 0,
  });

  useEffect(() => {
    loadFraudData();
    const interval = setInterval(loadFraudData, 5000);
    return () => clearInterval(interval);
  }, [selectedState]);

  const loadFraudData = async () => {
    try {
      const { data: apps } = await supabase
        .from('applications')
        .select('*')
        .eq('state', selectedState);

      const { data: fraudLogs } = await supabase
        .from('fraud_detection_logs')
        .select('*')
        .eq('resolved', false);

      const flagged: FlaggedApp[] = (apps || [])
        .map(app => ({
          application: app,
          fraudLogs: (fraudLogs || []).filter(f => f.application_id === app.id),
        }))
        .filter(f => f.fraudLogs.length > 0);

      setFlaggedApps(flagged);

      const stats = {
        total: flagged.length,
        critical: flagged.reduce((sum, f) => sum + f.fraudLogs.filter(l => l.severity === 'critical').length, 0),
        high: flagged.reduce((sum, f) => sum + f.fraudLogs.filter(l => l.severity === 'high').length, 0),
        medium: flagged.reduce((sum, f) => sum + f.fraudLogs.filter(l => l.severity === 'medium').length, 0),
        resolved: (fraudLogs || []).filter(f => f.resolved).length,
      };

      setStats(stats);
    } catch (error) {
      console.error('Error loading fraud data');
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (fraudLogId: string, notes: string) => {
    try {
      await supabase
        .from('fraud_detection_logs')
        .update({ resolved: true, resolution_notes: notes })
        .eq('id', fraudLogId);
      await loadFraudData();
    } catch (error) {
      console.error('Error resolving fraud flag');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 text-red-900 border-red-300';
      case 'high':
        return 'bg-orange-100 text-orange-900 border-orange-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-900 border-yellow-300';
      default:
        return 'bg-blue-100 text-blue-900 border-blue-300';
    }
  };

  const getSeverityBadgeColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-600 text-white';
      case 'high':
        return 'bg-orange-600 text-white';
      case 'medium':
        return 'bg-yellow-600 text-white';
      default:
        return 'bg-blue-600 text-white';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <Shield className="w-12 h-12 text-blue-600 mx-auto mb-4 animate-pulse" />
        <p className="text-gray-600">Analyzing applications...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-red-100 rounded-lg">
            <Zap className="w-6 h-6 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800">AI Fraud Detection</h2>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-xs text-red-600 font-medium">Critical</p>
          <p className="text-2xl font-bold text-red-900">{stats.critical}</p>
        </div>
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <p className="text-xs text-orange-600 font-medium">High</p>
          <p className="text-2xl font-bold text-orange-900">{stats.high}</p>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-xs text-yellow-600 font-medium">Medium</p>
          <p className="text-2xl font-bold text-yellow-900">{stats.medium}</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-xs text-blue-600 font-medium">Flagged Apps</p>
          <p className="text-2xl font-bold text-blue-900">{stats.total}</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-xs text-green-600 font-medium">Resolved</p>
          <p className="text-2xl font-bold text-green-900">{stats.resolved}</p>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="font-semibold text-gray-800">Suspicious Applications</h3>
        {flaggedApps.length === 0 ? (
          <div className="text-center py-12 bg-green-50 border border-green-200 rounded-lg">
            <Shield className="w-16 h-16 text-green-600 mx-auto mb-3" />
            <p className="text-green-800 font-medium">No suspicious applications detected</p>
          </div>
        ) : (
          flaggedApps.map(flagged => (
            <div key={flagged.application.id} className="border border-red-300 rounded-lg overflow-hidden">
              <div className="bg-red-50 p-4 border-b border-red-200">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-semibold text-red-900 flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5" />
                      Application {flagged.application.id.slice(0, 8).toUpperCase()}
                    </h4>
                    <p className="text-sm text-red-700 mt-1">{flagged.application.citizen_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-red-600">Aadhaar: {flagged.application.aadhaar_number}</p>
                    <p className="text-xs text-red-600 mt-1">{flagged.application.district}, {flagged.application.state}</p>
                  </div>
                </div>
              </div>

              <div className="p-4 space-y-3">
                {flagged.fraudLogs.map(log => (
                  <div key={log.id} className={`border rounded-lg p-4 ${getSeverityColor(log.severity)}`}>
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 text-xs font-bold rounded ${getSeverityBadgeColor(log.severity)}`}>
                          {log.severity.toUpperCase()}
                        </span>
                        <h5 className="font-semibold">{log.fraud_type}</h5>
                      </div>
                      <span className="text-xs">
                        {new Date(log.flagged_at).toLocaleDateString()}
                      </span>
                    </div>

                    <p className="text-sm mb-2">{log.description}</p>

                    {log.evidence && (
                      <div className="bg-white bg-opacity-50 rounded p-2 mb-3 text-sm font-mono text-gray-700">
                        {log.evidence}
                      </div>
                    )}

                    {!log.resolved && (
                      <div className="flex gap-2">
                        <input
                          type="text"
                          placeholder="Resolution notes..."
                          onKeyPress={(e) => {
                            if (e.key === 'Enter' && e.currentTarget.value) {
                              handleResolve(log.id, e.currentTarget.value);
                              e.currentTarget.value = '';
                            }
                          }}
                          className="flex-1 px-2 py-1 text-sm rounded bg-white bg-opacity-70 border border-current focus:outline-none focus:ring-2"
                        />
                      </div>
                    )}

                    {log.resolved && (
                      <div className="bg-white bg-opacity-60 rounded p-2 text-sm text-green-700 font-medium">
                        ✓ Resolved: {log.resolution_notes}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
          <Zap className="w-5 h-5" />
          Fraud Detection Rules
        </h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Duplicate Aadhaar: Multiple applications with same Aadhaar number</li>
          <li>• Suspicious Transfer: Property value too low for location + property type</li>
          <li>• Document Mismatch: Property details don't match owner documents</li>
          <li>• Rapid Applications: Multiple applications from same person in 7 days</li>
          <li>• High-Risk Location: Properties in areas with known fraud patterns</li>
        </ul>
      </div>
    </div>
  );
}
