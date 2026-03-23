import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Database configuration incomplete');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export type Application = {
  id: string;
  citizen_name: string;
  citizen_email: string;
  citizen_phone: string;
  aadhaar_number: string;
  property_address: string;
  property_size: number;
  property_value: number;
  village: string;
  tehsil: string;
  district: string;
  state: string;
  property_type: string;
  ownership_type: string;
  current_owner: string;
  transferring_to: string;
  system_reference: string | null;
  bhoomi_id: string | null;
  kaveri_id: string | null;
  e_aasthi_id: string | null;
  lris_id: string | null;
  user_id: string | null;
  created_at: string;
  updated_at: string;
};

export type WorkflowStep = {
  id: string;
  step_order: number;
  step_name: string;
  step_description: string;
  required_days: number;
  created_at: string;
};

export type StepProgress = {
  id: string;
  application_id: string;
  step_id: string;
  status: 'pending' | 'in_progress' | 'completed' | 'rejected';
  completed_at: string | null;
  notes: string | null;
  assigned_officer_id: string | null;
  created_at: string;
  updated_at: string;
};

export type Document = {
  id: string;
  application_id: string;
  document_type: string;
  document_name: string;
  file_size: number | null;
  upload_status: 'pending' | 'uploaded' | 'verified';
  verified_status: 'pending' | 'verified' | 'rejected';
  verified_by: string | null;
  verified_at: string | null;
  notes: string | null;
  created_at: string;
};

export type Notification = {
  id: string;
  application_id: string;
  notification_type: string;
  channel: 'sms' | 'email';
  recipient: string;
  message_content: string;
  sent_at: string;
  status: 'sent' | 'failed' | 'pending';
  created_at: string;
};

export type FraudDetectionLog = {
  id: string;
  application_id: string;
  fraud_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  evidence: string | null;
  flagged_at: string;
  resolved: boolean;
  resolution_notes: string | null;
  created_at: string;
};

export type OfficerAction = {
  id: string;
  application_id: string;
  officer_id: string;
  action_type: 'approve' | 'reject' | 'request_info';
  step_name: string;
  status: 'completed' | 'pending';
  reason: string | null;
  created_at: string;
};

export type Officer = {
  id: string;
  email: string;
  name: string;
  department: string;
  district: string;
  state: string;
  user_id: string | null;
  created_at: string;
};

export type StateRules = {
  id: string;
  state: string;
  stamp_duty_rate: number;
  stamp_duty_slab: string;
  document_requirements: string[];
  processing_days: number;
  created_at: string;
};
