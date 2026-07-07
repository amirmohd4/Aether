import { useState } from 'react';
import { Search, Building, MapPin, AlertCircle, FileText, RefreshCw, FileCheck, Landmark, Shield } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(err.message || `HTTP ${res.status}`);
  }
  return await res.json();
}

interface Property {
  property_id: string;
  district: string;
  owner: string;
  property_value: number;
  property_size: number;
  property_type: string;
  title_status: string;
  state: string;
  location: string;
}

interface WorkflowStatus {
  workflow_id: string;
  status: string;
  current_step: string;
  progress_percentage: number;
}

interface FraudResult {
  fraud_score: number;
  severity: string;
  explanation: string;
}

export function PropertySearch() {
  const [property, setProperty] = useState<Property | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchId, setSearchId] = useState('');
  const [workflowStatus, setWorkflowStatus] = useState<WorkflowStatus | null>(null);
  const [fraudResult, setFraudResult] = useState<FraudResult | null>(null);
  const [mutationResult, setMutationResult] = useState<any>(null);
  const [ecResult, setECResult] = useState<any>(null);
  const [conversionResult, setConversionResult] = useState<any>(null);
  const [titleResult, setTitleResult] = useState<any>(null);

  const handleSearch = async () => {
    if (!searchId.trim()) {
      setError('Please enter a property ID');
      return;
    }
    setLoading(true);
    setError('');
    setProperty(null);
    setWorkflowStatus(null);
    setFraudResult(null);
    setMutationResult(null);
    setECResult(null);
    setConversionResult(null);
    setTitleResult(null);
    try {
      const data = await directFetch<Property>(`/property/${searchId.trim()}`);
      setProperty(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const startWorkflow = async () => {
    if (!property) return;
    setLoading(true);
    try {
      const result = await directFetch<any>('/workflow/start', {
        method: 'POST',
        body: JSON.stringify({
          property_id: property.property_id,
          citizen_id: 'CIT-DEMO-001',
          workflow_type: 'property_registration'
        })
      });
      setWorkflowStatus(result);
      alert('✅ Workflow started successfully!');
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const checkFraud = async () => {
    if (!property) return;
    setLoading(true);
    try {
      const result = await directFetch<FraudResult>(`/fraud/detect/${property.property_id}`, { method: 'POST' });
      setFraudResult(result);
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const applyMutation = async () => {
    if (!property) return;
    const newOwner = prompt('Enter new owner name:');
    if (!newOwner) return;
    setLoading(true);
    try {
      const result = await directFetch<any>('/workflow/mutation/start', {
        method: 'POST',
        body: JSON.stringify({
          property_id: property.property_id,
          new_owner: newOwner,
          transfer_type: 'Sale'
        })
      });
      setMutationResult(result);
      alert('✅ Mutation workflow started!');
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateEC = async () => {
    if (!property) return;
    setLoading(true);
    try {
      const result = await directFetch<any>('/workflow/ec/generate', {
        method: 'POST',
        body: JSON.stringify({
          property_id: property.property_id,
          years: 30
        })
      });
      setECResult(result);
      alert('✅ EC generated!');
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const convertLandUse = async () => {
    if (!property) return;
    const targetUse = prompt('Enter target land use (residential/commercial/industrial/agricultural):');
    if (!targetUse) return;
    setLoading(true);
    try {
      const result = await directFetch<any>('/workflow/conversion/start', {
        method: 'POST',
        body: JSON.stringify({
          property_id: property.property_id,
          target_use: targetUse.toLowerCase()
        })
      });
      setConversionResult(result);
      alert('✅ Land conversion started!');
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const verifyTitle = async () => {
    if (!property) return;
    setLoading(true);
    try {
      const result = await directFetch<any>('/workflow/title/verify', {
        method: 'POST',
        body: JSON.stringify({
          property_id: property.property_id
        })
      });
      setTitleResult(result);
      alert('✅ Title verified!');
    } catch (err: any) {
      alert('❌ Error: ' + err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (score: number) => {
    if (score >= 75) return 'text-red-700 bg-red-100';
    if (score >= 50) return 'text-orange-700 bg-orange-100';
    if (score >= 25) return 'text-yellow-700 bg-yellow-100';
    return 'text-green-700 bg-green-100';
  };

  const getStatusColor = (status: string) => {
    return status === 'clear' ? 'bg-green-100 text-green-800' :
           status === 'disputed' ? 'bg-red-100 text-red-800' :
           'bg-yellow-100 text-yellow-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Centered Search Bar */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-2">Aether GovOS</h1>
        <p className="text-center text-gray-600 mb-6">One API for all government services</p>
        
        <div className="flex gap-3 max-w-2xl mx-auto">
          <input
            type="text"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Enter property ID (e.g., KAR-PROP-0001)"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Search className="w-5 h-5" />
            Search
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700 text-center">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}
      </div>

      {/* Loading indicator */}
      {loading && (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      )}

      {/* Property Details */}
      {property && !loading && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Property Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p><span className="font-medium">Property ID:</span> {property.property_id}</p>
              <p><span className="font-medium">State:</span> {property.state}</p>
              <p><span className="font-medium">District:</span> {property.district}</p>
              <p><span className="font-medium">Location:</span> {property.location}</p>
            </div>
            <div>
              <p><span className="font-medium">Value:</span> ₹{property.property_value.toLocaleString()}</p>
              <p><span className="font-medium">Size:</span> {property.property_size.toFixed(0)} sq ft</p>
              <p><span className="font-medium">Type:</span> {property.property_type}</p>
              <p>
                <span className="font-medium">Title Status:</span>
                <span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(property.title_status)}`}>
                  {property.title_status}
                </span>
              </p>
              <p><span className="font-medium">Owner:</span> {property.owner}</p>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex flex-wrap gap-3 mb-6">
            <button onClick={startWorkflow} disabled={loading} className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2">
              <FileText className="w-4 h-4" /> Start Registration
            </button>
            <button onClick={checkFraud} disabled={loading} className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 flex items-center gap-2">
              <AlertCircle className="w-4 h-4" /> Check Fraud
            </button>
            <button onClick={applyMutation} disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> Apply Mutation
            </button>
            <button onClick={generateEC} disabled={loading} className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2">
              <FileCheck className="w-4 h-4" /> Get EC
            </button>
            <button onClick={convertLandUse} disabled={loading} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
              <Landmark className="w-4 h-4" /> Convert Land Use
            </button>
            <button onClick={verifyTitle} disabled={loading} className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50 flex items-center gap-2">
              <Shield className="w-4 h-4" /> Verify Title
            </button>
          </div>

          {/* Workflow Status */}
          {workflowStatus && (
            <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">Workflow Status</h4>
              <p><span className="font-medium">Workflow ID:</span> {workflowStatus.workflow_id}</p>
              <p><span className="font-medium">Status:</span> <span className="ml-2 px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">{workflowStatus.status}</span></p>
              <p><span className="font-medium">Current Step:</span> {workflowStatus.current_step}</p>
              <p><span className="font-medium">Progress:</span> {workflowStatus.progress_percentage}%</p>
              <div className="w-full bg-gray-200 rounded-full h-2"><div className="bg-blue-600 h-2 rounded-full" style={{ width: `${workflowStatus.progress_percentage}%` }}></div></div>
            </div>
          )}

          {/* Fraud Result */}
          {fraudResult && (
            <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-3">Fraud Detection Result</h4>
              <div className="flex items-center justify-between mb-2"><span className="font-medium">Fraud Score:</span><span className={`px-3 py-1 rounded-full text-lg font-bold ${getSeverityColor(fraudResult.fraud_score)}`}>{fraudResult.fraud_score.toFixed(1)}/100</span></div>
              <p><span className="font-medium">Severity:</span> <span className={`ml-2 px-2 py-1 rounded text-xs uppercase ${getSeverityColor(fraudResult.fraud_score)}`}>{fraudResult.severity}</span></p>
              <p className="font-medium mt-2">Explanation:</p>
              <p className="text-sm text-gray-700 bg-white p-3 rounded border">{fraudResult.explanation}</p>
            </div>
          )}

          {/* Mutation Result */}
          {mutationResult && (
            <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-3">Mutation Result</h4>
              <p><span className="font-medium">Mutation ID:</span> {mutationResult.mutation_id}</p>
              <p><span className="font-medium">Status:</span> <span className="ml-2 px-2 py-1 rounded text-xs bg-green-100 text-green-800">{mutationResult.status}</span></p>
              <p><span className="font-medium">From:</span> {mutationResult.current_owner}</p>
              <p><span className="font-medium">To:</span> {mutationResult.new_owner}</p>
            </div>
          )}

          {/* EC Result */}
          {ecResult && (
            <div className="mb-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
              <h4 className="font-semibold text-purple-900 mb-3">Encumbrance Certificate</h4>
              <p><span className="font-medium">EC ID:</span> {ecResult.ec_id}</p>
              <p><span className="font-medium">Status:</span> <span className="ml-2 px-2 py-1 rounded text-xs bg-green-100 text-green-800">{ecResult.certificate_status}</span></p>
              <p><span className="font-medium">Years Covered:</span> {ecResult.years_covered}</p>
              <p><span className="font-medium">Total Encumbrance:</span> ₹{ecResult.total_encumbrance_amount?.toLocaleString() || 0}</p>
            </div>
          )}

          {/* Conversion Result */}
          {conversionResult && (
            <div className="mb-4 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
              <h4 className="font-semibold text-indigo-900 mb-3">Land Conversion Result</h4>
              <p><span className="font-medium">Conversion ID:</span> {conversionResult.conversion_id}</p>
              <p><span className="font-medium">Status:</span> <span className="ml-2 px-2 py-1 rounded text-xs bg-green-100 text-green-800">{conversionResult.status}</span></p>
              <p><span className="font-medium">Target Use:</span> {conversionResult.target_use}</p>
              {conversionResult.conversion_fee && <p><span className="font-medium">Conversion Fee:</span> ₹{conversionResult.conversion_fee.toLocaleString()}</p>}
            </div>
          )}

          {/* Title Result */}
          {titleResult && titleResult.title_report && (
            <div className="mb-4 p-4 bg-teal-50 border border-teal-200 rounded-lg">
              <h4 className="font-semibold text-teal-900 mb-3">Title Verification Report</h4>
              <div className="flex items-center justify-between"><span className="font-medium">Risk Score:</span><span className={`px-3 py-1 rounded-full text-lg font-bold ${titleResult.title_report.risk_score < 40 ? 'bg-green-100 text-green-800' : titleResult.title_report.risk_score < 70 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>{titleResult.title_report.risk_score}/100</span></div>
              <p><span className="font-medium">Risk Level:</span> {titleResult.title_report.risk_level}</p>
              <p><span className="font-medium">Recommendation:</span> {titleResult.title_report.recommendation}</p>
              {titleResult.title_report.risk_factors?.length > 0 && (
                <div><p className="font-medium">Risk Factors:</p><ul className="list-disc list-inside bg-white p-3 rounded border">{titleResult.title_report.risk_factors.map((f: string, i: number) => <li key={i}>{f}</li>)}</ul></div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
