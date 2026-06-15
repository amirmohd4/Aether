// API base URL - using relative path for same origin
const API_BASE_URL = 'https://aether-backend.onrender.com/api';
// Generic API call function
async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `https://aether-backend.onrender.com/api${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.message || `API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
}

// Property APIs
export const propertyAPI = {
  getProperty: (propertyId: string) => 
    apiCall(`/property/${propertyId}`),
  
  searchByState: (state: string, limit = 20, offset = 0) =>
    apiCall(`/property/search/by-state/${state}?limit=${limit}&offset=${offset}`),
  
  searchByDistrict: (district: string, limit = 20, offset = 0) =>
    apiCall(`/property/search/by-district/${district}?limit=${limit}&offset=${offset}`),
  
  verifyTitle: (propertyId: string) =>
    apiCall(`/property/verify-title/${propertyId}`, { method: 'POST' }),
  
  checkEncumbrance: (propertyId: string) =>
    apiCall(`/property/check-encumbrance/${propertyId}`, { method: 'POST' }),
};

// Workflow APIs
export const workflowAPI = {
  start: (data: { property_id: string; citizen_id: string; workflow_type?: string }) =>
    apiCall('/workflow/start', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  getStatus: (workflowId: string) =>
    apiCall(`/workflow/${workflowId}`),
  
  processNext: (workflowId: string) =>
    apiCall(`/workflow/${workflowId}/process-next`, { method: 'POST' }),
  
  reject: (workflowId: string, reason: string) =>
    apiCall(`/workflow/${workflowId}/reject?reason=${encodeURIComponent(reason)}`, {
      method: 'POST',
    }),
  
  approveManualReview: (workflowId: string) =>
    apiCall(`/workflow/${workflowId}/approve-manual-review`, { method: 'POST' }),
  
  getByProperty: (propertyId: string) =>
    apiCall(`/workflow/list/by-property/${propertyId}`),
};

// Fraud Detection APIs
export const fraudAPI = {
  detect: (propertyId: string, workflowId?: string) => {
    const url = workflowId 
      ? `/fraud/detect/${propertyId}?workflow_id=${workflowId}`
      : `/fraud/detect/${propertyId}`;
    return apiCall(url, { method: 'POST' });
  },
  
  getAlert: (fraudId: string) =>
    apiCall(`/fraud/alert/${fraudId}`),
  
  resolve: (fraudId: string, resolutionNotes: string) =>
    apiCall(`/fraud/alert/${fraudId}/resolve?resolution_notes=${encodeURIComponent(resolutionNotes)}`, {
      method: 'POST',
    }),
  
  getByProperty: (propertyId: string) =>
    apiCall(`/fraud/alerts/by-property/${propertyId}`),
  
  getHighRisk: () =>
    apiCall('/fraud/alerts/high-risk'),
  
  trainModel: () =>
    apiCall('/fraud/train-model', { method: 'POST' }),
};

// Certificate APIs
export const certificateAPI = {
  get: (certificateId: string) =>
    apiCall(`/certificate/${certificateId}`),
  
  getByCitizen: (citizenId: string) =>
    apiCall(`/certificate/by-citizen/${citizenId}`),
};

// System APIs
export const systemAPI = {
  health: () =>
    apiCall('/system/health'),
  
  stateInfo: () =>
    apiCall('/system/state-info'),
  
  stats: () =>
    apiCall('/system/stats'),
  
  marketplace: () =>
    apiCall('/system/api-marketplace'),
  
  connectorsStatus: () =>
    apiCall('/system/connectors/status'),
};

// Land Ecosystem APIs
export const landEcosystemAPI = {
  // Mutation
  startMutation: (data: { property_id: string; new_owner: string; transfer_type?: string }) =>
    apiCall('/workflow/mutation/start', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  getMutationStatus: (mutationId: string) =>
    apiCall(`/workflow/mutation/${mutationId}/status`),
  
  // Encumbrance Certificate
  generateEC: (data: { property_id: string; years?: number }) =>
    apiCall('/workflow/ec/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  getEC: (ecId: string) =>
    apiCall(`/workflow/ec/${ecId}`),
  
  getECHistory: (propertyId: string) =>
    apiCall(`/workflow/ec/property/${propertyId}/history`),
  
  // Land Use Conversion
  startConversion: (data: { property_id: string; target_use: string }) =>
    apiCall('/workflow/conversion/start', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  getConversionStatus: (conversionId: string) =>
    apiCall(`/workflow/conversion/${conversionId}/status`),
  
  // Title Verification
  verifyTitle: (data: { property_id: string; owner_aadhaar?: string }) =>
    apiCall('/workflow/title/verify', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  
  getTitleVerification: (verificationId: string) =>
    apiCall(`/workflow/title/${verificationId}`),
};

// Types
export interface Property {
  property_id: string;
  state: string;
  location: string;
  district: string;
  owner: string;
  title_status: string;
  property_value: number;
  property_size: number;
  property_type: string;
}

export interface Workflow {
  workflow_id: string;
  property_id: string;
  citizen_id: string;
  workflow_type: string;
  current_step: string;
  status: string;
  progress_percentage: number;
  steps_completed: any[];
  steps_pending: any[];
  started_at: string;
  completed_at?: string;
}

export interface FraudAlert {
  fraud_id: string;
  property_id: string;
  fraud_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  severity_color: string;
  fraud_score: number;
  description: string;
  explanation: string;
  evidence: any;
  flagged_at: string;
  resolved: boolean;
}
