import { useState, useEffect } from 'react';
import { propertyAPI, workflowAPI, fraudAPI, landEcosystemAPI, Property } from '../lib/api';
import { Search, Building, MapPin, DollarSign, FileText, AlertCircle, CheckCircle, Clock, RefreshCw, FileCheck, Landmark, Shield } from 'lucide-react';

interface Props {
  selectedState: string;
}

export function PropertySearch({ selectedState }: Props) {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedProperty, setSelectedProperty] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [workflowStatus, setWorkflowStatus] = useState<any>(null);
  const [fraudResult, setFraudResult] = useState<any>(null);
  const [mutationResult, setMutationResult] = useState<any>(null);
  const [ecResult, setECResult] = useState<any>(null);
  const [conversionResult, setConversionResult] = useState<any>(null);
  const [titleResult, setTitleResult] = useState<any>(null);
  const [ecHistory, setECHistory] = useState<any[]>([]);

  useEffect(() => {
    loadProperties();
  }, [selectedState]);

  const loadProperties = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await propertyAPI.searchByState(selectedState, 10);
      setProperties(data as Property[]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPropertyDetails = async (propertyId: string) => {
    setLoading(true);
    try {
      const data = await propertyAPI.getProperty(propertyId);
      setSelectedProperty(data);
      
      // Check for existing workflows
      const workflows = await workflowAPI.getByProperty(propertyId);
      if (workflows && workflows.length > 0) {
        const latest = workflows[0];
        const status = await workflowAPI.getStatus(latest.workflow_id);
        setWorkflowStatus(status);
      }
      
      // Load EC history
      try {
        const ecHist = await landEcosystemAPI.getECHistory(propertyId);
        setECHistory(ecHist || []);
      } catch (err) {
        setECHistory([]);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const startWorkflow = async () => {
    if (!selectedProperty) return;
    
    setLoading(true);
    try {
      const result = await workflowAPI.start({
        property_id: selectedProperty.property_id,
        citizen_id: 'CIT-DEMO-001',
        workflow_type: 'property_registration'
      });
      
      setWorkflowStatus(result);
      alert('Workflow started successfully!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const checkFraud = async () => {
    if (!selectedProperty) return;
    
    setLoading(true);
    try {
      const result = await fraudAPI.detect(selectedProperty.property_id);
      setFraudResult(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const applyMutation = async () => {
    if (!selectedProperty) return;
    
    const newOwner = prompt('Enter new owner name:');
    if (!newOwner) return;
    
    setLoading(true);
    try {
      const result = await landEcosystemAPI.startMutation({
        property_id: selectedProperty.property_id,
        new_owner: newOwner,
        transfer_type: 'Sale'
      });
      setMutationResult(result);
      alert('Mutation workflow started successfully!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateEC = async () => {
    if (!selectedProperty) return;
    
    setLoading(true);
    try {
      const result = await landEcosystemAPI.generateEC({
        property_id: selectedProperty.property_id,
        years: 30
      });
      setECResult(result);
      setECHistory([result, ...ecHistory]);
      alert('Encumbrance Certificate generated successfully!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const convertLandUse = async () => {
    if (!selectedProperty) return;
    
    const targetUse = prompt('Enter target land use (residential/commercial/industrial/agricultural):');
    if (!targetUse) return;
    
    setLoading(true);
    try {
      const result = await landEcosystemAPI.startConversion({
        property_id: selectedProperty.property_id,
        target_use: targetUse.toLowerCase()
      });
      setConversionResult(result);
      alert('Land use conversion workflow started!');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const verifyTitle = async () => {
    if (!selectedProperty) return;
    
    setLoading(true);
    try {
      const result = await landEcosystemAPI.verifyTitle({
        property_id: selectedProperty.property_id
      });
      setTitleResult(result);
      alert('Title verification completed!');
    } catch (err: any) {
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

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Property Search</h2>
          <button
            onClick={loadProperties}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            data-testid="refresh-properties-btn"
          >
            <Search className="w-4 h-4 inline mr-2" />
            Refresh
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700">
            <AlertCircle className="w-5 h-5 inline mr-2" />
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {loading && !selectedProperty ? (
            <div className="col-span-3 text-center py-8 text-gray-500">Loading properties...</div>
          ) : (
            properties.map((property) => (
              <div
                key={property.property_id}
                onClick={() => loadPropertyDetails(property.property_id)}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-lg cursor-pointer transition-shadow"
                data-testid="property-card"
              >
                <div className="flex items-start justify-between mb-2">
                  <Building className="w-6 h-6 text-blue-600" />
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    property.title_status === 'clear' ? 'bg-green-100 text-green-800' :
                    property.title_status === 'disputed' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {property.title_status}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{property.property_id}</h3>
                <p className="text-sm text-gray-600 mb-2 flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {property.district}
                </p>
                <p className="text-sm text-gray-600 mb-2">
                  Owner: {property.owner}
                </p>
                <p className="text-lg font-bold text-blue-600">
                  ₹{property.property_value.toLocaleString()}
                </p>
                <p className="text-xs text-gray-500">
                  {property.property_size.toFixed(0)} sq ft • {property.property_type}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {selectedProperty && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Property Details</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Basic Information</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Property ID:</span> {selectedProperty.property_id}</p>
                <p><span className="font-medium">State:</span> {selectedProperty.state}</p>
                <p><span className="font-medium">District:</span> {selectedProperty.district}</p>
                <p><span className="font-medium">Location:</span> {selectedProperty.location}</p>
                <p><span className="font-medium">Owner:</span> {selectedProperty.owner}</p>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Property Details</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Value:</span> ₹{selectedProperty.property_value.toLocaleString()}</p>
                <p><span className="font-medium">Size:</span> {selectedProperty.property_size.toFixed(0)} sq ft</p>
                <p><span className="font-medium">Type:</span> {selectedProperty.property_type}</p>
                <p><span className="font-medium">Title Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    selectedProperty.title_status === 'clear' ? 'bg-green-100 text-green-800' :
                    selectedProperty.title_status === 'disputed' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {selectedProperty.title_status}
                  </span>
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-3 mb-6">
            <button
              onClick={startWorkflow}
              disabled={loading || (workflowStatus && workflowStatus.status !== 'completed')}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="start-workflow-btn"
            >
              <FileText className="w-4 h-4" />
              Start Registration
            </button>
            
            <button
              onClick={checkFraud}
              disabled={loading}
              className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="check-fraud-btn"
            >
              <AlertCircle className="w-4 h-4" />
              Check Fraud
            </button>

            <button
              onClick={applyMutation}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="apply-mutation-btn"
            >
              <RefreshCw className="w-4 h-4" />
              Apply Mutation
            </button>

            <button
              onClick={generateEC}
              disabled={loading}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="generate-ec-btn"
            >
              <FileCheck className="w-4 h-4" />
              Get EC
            </button>

            <button
              onClick={convertLandUse}
              disabled={loading}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="convert-land-btn"
            >
              <Landmark className="w-4 h-4" />
              Convert Land Use
            </button>

            <button
              onClick={verifyTitle}
              disabled={loading}
              className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50 flex items-center gap-2"
              data-testid="verify-title-btn"
            >
              <Shield className="w-4 h-4" />
              Verify Title
            </button>
          </div>

          {workflowStatus && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">Workflow Status</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Workflow ID:</span> {workflowStatus.workflow_id}</p>
                <p><span className="font-medium">Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    workflowStatus.status === 'completed' ? 'bg-green-100 text-green-800' :
                    workflowStatus.status === 'rejected' ? 'bg-red-100 text-red-800' :
                    workflowStatus.status === 'manual_review' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {workflowStatus.status}
                  </span>
                </p>
                <p><span className="font-medium">Current Step:</span> {workflowStatus.current_step}</p>
                <p><span className="font-medium">Progress:</span> {workflowStatus.progress_percentage}%</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${workflowStatus.progress_percentage}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}

          {fraudResult && (
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg mb-6">
              <h4 className="font-semibold text-gray-900 mb-3">Fraud Detection Result</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Fraud Score:</span>
                  <span className={`px-3 py-1 rounded-full text-lg font-bold ${getSeverityColor(fraudResult.fraud_score)}`}>
                    {fraudResult.fraud_score.toFixed(1)}/100
                  </span>
                </div>
                <div>
                  <span className="font-medium">Severity:</span>
                  <span className={`ml-2 px-2 py-1 rounded text-xs uppercase ${getSeverityColor(fraudResult.fraud_score)}`}>
                    {fraudResult.severity}
                  </span>
                </div>
                <div>
                  <p className="font-medium mb-1">Explanation:</p>
                  <p className="text-sm text-gray-700 bg-white p-3 rounded border">{fraudResult.explanation}</p>
                </div>
              </div>
            </div>
          )}

          {mutationResult && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-6">
              <h4 className="font-semibold text-blue-900 mb-3">Mutation Result</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Mutation ID:</span> {mutationResult.mutation_id}</p>
                <p><span className="font-medium">Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    mutationResult.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {mutationResult.status}
                  </span>
                </p>
                <p><span className="font-medium">From:</span> {mutationResult.current_owner}</p>
                <p><span className="font-medium">To:</span> {mutationResult.new_owner}</p>
              </div>
            </div>
          )}

          {ecResult && (
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg mb-6">
              <h4 className="font-semibold text-purple-900 mb-3">Encumbrance Certificate</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">EC ID:</span> {ecResult.ec_id}</p>
                <p><span className="font-medium">Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    ecResult.certificate_status === 'Clear' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {ecResult.certificate_status}
                  </span>
                </p>
                <p><span className="font-medium">Years Covered:</span> {ecResult.years_covered}</p>
                <p><span className="font-medium">Transactions:</span> {ecResult.transactions?.length || 0}</p>
                <p><span className="font-medium">Total Encumbrance:</span> ₹{ecResult.total_encumbrance_amount?.toLocaleString() || 0}</p>
              </div>
            </div>
          )}

          {conversionResult && (
            <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg mb-6">
              <h4 className="font-semibold text-indigo-900 mb-3">Land Conversion Result</h4>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Conversion ID:</span> {conversionResult.conversion_id}</p>
                <p><span className="font-medium">Status:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    conversionResult.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {conversionResult.status}
                  </span>
                </p>
                <p><span className="font-medium">Target Use:</span> {conversionResult.target_use}</p>
                {conversionResult.conversion_fee && (
                  <p><span className="font-medium">Conversion Fee:</span> ₹{conversionResult.conversion_fee.toLocaleString()}</p>
                )}
              </div>
            </div>
          )}

          {titleResult && titleResult.title_report && (
            <div className="p-4 bg-teal-50 border border-teal-200 rounded-lg mb-6">
              <h4 className="font-semibold text-teal-900 mb-3">Title Verification Report</h4>
              <div className="space-y-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Risk Score:</span>
                  <span className={`px-3 py-1 rounded-full text-lg font-bold ${
                    titleResult.title_report.risk_score < 40 ? 'bg-green-100 text-green-800' :
                    titleResult.title_report.risk_score < 70 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {titleResult.title_report.risk_score}/100
                  </span>
                </div>
                <p><span className="font-medium">Risk Level:</span> 
                  <span className="ml-2 px-2 py-1 rounded text-xs bg-white">
                    {titleResult.title_report.risk_level}
                  </span>
                </p>
                <div>
                  <p className="font-medium mb-1">Recommendation:</p>
                  <p className="bg-white p-3 rounded border">{titleResult.title_report.recommendation}</p>
                </div>
                {titleResult.title_report.risk_factors && titleResult.title_report.risk_factors.length > 0 && (
                  <div>
                    <p className="font-medium mb-1">Risk Factors:</p>
                    <ul className="list-disc list-inside bg-white p-3 rounded border">
                      {titleResult.title_report.risk_factors.map((factor: string, idx: number) => (
                        <li key={idx}>{factor}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {ecHistory && ecHistory.length > 0 && (
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="font-semibold text-gray-900 mb-3">EC History</h4>
              <div className="space-y-2">
                {ecHistory.map((ec: any, idx: number) => (
                  <div key={idx} className="p-3 bg-white rounded border text-sm">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{ec.ec_id}</span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        ec.certificate_status === 'Clear' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {ec.certificate_status}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">
                      Issued: {new Date(ec.issue_date).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}