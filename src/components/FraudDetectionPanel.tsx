import { useState, useEffect } from 'react';
import { supabase, type Application, type FraudFlag } from '../lib/supabase';
import { AlertTriangle, Shield, TrendingUp } from 'lucide-react';

type FlaggedApplication = Application & {
  fraud_flags: FraudFlag[];
};

type Props = {
  selectedState: string;
};

export function FraudDetectionPanel({ selectedState }: Props) {
  const [flaggedApps, setFlaggedApps] = useState<FlaggedApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    flagged: 0,
    percentage: 0,
  });

  useEffect(() => {
    loadFlaggedApplications();
  }, [selectedState]);

  const loadFlaggedApplications = async () => {
    setLoading(true);
    try {
      const { data: allApps, error: appsError } = await supabase
        .from('applications')
        .select('*')
        .eq('state', selectedState);

      if (appsError) throw appsError;

      const { data: flags, error: flagsError } = await supabase
        .from('fraud_flags')
        .select('*');

      if (flagsError) throw flagsError;

      const flaggedApplications = (allApps || [])
        .map((app) => ({
          ...app,
          fraud_flags: (flags || []).filter((flag) => flag.application_id === app.id),
        }))
        .filter((app) => app.fraud_flags.length > 0);

      setFlaggedApps(flaggedApplications);

      setStats({
        total: allApps?.length || 0,
        flagged: flaggedApplications.length,
        percentage:
          allApps && allApps.length > 0
            ? Math.round((flaggedApplications.length / allApps.length) * 100)
            : 0,
      });
    } catch (err) {
      console.error('Error loading fraud flags');
    } finally {
      setLoading(false);
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
            <Shield className="w-6 h-6 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800">AI Fraud Detection</h2>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium">Total Applications</p>
              <p className="text-2xl font-bold text-blue-900">{stats.total}</p>
            </div>
            <TrendingUp className="w-8 h-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600 font-medium">Flagged Applications</p>
              <p className="text-2xl font-bold text-red-900">{stats.flagged}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-600" />
          </div>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-amber-600 font-medium">Fraud Rate</p>
              <p className="text-2xl font-bold text-amber-900">{stats.percentage}%</p>
            </div>
            <Shield className="w-8 h-8 text-amber-600" />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="font-semibold text-gray-800">Suspicious Applications</h3>
        {flaggedApps.length === 0 ? (
          <div className="text-center py-8 bg-green-50 border border-green-200 rounded-lg">
            <Shield className="w-12 h-12 text-green-600 mx-auto mb-3" />
            <p className="text-green-800 font-medium">No suspicious applications detected</p>
            <p className="text-sm text-green-600 mt-1">All applications appear legitimate</p>
          </div>
        ) : (
          flaggedApps.map((app) => (
            <div
              key={app.id}
              className="border-l-4 border-red-500 bg-red-50 p-4 rounded-r-lg hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                    <span className="font-semibold text-red-900">
                      Application ID: {app.id.slice(0, 8).toUpperCase()}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700 mb-3">
                    <p>
                      <span className="font-medium">Applicant:</span> {app.citizen_name}
                    </p>
                    <p>
                      <span className="font-medium">Aadhaar:</span> {app.aadhaar_number}
                    </p>
                    <p>
                      <span className="font-medium">District:</span> {app.district}
                    </p>
                  </div>
                  <div className="space-y-2">
                    {app.fraud_flags.map((flag) => (
                      <div key={flag.id} className="bg-white border border-red-200 rounded p-3">
                        <div className="flex items-start gap-2">
                          <AlertTriangle className="w-4 h-4 text-red-600 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="font-medium text-red-900 text-sm">
                              {flag.flag_type.replace('_', ' ').toUpperCase()}
                            </p>
                            <p className="text-sm text-gray-600 mt-1">{flag.description}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <span className="font-medium">AI Detection Algorithm:</span> Analyzing patterns including
          duplicate Aadhaar numbers, incomplete documentation, suspicious property addresses, and
          unusual application frequencies.
        </p>
      </div>
    </div>
  );
}
