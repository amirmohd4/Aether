import { useState, useEffect } from 'react';
import { supabase, type Application } from '../lib/supabase';
import { CircleCheck as CheckCircle, Circle as XCircle, Clock, Building2 } from 'lucide-react';

type Props = {
  selectedState: string;
};

export function OfficerDashboard({ selectedState }: Props) {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState<string | null>(null);

  useEffect(() => {
    loadApplications();
  }, [selectedState]);

  const loadApplications = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('applications')
        .select('*')
        .eq('state', selectedState)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setApplications(data || []);
    } catch (err) {
      console.error('Error loading applications');
      setApplications([]);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id: string, currentStatus: string) => {
    setProcessingId(id);
    try {
      let newStatus = currentStatus;
      if (currentStatus === 'submitted') newStatus = 'verified';
      else if (currentStatus === 'verified') newStatus = 'approved';
      else if (currentStatus === 'approved') newStatus = 'completed';

      const { error } = await supabase
        .from('applications')
        .update({ status: newStatus, updated_at: new Date().toISOString() })
        .eq('id', id);

      if (error) throw error;
      await loadApplications();
    } catch (err) {
      alert('Failed to process application');
    } finally {
      setProcessingId(null);
    }
  };

  const handleReject = async (id: string) => {
    setProcessingId(id);
    try {
      const { error } = await supabase
        .from('applications')
        .update({ status: 'rejected', updated_at: new Date().toISOString() })
        .eq('id', id);

      if (error) throw error;
      await loadApplications();
    } catch (err) {
      alert('Failed to reject application');
    } finally {
      setProcessingId(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted':
        return 'bg-yellow-100 text-yellow-800';
      case 'verified':
        return 'bg-blue-100 text-blue-800';
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getDepartmentColor = (dept: string) => {
    switch (dept) {
      case 'Land Records':
        return 'text-blue-600';
      case 'Stamp Duty':
        return 'text-green-600';
      case 'Registration':
        return 'text-purple-600';
      default:
        return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <Clock className="w-12 h-12 text-blue-600 mx-auto mb-4 animate-spin" />
        <p className="text-gray-600">Loading applications...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Officer Dashboard</h2>
        <div className="text-sm text-gray-600">
          Total Applications: <span className="font-semibold">{applications.length}</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Application ID</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Citizen Name</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">District</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Department</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((app) => (
              <tr key={app.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-mono text-sm text-gray-600">
                  {app.id.slice(0, 8).toUpperCase()}
                </td>
                <td className="py-3 px-4 text-gray-800">{app.citizen_name}</td>
                <td className="py-3 px-4 text-gray-600">{app.district}</td>
                <td className="py-3 px-4">
                  <div className="flex items-center">
                    <Building2 className={`w-4 h-4 mr-2 ${getDepartmentColor(app.department)}`} />
                    <span className={`text-sm font-medium ${getDepartmentColor(app.department)}`}>
                      {app.department}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <span
                    className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                      app.status
                    )}`}
                  >
                    {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                  </span>
                </td>
                <td className="py-3 px-4 text-sm text-gray-600">
                  {new Date(app.created_at).toLocaleDateString()}
                </td>
                <td className="py-3 px-4">
                  {app.status !== 'rejected' && app.status !== 'completed' && (
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleApprove(app.id, app.status)}
                        disabled={processingId === app.id}
                        className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                      >
                        <CheckCircle className="w-4 h-4" />
                        Approve
                      </button>
                      <button
                        onClick={() => handleReject(app.id)}
                        disabled={processingId === app.id}
                        className="flex items-center gap-1 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                      >
                        <XCircle className="w-4 h-4" />
                        Reject
                      </button>
                    </div>
                  )}
                  {(app.status === 'rejected' || app.status === 'completed') && (
                    <span className="text-sm text-gray-500">No actions available</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {applications.length === 0 && (
          <div className="text-center py-12">
            <Building2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No applications found for {selectedState}</p>
          </div>
        )}
      </div>
    </div>
  );
}
