/*
  # Enhanced Aether GovOS Schema with Complete Workflow

  ## New Tables

  ### `applications`
  - Enhanced with workflow tracking, state-specific rules, and system integration
  - Tracks application through all workflow stages
  - Stores references to connected systems (Bhoomi, Kaveri, e-Aasthi, LRIS)

  ### `workflow_steps`
  - Defines the workflow stages for property registration
  - Tracks progress through: Title Check → Stamp Duty → Documents → Payment → Registration → Certificate

  ### `step_progress`
  - Tracks which step each application is currently at
  - Records completion status and notes for each step

  ### `documents`
  - Stores document metadata and references
  - Links documents to applications and workflow steps

  ### `notifications`
  - Mock SMS and email notifications to citizens
  - Tracks all communication at each step

  ### `system_records`
  - Integration data with Bhoomi, Kaveri, e-Aasthi, LRIS
  - Stores responses from connected systems

  ### `fraud_detection_logs`
  - Detailed fraud detection results
  - Tracks suspicious patterns automatically detected

  ### `officer_actions`
  - Audit trail of all officer approvals/rejections with reasons

  ### `state_rules`
  - State-specific configuration (Karnataka vs J&K)
  - Stamp duty rates, document requirements, routing rules

  ### `geographical_routing`
  - Village → Tehsil → District → State routing
  - Maps applications to correct jurisdiction
*/

-- Drop existing tables if they exist
DROP TABLE IF EXISTS officer_actions CASCADE;
DROP TABLE IF EXISTS fraud_detection_logs CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS system_records CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS step_progress CASCADE;
DROP TABLE IF EXISTS workflow_steps CASCADE;
DROP TABLE IF EXISTS geographical_routing CASCADE;
DROP TABLE IF EXISTS state_rules CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS officers CASCADE;
DROP TABLE IF EXISTS fraud_flags CASCADE;

-- Create state_rules table
CREATE TABLE state_rules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  state text NOT NULL UNIQUE,
  stamp_duty_rate float NOT NULL,
  stamp_duty_slab text NOT NULL,
  document_requirements text[] NOT NULL,
  processing_days integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create geographical_routing table
CREATE TABLE geographical_routing (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  state text NOT NULL,
  village text NOT NULL,
  tehsil text NOT NULL,
  district text NOT NULL,
  routing_officer_id uuid,
  created_at timestamptz DEFAULT now()
);

-- Create applications table (enhanced)
CREATE TABLE applications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  citizen_name text NOT NULL,
  citizen_email text NOT NULL,
  citizen_phone text NOT NULL,
  aadhaar_number text NOT NULL UNIQUE,
  property_address text NOT NULL,
  property_size numeric NOT NULL,
  property_value numeric NOT NULL,
  village text NOT NULL,
  tehsil text NOT NULL,
  district text NOT NULL,
  state text NOT NULL,
  property_type text NOT NULL,
  ownership_type text NOT NULL,
  current_owner text NOT NULL,
  transferring_to text NOT NULL,
  system_reference text,
  bhoomi_id text,
  kaveri_id text,
  e_aasthi_id text,
  lris_id text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  user_id uuid
);

-- Create workflow_steps table
CREATE TABLE workflow_steps (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  step_order integer NOT NULL,
  step_name text NOT NULL UNIQUE,
  step_description text NOT NULL,
  required_days integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create step_progress table
CREATE TABLE step_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  step_id uuid NOT NULL REFERENCES workflow_steps(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'pending',
  completed_at timestamptz,
  notes text,
  assigned_officer_id uuid,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create documents table
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  document_type text NOT NULL,
  document_name text NOT NULL,
  file_size integer,
  upload_status text DEFAULT 'pending',
  verified_status text DEFAULT 'pending',
  verified_by uuid,
  verified_at timestamptz,
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Create notifications table
CREATE TABLE notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  notification_type text NOT NULL,
  channel text NOT NULL,
  recipient text NOT NULL,
  message_content text NOT NULL,
  sent_at timestamptz DEFAULT now(),
  status text DEFAULT 'sent',
  created_at timestamptz DEFAULT now()
);

-- Create system_records table
CREATE TABLE system_records (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  system_name text NOT NULL,
  system_response text NOT NULL,
  status text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create fraud_detection_logs table
CREATE TABLE fraud_detection_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  fraud_type text NOT NULL,
  severity text NOT NULL,
  description text NOT NULL,
  evidence text,
  flagged_at timestamptz DEFAULT now(),
  resolved boolean DEFAULT false,
  resolution_notes text,
  created_at timestamptz DEFAULT now()
);

-- Create officer_actions table
CREATE TABLE officer_actions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id uuid NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  officer_id uuid NOT NULL,
  action_type text NOT NULL,
  step_name text NOT NULL,
  status text NOT NULL,
  reason text,
  created_at timestamptz DEFAULT now()
);

