import { useState, useEffect } from 'react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com';

interface WorkflowStep {
  id: string;
  label: string;
  description: string;
}

export function GlobalDemo() {
  const [selectedCountryCode, setSelectedCountryCode] = useState('in');
  const [selectedServiceId, setSelectedServiceId] = useState('property_registration');
  const [nationalId, setNationalId] = useState('');
  const [propertyParcelId, setPropertyParcelId] = useState('KAR-PROP-0001');
  const [isRunning, setIsRunning] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [currentStepIdx, setCurrentStepIdx] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [executionTimeMs, setExecutionTimeMs] = useState(0);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [resultData, setResultData] = useState<any>(null);

  // Define workflow steps based on service
  const workflowSteps: Record<string, WorkflowStep[]> = {
    property_registration: [
      { id: 'title_audit', label: 'Title Audit & Registry Verification', description: 'Checking property title and ownership records' },
      { id: 'lien_search', label: 'Lien & Encumbrance Search', description: 'Searching for any existing loans or encumbrances' },
      { id: 'fraud_scoring', label: 'AI Land Fraud Risk Scoring', description: 'AI analyzing fraud risk patterns' },
      { id: 'stamp_duty', label: 'Stamp Duty Settlement', description: 'Calculating and settling stamp duty' },
      { id: 'ledger_record', label: 'Digital Registry Ledger Recordation', description: 'Recording in the digital ledger' },
      { id: 'certificate_issue', label: 'e-Ownership Certificate Issued', description: 'Issuing the final certificate' }
    ],
    birth_certificate: [
      { id: 'verify_identity', label: 'Identity Verification', description: 'Verifying the citizen identity' },
      { id: 'hospital_records', label: 'Hospital Record Check', description: 'Checking hospital records' },
      { id: 'generate_certificate', label: 'Generate Certificate', description: 'Generating birth certificate' },
      { id: 'digital_sign', label: 'Digital Signature', description: 'Applying digital signature' }
    ],
    driving_license: [
      { id: 'verify_identity', label: 'Identity Verification', description: 'Verifying applicant identity' },
      { id: 'test_schedule', label: 'Test Scheduling', description: 'Scheduling driving test' },
      { id: 'test_result', label: 'Test Result Verification', description: 'Verifying test results' },
      { id: 'issue_license', label: 'License Issuance', description: 'Issuing driving license' }
    ],
    passport: [
      { id: 'police_verification', label: 'Police Verification', description: 'Verifying with police records' },
      { id: 'document_check', label: 'Document Check', description: 'Checking all documents' },
      { id: 'issue_passport', label: 'Passport Issuance', description: 'Issuing passport' }
    ],
    business_license: [
      { id: 'name_availability', label: 'Trade Name Availability', description: 'Checking business name availability' },
      { id: 'biometric_auth', label: 'Biometric Authentication', description: 'Authenticating the applicant' },
      { id: 'fee_payment', label: 'Treasury License Fee', description: 'Processing license fee payment' },
      { id: 'issue_certificate', label: 'Certificate of Incorporation', description: 'Issuing incorporation certificate' }
    ],
    court_case: [
      { id: 'filing', label: 'Case Filing', description: 'Filing court case' },
      { id: 'review', label: 'Judicial Review', description: 'Reviewing the case' },
      { id: 'hearing', label: 'Hearing Scheduling', description: 'Scheduling hearing' },
      { id: 'resolution', label: 'Case Resolution', description: 'Resolving the case' }
    ]
  };

  const currentServiceSteps = workflowSteps[selectedServiceId] || workflowSteps.property_registration;
  const progress = currentStepIdx / (currentServiceSteps.length - 1);

  const startWorkflow = async () => {
    if (isRunning) return;
    setIsRunning(true);
    setIsCompleted(false);
    setCurrentStepIdx(0);
    setCompletedSteps([]);
    setResultData(null);
    setWorkflowId(null);

    // Validate inputs
    if (!nationalId || nationalId.length < 6) {
      alert('Please enter a valid National ID / Digital ID');
      setIsRunning(false);
      return;
    }

    try {
      // Start the workflow via API
      const response = await fetch(`${BACKEND_URL}/api/workflow/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_id: selectedServiceId,
          country: selectedCountryCode,
          state: 'karnataka', // will be dynamic later
          national_id: nationalId,
          property_id: propertyParcelId
        })
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to start workflow');
      }

      const data = await response.json();
      setWorkflowId(data.workflow_id);

      // Poll for status
      const interval = setInterval(async () => {
        try {
          const statusRes = await fetch(`${BACKEND_URL}/api/workflow/${data.workflow_id}`);
          if (!statusRes.ok) {
            clearInterval(interval);
            setIsRunning(false);
            alert('Workflow failed');
            return;
          }
          const statusData = await statusRes.json();
          const progressPercent = statusData.progress_percentage || 0;
          const stepIndex = Math.floor((progressPercent / 100) * (currentServiceSteps.length - 1));
          
          if (stepIndex > currentStepIdx) {
            setCurrentStepIdx(stepIndex);
            setCompletedSteps(prev => [...prev, stepIndex]);
          }

          if (statusData.status === 'completed') {
            clearInterval(interval);
            setIsRunning(false);
            setIsCompleted(true);
            setExecutionTimeMs(Date.now() - startTime);
            setResultData({
              reference: `REF-${Math.floor(Math.random() * 1000000)}`,
              issuedAt: new Date().toLocaleString(),
              service: currentServiceSteps[currentServiceSteps.length - 1]?.label || 'Certificate'
            });
          } else if (statusData.status === 'failed') {
            clearInterval(interval);
            setIsRunning(false);
            alert('Workflow failed. Please try again.');
          }
        } catch (error) {
          console.error('Polling error:', error);
          clearInterval(interval);
          setIsRunning(false);
        }
      }, 1500);

      const startTime = Date.now();

      // Simulate steps for demo if backend doesn't have all steps
      // This will be removed once backend fully supports step updates
      let demoStep = 0;
      const demoInterval = setInterval(() => {
        if (demoStep < currentServiceSteps.length - 1 && isRunning) {
          demoStep += 1;
          setCurrentStepIdx(demoStep);
          setCompletedSteps(prev => [...prev, demoStep]);
        }
      }, 2000);

      // Cleanup intervals after completion
      setTimeout(() => {
        clearInterval(demoInterval);
      }, 10000);

    } catch (error: any) {
      console.error('Error starting workflow:', error);
      alert('Error starting workflow: ' + error.message);
      setIsRunning(false);
    }
  };

  const resetDemo = () => {
    setIsRunning(false);
    setIsCompleted(false);
    setCurrentStepIdx(0);
    setCompletedSteps([]);
    setExecutionTimeMs(0);
    setWorkflowId(null);
    setResultData(null);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
        <div className="space-y-4">
          {/* Service Selection (simplified) */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Service</label>
            <select
              value={selectedServiceId}
              onChange={(e) => setSelectedServiceId(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="property_registration">Property Registration & Title Deed</option>
              <option value="birth_certificate">Birth Certificate</option>
              <option value="driving_license">Driving License</option>
              <option value="passport">Passport Application</option>
              <option value="business_license">Business License</option>
              <option value="court_case">Court Case Filing</option>
            </select>
          </div>

          {/* ID Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700">National ID / Digital ID</label>
            <input
              type="text"
              value={nationalId}
              onChange={(e) => setNationalId(e.target.value)}
              placeholder="Enter your National ID..."
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div className="flex gap-3">
            <button
              onClick={startWorkflow}
              disabled={isRunning || !nationalId}
              className={`px-6 py-2 rounded-lg font-semibold ${isRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white'}`}
            >
              {isRunning ? 'Processing...' : 'Run Workflow'}
            </button>
            <button
              onClick={resetDemo}
              className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
            >
              Reset
            </button>
          </div>
        </div>

        {isRunning && (
          <div className="mt-6">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{Math.round(progress * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" style={{ width: `${progress * 100}%` }}></div>
            </div>
            <div className="mt-4 space-y-2">
              {currentServiceSteps.map((step, idx) => (
                <div key={step.id} className="flex items-center gap-3">
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${idx <= currentStepIdx ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${idx <= currentStepIdx ? 'text-gray-900' : 'text-gray-400'}`}>{step.label}</p>
                    <p className={`text-xs ${idx <= currentStepIdx ? 'text-gray-600' : 'text-gray-400'}`}>{step.description}</p>
                  </div>
                  {idx <= currentStepIdx && <span className="text-green-500 text-sm">✓</span>}
                </div>
              ))}
            </div>
          </div>
        )}

        {isCompleted && resultData && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center gap-2 text-green-800 mb-2">
              <span className="text-xl">✅</span>
              <span className="font-semibold">Request Completed</span>
            </div>
            <p className="text-sm text-gray-700">Your request for <strong>{resultData.service}</strong> has been successfully processed and approved.</p>
            <div className="mt-2 text-xs text-gray-500">
              <p>Service: {resultData.service}</p>
              <p>Country: {selectedCountryCode.toUpperCase()}</p>
              <p>Reference Number: {resultData.reference}</p>
              <p>Issued: {resultData.issuedAt}</p>
              <p className="mt-1 text-green-600">✔️ Sovereign Verified</p>
            </div>
            <button onClick={resetDemo} className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
              Done
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
