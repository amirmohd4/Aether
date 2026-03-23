import { useState, useEffect } from 'react';
import { supabase, type Application, type WorkflowStep, type StateRules, type Document, type Notification } from '../lib/supabase';
import { FileText, Upload, Clock, CircleCheck as CheckCircle, CircleAlert as AlertCircle, Phone, Mail } from 'lucide-react';

type Props = {
  selectedState: string;
};

const PROPERTY_TYPES = ['Residential', 'Commercial', 'Agricultural', 'Industrial'];
const OWNERSHIP_TYPES = ['Individual', 'Joint', 'HUF', 'Company'];

export function EnhancedCitizenPortal({ selectedState }: Props) {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    citizen_name: '',
    citizen_email: '',
    citizen_phone: '',
    aadhaar_number: '',
    property_address: '',
    property_size: '',
    property_value: '',
    village: '',
    tehsil: '',
    district: '',
    property_type: '',
    ownership_type: '',
    current_owner: '',
    transferring_to: '',
  });
  const [application, setApplication] = useState<Application | null>(null);
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([]);
  const [stateRules, setStateRules] = useState<StateRules | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, [selectedState]);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const { data: steps } = await supabase
        .from('workflow_steps')
        .select('*')
        .order('step_order');

      const { data: rules } = await supabase
        .from('state_rules')
        .select('*')
        .eq('state', selectedState)
        .single();

      setWorkflowSteps(steps || []);
      setStateRules(rules);
    } catch (error) {
      console.error('Error loading initial data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitApplication = async () => {
    setSubmitting(true);
    try {
      const { data, error } = await supabase
        .from('applications')
        .insert([
          {
            ...formData,
            property_size: parseFloat(formData.property_size),
            property_value: parseFloat(formData.property_value),
            state: selectedState,
          },
        ])
        .select()
        .single();

      if (error) throw error;

      setApplication(data);

      const { data: docsData } = await supabase
        .from('documents')
        .select('*')
        .eq('application_id', data.id);

      setDocuments(docsData || []);

      const { data: notifData } = await supabase
        .from('notifications')
        .select('*')
        .eq('application_id', data.id);

      setNotifications(notifData || []);

      await createInitialNotification(data.id, data.citizen_email, data.citizen_phone);
    } catch (error) {
      console.error('Error submitting application');
      alert('Failed to submit application');
    } finally {
      setSubmitting(false);
    }
  };

  const createInitialNotification = async (appId: string, email: string, phone: string) => {
    const systemRef = `REF-${Date.now()}`;

    await supabase.from('notifications').insert([
      {
        application_id: appId,
        notification_type: 'application_submitted',
        channel: 'email',
        recipient: email,
        message_content: `Your property registration application ${systemRef} has been submitted successfully. Expected processing time: ${stateRules?.processing_days} days.`,
      },
      {
        application_id: appId,
        notification_type: 'application_submitted',
        channel: 'sms',
        recipient: phone,
        message_content: `GovOS: Application ${systemRef.slice(-8)} submitted. Status updates via SMS & email.`,
      },
    ]);
  };

  const handleDocumentUpload = async (e: React.ChangeEvent<HTMLInputElement>, docType: string) => {
    const file = e.target.files?.[0];
    if (!file || !application) return;

    try {
      const { data, error } = await supabase
        .from('documents')
        .insert([
          {
            application_id: application.id,
            document_type: docType,
            document_name: file.name,
            file_size: file.size,
            upload_status: 'uploaded',
          },
        ])
        .select()
        .single();

      if (error) throw error;

      setDocuments([...documents, data]);

      await supabase.from('notifications').insert([
        {
          application_id: application.id,
          notification_type: 'document_uploaded',
          channel: 'sms',
          recipient: application.citizen_phone,
          message_content: `Document ${docType} uploaded successfully.`,
        },
      ]);
    } catch (error) {
      console.error('Error uploading document');
      alert('Failed to upload document');
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <Clock className="w-12 h-12 text-blue-600 mx-auto mb-4 animate-spin" />
        <p className="text-gray-600">Loading application form...</p>
      </div>
    );
  }

  if (application) {
    const uploadedDocs = documents.filter(d => d.upload_status === 'uploaded');
    const requiredDocs = stateRules?.document_requirements || [];

    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="text-center mb-8">
          <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Application Submitted!</h2>
          <p className="text-lg text-gray-600 mb-4">Reference: {application.id.slice(0, 8).toUpperCase()}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-start gap-3">
              <Mail className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <p className="font-medium text-blue-900">Email Notifications</p>
                <p className="text-sm text-blue-700">{application.citizen_email}</p>
              </div>
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-200">
            <div className="flex items-start gap-3">
              <Phone className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <p className="font-medium text-green-900">SMS Updates</p>
                <p className="text-sm text-green-700">{application.citizen_phone}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Upload className="w-5 h-5 text-blue-600" />
            Document Upload ({uploadedDocs.length}/{requiredDocs.length})
          </h3>
          <div className="space-y-3">
            {requiredDocs.map((docType) => {
              const uploaded = documents.find(d => d.document_type === docType);
              return (
                <div key={docType} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-gray-600" />
                      <div>
                        <p className="font-medium text-gray-800">{docType}</p>
                        {uploaded && (
                          <p className="text-sm text-green-600">Uploaded: {uploaded.document_name}</p>
                        )}
                      </div>
                    </div>
                    {!uploaded && (
                      <label className="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer hover:bg-blue-700 transition-colors">
                        Upload
                        <input
                          type="file"
                          className="hidden"
                          onChange={(e) => handleDocumentUpload(e, docType)}
                        />
                      </label>
                    )}
                    {uploaded && <CheckCircle className="w-5 h-5 text-green-600" />}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="mb-8">
          <h3 className="font-semibold text-gray-800 mb-4">Workflow Progress</h3>
          <div className="space-y-2">
            {workflowSteps.map((ws, idx) => (
              <div key={ws.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  {idx + 1}
                </div>
                <div className="flex-grow">
                  <p className="font-medium text-gray-800">{ws.step_name}</p>
                  <p className="text-sm text-gray-600">{ws.step_description}</p>
                </div>
                <span className="text-xs font-semibold px-3 py-1 rounded-full bg-yellow-100 text-yellow-800">
                  {ws.required_days}d
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6">
          <div className="flex gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-amber-800">
              <p className="font-medium mb-1">Expected Processing Time</p>
              <p>Total: {stateRules?.processing_days} days for {selectedState}</p>
              <p className="mt-2 font-medium">Stamp Duty Rate: {stateRules?.stamp_duty_rate}%</p>
              <p className="text-xs mt-1">{stateRules?.stamp_duty_slab}</p>
            </div>
          </div>
        </div>

        {notifications.length > 0 && (
          <div className="mb-6">
            <h3 className="font-semibold text-gray-800 mb-3">Notifications Sent</h3>
            <div className="space-y-2">
              {notifications.slice(-3).map((notif) => (
                <div key={notif.id} className="text-sm p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-start gap-2">
                    {notif.channel === 'email' ? (
                      <Mail className="w-4 h-4 text-blue-600 mt-0.5" />
                    ) : (
                      <Phone className="w-4 h-4 text-green-600 mt-0.5" />
                    )}
                    <div className="flex-grow">
                      <p className="font-medium text-gray-700">{notif.notification_type}</p>
                      <p className="text-gray-600">{notif.message_content.substring(0, 100)}...</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(notif.sent_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  const steps = [
    { title: 'Personal Information', icon: FileText },
    { title: 'Property Details', icon: FileText },
    { title: 'Ownership & Transfer', icon: FileText },
    { title: 'Review & Submit', icon: CheckCircle },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-8">Property Registration Application</h2>

      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          {steps.map((s, idx) => (
            <div key={idx} className="flex flex-col items-center flex-1">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold mb-2 ${
                  idx <= step
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {idx + 1}
              </div>
              <p className={`text-xs text-center font-medium ${idx <= step ? 'text-blue-600' : 'text-gray-600'}`}>
                {s.title}
              </p>
              {idx < steps.length - 1 && (
                <div
                  className={`w-full h-1 mt-2 ${
                    idx < step ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {step === 0 && (
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            value={formData.citizen_name}
            onChange={(e) => setFormData({ ...formData, citizen_name: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="email"
            placeholder="Email Address"
            value={formData.citizen_email}
            onChange={(e) => setFormData({ ...formData, citizen_email: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="tel"
            placeholder="Phone Number"
            value={formData.citizen_phone}
            onChange={(e) => setFormData({ ...formData, citizen_phone: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Aadhaar Number (XXXX-XXXX-XXXX)"
            value={formData.aadhaar_number}
            onChange={(e) => setFormData({ ...formData, aadhaar_number: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )}

      {step === 1 && (
        <div className="space-y-4">
          <textarea
            placeholder="Property Address"
            value={formData.property_address}
            onChange={(e) => setFormData({ ...formData, property_address: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
          <input
            type="number"
            placeholder="Property Size (sq.ft)"
            value={formData.property_size}
            onChange={(e) => setFormData({ ...formData, property_size: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="number"
            placeholder="Property Value (₹)"
            value={formData.property_value}
            onChange={(e) => setFormData({ ...formData, property_value: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Village"
            value={formData.village}
            onChange={(e) => setFormData({ ...formData, village: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Tehsil"
            value={formData.tehsil}
            onChange={(e) => setFormData({ ...formData, tehsil: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="District"
            value={formData.district}
            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={formData.property_type}
            onChange={(e) => setFormData({ ...formData, property_type: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Property Type</option>
            {PROPERTY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <select
            value={formData.ownership_type}
            onChange={(e) => setFormData({ ...formData, ownership_type: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Ownership Type</option>
            {OWNERSHIP_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <input
            type="text"
            placeholder="Current Owner Name"
            value={formData.current_owner}
            onChange={(e) => setFormData({ ...formData, current_owner: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Transferring To (New Owner)"
            value={formData.transferring_to}
            onChange={(e) => setFormData({ ...formData, transferring_to: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )}

      {step === 3 && (
        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-900"><span className="font-medium">Property Value:</span> ₹{formData.property_value || '0'}</p>
            <p className="text-sm text-blue-900 mt-1">
              <span className="font-medium">Estimated Stamp Duty ({stateRules?.stamp_duty_rate}%):</span> ₹{formData.property_value ? (parseFloat(formData.property_value) * (stateRules?.stamp_duty_rate || 0) / 100).toLocaleString() : '0'}
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 max-h-64 overflow-y-auto">
            <p className="font-medium text-gray-800 mb-3">Application Summary</p>
            <dl className="space-y-2 text-sm">
              <div><dt className="font-medium text-gray-700">Name:</dt><dd className="text-gray-600">{formData.citizen_name}</dd></div>
              <div><dt className="font-medium text-gray-700">Email:</dt><dd className="text-gray-600">{formData.citizen_email}</dd></div>
              <div><dt className="font-medium text-gray-700">Phone:</dt><dd className="text-gray-600">{formData.citizen_phone}</dd></div>
              <div><dt className="font-medium text-gray-700">Property Address:</dt><dd className="text-gray-600">{formData.property_address}</dd></div>
              <div><dt className="font-medium text-gray-700">Property Type:</dt><dd className="text-gray-600">{formData.property_type}</dd></div>
              <div><dt className="font-medium text-gray-700">Ownership Type:</dt><dd className="text-gray-600">{formData.ownership_type}</dd></div>
            </dl>
          </div>
        </div>
      )}

      <div className="flex gap-4 mt-8">
        {step > 0 && (
          <button
            onClick={() => setStep(step - 1)}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors"
          >
            Back
          </button>
        )}
        {step < steps.length - 1 && (
          <button
            onClick={() => setStep(step + 1)}
            className="flex-1 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors disabled:bg-gray-400"
            disabled={step === steps.length - 1}
          >
            Next
          </button>
        )}
        {step === steps.length - 1 && (
          <button
            onClick={handleSubmitApplication}
            disabled={submitting}
            className="flex-1 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors disabled:bg-gray-400"
          >
            {submitting ? 'Submitting...' : 'Submit Application'}
          </button>
        )}
      </div>
    </div>
  );
}
