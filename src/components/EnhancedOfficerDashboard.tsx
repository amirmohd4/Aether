import { useState, useEffect } from 'react';
import { supabase, type Application, type StepProgress, type WorkflowStep, type OfficerAction } from '../lib/supabase';
import { CircleCheck as CheckCircle, Circle as XCircle, Clock, Building2, MessageSquare, Eye } from 'lucide-react';

type Props = {
  selectedState: string;
};

export function EnhancedOfficerDashboard({ selectedState }: Props) {
  const [applications, setApplications] = useState<Application[]>([]);
  const [steps, setSteps] = useState<WorkflowStep[]>([]);
  const [stepProgress, setStepProgress] = useState<Map<string, StepProgress>>(new Map());
  const [loading, setLoading] = useState(true);
  const [selectedApp, setSelectedApp] = useState<Application | null>(null);
  const [actionReason, setActionReason] = useState('');
  const [showRejectModal, setShowRejectModal] = useState(false);

  useEffect(() => {
    loadData();
  }, [selectedState]);

  const loadData = async () => {
    setLoading(true);
    try {
      const { data: apps } = await supabase
        .from('applications')
        .select('*')
        .eq('state', selectedState)
        .order('created_at', { ascending: false });

      const { data: wfSteps } = await supabase
        .from('workflow_steps')
        .select('*')
        .order('step_order');

      const { data: progress } = await supabase
        .from('step_progress')
        .select('*');

      setApplications(apps || []);
      setSteps(wfSteps || []);

      const progressMap = new Map();
      (progress || []).forEach(p => {
        progressMap.set(`${p.application_id}-${p.step_id}`, p);
      });
      setStepProgress(progressMap);
    } catch (error) {
      console.error('Error loading data');
    } finally {
      setLoading(false);
    }
  };

  const handleApproveStep = async (appId: string, stepId: string) => {
    try {
      const key = `${appId}-${stepId}`;
      const existing = stepProgress.get(key);

      if (existing) {
        await supabase
          .from('step_progress')
          .update({ status: 'completed', completed_at: new Date().toISOString() })
          .eq('id', existing.id);
      } else {
        await supabase
          .from('step_progress')
          .insert([{ application_id: appId, step_id: stepId, status: 'completed' }]);
      }

      const step = steps.find(s => s.id === stepId);
      await supabase
        .from('officer_actions')
        .insert([{
          application_id: appId,
          officer_id: 'current_officer',
          action_type: 'approve',
          step_name: step?.step_name || 'Unknown',
          status: 'completed',
          reason: null,
        }]);

      const app = applications.find(a => a.id === appId);
      if (app) {
        await supabase.from('notifications').insert([{
          application_id: appId,
          notification_type: 'step_approved',
          channel: 'sms',
          recipient: app.citizen_phone,
          message_content: `Step "${step?.step_name}" approved. Moving to next step.`,
        }]);
      }

      await loadData();
    } catch (error) {
      console.error('Error approving step');
      alert('Failed to approve step');
    }
  };

  const handleRejectStep = async (appId: string, stepId: string) => {
    if (!actionReason) {
      alert('Please provide a rejection reason');
      return;
    }

    try {
      const key = `${appId}-${stepId}`;
      const existing = stepProgress.get(key);

      if (existing) {
        await supabase
          .from('step_progress')
          .update({ status: 'rejected', notes: actionReason })
          .eq('id', existing.id);
      } else {
        await supabase
          .from('step_progress')
          .insert([{
            application_id: appId,
            step_id: stepId,
            status: 'rejected',
            notes: actionReason,
          }]);
      }

      const step = steps.find(s => s.id === stepId);
      await supabase
        .from('officer_actions')
        .insert([{
          application_id: appId,
          officer_id: 'current_officer',
          action_type: 'reject',
          step_name: step?.step_name || 'Unknown',
          status: 'completed',
          reason: actionReason,
        }]);

      const app = applications.find(a => a.id === appId);
      if (app) {
        await supabase.from('notifications').insert([{
          application_id: appId,
          notification_type: 'step_rejected',
          channel: 'email',
          recipient: app.citizen_email,
          message_content: `Step "${step?.step_name}" rejected. Reason: ${actionReason}`,
        }]);
      }

      setShowRejectModal(false);
      setActionReason('');
      await loadData();
    } catch (error) {
      console.error('Error rejecting step');
      alert('Failed to reject step');
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

  if (selectedApp) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <button
          onClick={() => setSelectedApp(null)}
          className="mb-6 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
        >
          ← Back to Applications
        </button>

        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            {selectedApp.citizen_name}
            <span className="text-sm font-normal text-gray-600 ml-3">
              Ref: {selectedApp.id.slice(0, 8).toUpperCase()}
            </span>
          </h2>
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div className="text-sm">
              <p><span className="font-medium text-gray-700">Email:</span> {selectedApp.citizen_email}</p>
              <p><span className="font-medium text-gray-700">Phone:</span> {selectedApp.citizen_phone}</p>
              <p><span className="font-medium text-gray-700">Aadhaar:</span> {selectedApp.aadhaar_number}</p>
            </div>
            <div className="text-sm">
              <p><span className="font-medium text-gray-700">Property:</span> {selectedApp.property_type} - {selectedApp.property_address}</p>
              <p><span className="font-medium text-gray-700">Value:</span> ₹{selectedApp.property_value.toLocaleString()}</p>
              <p><span className="font-medium text-gray-700">Location:</span> {selectedApp.village}, {selectedApp.district}</p>
            </div>
          </div>
        </div>

        <div className="space-y-4 mb-8">
          <h3 className="font-semibold text-gray-800">Workflow Progress</h3>
          {steps.map((step) => {
            const key = `${selectedApp.id}-${step.id}`;
            const progress = stepProgress.get(key);
            const status = progress?.status || 'pending';

            return (
              <div key={step.id} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-bold">
                        {step.step_order}
                      </span>
                      <div>
                        <h4 className="font-semibold text-gray-800">{step.step_name}</h4>
                        <p className="text-sm text-gray-600">{step.step_description}</p>
                      </div>
                    </div>

                    {progress?.notes && (
                      <p className="text-sm text-gray-700 ml-11 mb-2 bg-white p-2 rounded border border-gray-200">
                        {progress.notes}
                      </p>
                    )}

                    <div className="ml-11 flex gap-2">
                      <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                        status === 'completed' ? 'bg-green-100 text-green-800' :
                        status === 'rejected' ? 'bg-red-100 text-red-800' :
                        status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {status.toUpperCase()}
                      </span>
                      {progress?.completed_at && (
                        <span className="text-xs text-gray-600">
                          {new Date(progress.completed_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>

                  {status === 'pending' && (
                    <div className="flex gap-2 ml-4">
                      <button
                        onClick={() => handleApproveStep(selectedApp.id, step.id)}
                        className="flex items-center gap-1 px-3 py-2 bg-green-600 text-white text-sm rounded hover:bg-green-700 transition-colors"
                      >
                        <CheckCircle className="w-4 h-4" />
                        Approve
                      </button>
                      <button
                        onClick={() => {
                          setSelectedApp(selectedApp);
                          setShowRejectModal(true);
                        }}
                        className="flex items-center gap-1 px-3 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors"
                      >
                        <XCircle className="w-4 h-4" />
                        Reject
                      </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {showRejectModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Rejection Reason</h3>
              <textarea
                value={actionReason}
                onChange={(e) => setActionReason(e.target.value)}
                placeholder="Enter the reason for rejection..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 mb-4"
                rows={4}
              />
              <div className="flex gap-3">
                <button
                  onClick={() => {
                    setShowRejectModal(false);
                    setActionReason('');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleRejectStep(selectedApp.id, steps[0].id)}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Submit Rejection
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Officer Dashboard</h2>

      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-600 font-medium">Total Applications</p>
          <p className="text-3xl font-bold text-blue-900">{applications.length}</p>
        </div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-600 font-medium">Pending Review</p>
          <p className="text-3xl font-bold text-yellow-900">
            {applications.filter(a => {
              const allProgress = Array.from(stepProgress.values())
                .filter(p => p.application_id === a.id);
              return allProgress.some(p => p.status === 'pending');
            }).length}
          </p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-sm text-green-600 font-medium">In Progress</p>
          <p className="text-3xl font-bold text-green-900">
            {applications.filter(a => {
              const allProgress = Array.from(stepProgress.values())
                .filter(p => p.application_id === a.id);
              return allProgress.some(p => p.status === 'in_progress');
            }).length}
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 border-b-2 border-gray-200">
            <tr>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Application ID</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Citizen Name</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Property</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Value</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Current Step</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {applications.map((app) => {
              const appProgress = Array.from(stepProgress.values())
                .filter(p => p.application_id === app.id)
                .sort((a, b) => {
                  const stepA = steps.find(s => s.id === a.step_id)?.step_order || 0;
                  const stepB = steps.find(s => s.id === b.step_id)?.step_order || 0;
                  return stepB - stepA;
                })[0];

              const currentStep = appProgress ? steps.find(s => s.id === appProgress.step_id) : steps[0];
              const statusColor = appProgress?.status === 'completed' ? 'bg-green-100 text-green-800' :
                                 appProgress?.status === 'rejected' ? 'bg-red-100 text-red-800' :
                                 'bg-yellow-100 text-yellow-800';

              return (
                <tr key={app.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-mono text-xs text-gray-600">{app.id.slice(0, 8).toUpperCase()}</td>
                  <td className="py-3 px-4 text-gray-800">{app.citizen_name}</td>
                  <td className="py-3 px-4 text-gray-600 text-xs">{app.property_type}</td>
                  <td className="py-3 px-4 text-gray-600">₹{(app.property_value / 100000).toFixed(1)}L</td>
                  <td className="py-3 px-4">
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {currentStep?.step_name || 'Title Check'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`text-xs px-2 py-1 rounded font-medium ${statusColor}`}>
                      {appProgress?.status.toUpperCase() || 'PENDING'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <button
                      onClick={() => setSelectedApp(app)}
                      className="flex items-center gap-1 px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700 transition-colors"
                    >
                      <Eye className="w-3 h-3" />
                      Review
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
