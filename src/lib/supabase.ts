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
  aadhaar_number: string;
  property_address: string;
  district: string;
  state: string;
  status: 'submitted' | 'verified' | 'approved' | 'rejected' | 'completed';
  department: string;
  user_id: string | null;
  created_at: string;
  updated_at: string;
};

export type FraudFlag = {
  id: string;
  application_id: string;
  flag_type: string;
  description: string;
  created_at: string;
};

export type Officer = {
  id: string;
  email: string;
  name: string;
  department: string;
  user_id: string | null;
  created_at: string;
};
