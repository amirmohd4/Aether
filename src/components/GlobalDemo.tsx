import { useState } from 'react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com';

export function GlobalDemo() {
  const [serviceId, setServiceId] = useState('property_registration');
  const [nationalId, setNationalId] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [workflowId, setWorkflowId] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const steps = [
    'Title Audit & Registry Verification',
    'Lien & Encumbrance Search',
    'AI Land Fraud Risk Scoring',
    'Stamp Duty Settlement',
    'Digital Registry Ledger Recordation',
    'e-Ownership Certificate Issued'
  ];
  const [currentStep, setCurrentStep] = useState(0);

  const startWorkflow = async () => {
    if (!nationalId || nationalId.length < 6) {
      setError('Please enter a valid National ID');
      return;
    }
    setIsRunning(true);
    setError('');
    setResult(null);
    setCurrentStep(0);

    try {
      const res = await fetch(`${BACKEND_URL}/api/workflow/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_id: serviceId,
          country: 'india',
          state: 'karnataka',
          national_id: nationalId,
          property_id: 'KAR-PROP-0001'
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to start workflow');
      setWorkflowId(data.workflow_id);

      // Poll for status
      let stepIndex = 0;
      const interval = setInterval(async () => {
        try {
          const statusRes = await fetch(`${BACKEND_URL}/api/workflow/${data.workflow_id}`);
          const statusData = await statusRes.json();
          const progress = statusData.progress_percentage || 0;
          const newStep = Math.floor((progress / 100) * (steps.length - 1));
          if (newStep > stepIndex) {
            stepIndex = newStep;
            setCurrentStep(stepIndex);
          }
          if (statusData.status === 'completed') {
            clearInterval(interval);
            setIsRunning(false);
            setIsCompleted(true);
            setResult({
              reference: `REF-${Math.floor(Math.random() * 1000000)}`,
              issuedAt: new Date().toLocaleString()
            });
          } else if (statusData.status === 'failed') {
            clearInterval(interval);
            setIsRunning(false);
            setError('Workflow failed. Please try again.');
          }
        } catch (err) {
          clearInterval(interval);
          setIsRunning(false);
          setError('Error polling status');
        }
      }, 1500);

      // Auto-advance simulation for demo if backend doesn't update fast enough
      let simStep = 0;
      const simInterval = setInterval(() => {
        if (simStep < steps.length - 1 && isRunning) {
          simStep++;
          setCurrentStep(simStep);
        }
      }, 2000);
      setTimeout(() => clearInterval(simInterval), 12000);

    } catch (err) {
      setError(err.message);
      setIsRunning(false);
    }
  };

  const reset = () => {
    setIsRunning(false);
    setIsCompleted(false);
    setCurrentStep(0);
    setResult(null);
    setError('');
    setWorkflowId(null);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Get Your Service</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Service</label>
            <select
              value={serviceId}
              onChange={(e) => setServiceId(e.target.value)}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            >
              <option value="property_registration">Property Registration</option>
              <option value="birth_certificate">Birth Certificate</option>
              <option value="driving_license">Driving License</option>
              <option value="passport">Passport</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">National ID / Digital ID</label>
            <input
              type="text"
              value={nationalId}
              onChange={(e) => setNationalId(e.target.value)}
              placeholder="Enter your National ID..."
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </div>

          {error && <div className="text-red-600 text-sm">{error}</div>}

          <div className="flex gap-3">
            <button
              onClick={startWorkflow}
              disabled={isRunning}
              className={`px-6 py-2 rounded-lg font-semibold ${isRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white'}`}
            >
              {isRunning ? 'Processing...' : 'Run Workflow'}
            </button>
            <button onClick={reset} className="px-6 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">
              Reset
            </button>
          </div>

          {isRunning && (
            <div className="mt-4 space-y-2">
              {steps.map((step, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${idx <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
                    {idx + 1}
                  </div>
                  <span className={`text-sm ${idx <= currentStep ? 'text-gray-800' : 'text-gray-400'}`}>{step}</span>
                  {idx <= currentStep && <span className="text-green-500 ml-auto">✓</span>}
                </div>
              ))}
            </div>
          )}

          {isCompleted && result && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-2 text-green-800 font-semibold">
                <span>✅</span> Request Completed
              </div>
              <p className="text-sm text-gray-700 mt-1">Your request has been successfully processed.</p>
              <div className="mt-2 text-xs text-gray-500">
                <p>Reference: {result.reference}</p>
                <p>Issued: {result.issuedAt}</p>
              </div>
              <button onClick={reset} className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                Done
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
