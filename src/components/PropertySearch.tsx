import { useState, useEffect } from 'react';
import { propertyAPI, workflowAPI, fraudAPI, Property } from '../lib/api';
import { Search, Building, MapPin, DollarSign, FileText, AlertCircle, CheckCircle, Clock } from 'lucide-react';

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

          <div className="flex gap-4 mb-6">
            <button
              onClick={startWorkflow}
              disabled={loading || (workflowStatus && workflowStatus.status !== 'completed')}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
              data-testid="start-workflow-btn"
            >
              <FileText className="w-4 h-4 inline mr-2" />
              Start Registration Workflow
            </button>
            
            <button
              onClick={checkFraud}
              disabled={loading}
              className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50"
              data-testid="check-fraud-btn"
            >
              <AlertCircle className="w-4 h-4 inline mr-2" />
              Check Fraud
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
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
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
        </div>
      )}
    </div>
  );
}