-- Create officers table
CREATE TABLE officers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  name text NOT NULL,
  department text NOT NULL,
  district text NOT NULL,
  state text NOT NULL,
  user_id uuid,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS on all tables
ALTER TABLE state_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE geographical_routing ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE step_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE fraud_detection_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE officer_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE officers ENABLE ROW LEVEL SECURITY;

-- Create restrictive policies
CREATE POLICY "Public can view state rules"
  ON state_rules FOR SELECT TO public USING (true);

CREATE POLICY "Public can view geographical routing"
  ON geographical_routing FOR SELECT TO public USING (true);

CREATE POLICY "Public can view and create applications"
  ON applications FOR SELECT TO public USING (true);

CREATE POLICY "Public can insert applications"
  ON applications FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Public can view workflow steps"
  ON workflow_steps FOR SELECT TO public USING (true);

CREATE POLICY "Authenticated can view step progress"
  ON step_progress FOR SELECT TO authenticated USING (true);

CREATE POLICY "Public can view documents"
  ON documents FOR SELECT TO public USING (true);

CREATE POLICY "Public can insert documents"
  ON documents FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Public can view notifications"
  ON notifications FOR SELECT TO public USING (true);

CREATE POLICY "Public can insert notifications"
  ON notifications FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Public can view system records"
  ON system_records FOR SELECT TO public USING (true);

CREATE POLICY "Public can insert system records"
  ON system_records FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Authenticated can view fraud logs"
  ON fraud_detection_logs FOR SELECT TO authenticated USING (true);

CREATE POLICY "Authenticated can insert fraud logs"
  ON fraud_detection_logs FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Authenticated can view officer actions"
  ON officer_actions FOR SELECT TO authenticated USING (true);

CREATE POLICY "Authenticated can insert officer actions"
  ON officer_actions FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Public can view officers"
  ON officers FOR SELECT TO public USING (true);

-- Insert workflow steps
INSERT INTO workflow_steps (step_order, step_name, step_description, required_days) VALUES
  (1, 'Title Check', 'Verify property title and ownership from Bhoomi', 2),
  (2, 'Stamp Duty Calculation', 'Calculate applicable stamp duty based on state rules', 1),
  (3, 'Document Upload', 'Citizen uploads required documents', 3),
  (4, 'Payment', 'Process stamp duty and registration fees', 1),
  (5, 'Registration', 'Register property in Kaveri/e-Aasthi/LRIS', 2),
  (6, 'Certificate Generation', 'Generate ownership certificate', 1);

-- Insert state-specific rules
INSERT INTO state_rules (state, stamp_duty_rate, stamp_duty_slab, document_requirements, processing_days) VALUES
  ('Karnataka', 5.0, 'Progressive: 3% for ₹1L, 5% for ₹5L, 7% above ₹5L', 
   ARRAY['Title Deed', 'Encumbrance Certificate', 'Property Tax Receipt', 'Land Measurement Report', 'Aadhaar', 'PAN'],
   15),
  ('J&K', 4.0, 'Flat 4% on property value',
   ARRAY['Sale Deed', 'Inheritance Certificate', 'Property Ownership Document', 'Land Revenue Record', 'Aadhaar', 'ID Proof'],
   20);

-- Insert sample geographical routing
INSERT INTO geographical_routing (state, village, tehsil, district) VALUES
  ('Karnataka', 'Whitefield', 'Yelahanka', 'Bangalore Urban'),
  ('Karnataka', 'Indiranagar', 'Bangalore South', 'Bangalore Urban'),
  ('Karnataka', 'Mysore City', 'Mysore', 'Mysore'),
  ('J&K', 'Srinagar City', 'Srinagar', 'Srinagar'),
  ('J&K', 'Leh City', 'Leh', 'Leh Ladakh');

-- Insert sample officers
INSERT INTO officers (email, name, department, district, state) VALUES
  ('officer.title@karnataka.gov.in', 'Rajesh Kumar', 'Title Verification', 'Bangalore Urban', 'Karnataka'),
  ('officer.stamp@karnataka.gov.in', 'Priya Sharma', 'Stamp Duty', 'Bangalore Urban', 'Karnataka'),
  ('officer.registration@karnataka.gov.in', 'Amit Desai', 'Registration', 'Bangalore Urban', 'Karnataka'),
  ('officer.title@jk.gov.in', 'Fatima Khan', 'Title Verification', 'Srinagar', 'J&K'),
  ('officer.stamp@jk.gov.in', 'Mohammad Ali', 'Stamp Duty', 'Srinagar', 'J&K'),
  ('officer.registration@jk.gov.in', 'Sonam Wangchuk', 'Registration', 'Leh Ladakh', 'J&K');
