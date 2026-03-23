/*
  # Add Mock Fraud Detection Data

  ## Sample Data
  - Creates sample applications with fraud flags
  - Adds fraud detection logs for automated testing
  - Includes various fraud types and severity levels
*/

-- Insert sample applications with potential fraud
INSERT INTO applications (
  citizen_name, citizen_email, citizen_phone, aadhaar_number,
  property_address, property_size, property_value,
  village, tehsil, district, state, property_type, ownership_type,
  current_owner, transferring_to
) VALUES
  ('Rajesh Kumar', 'rajesh@email.com', '9876543210', '1111-2222-3333',
   'Plot 45, MG Road', 2500, 5000000,
   'Whitefield', 'Yelahanka', 'Bangalore Urban', 'Karnataka', 'Residential', 'Individual',
   'Suresh Singh', 'Rajesh Kumar'),
  ('Priya Patel', 'priya@email.com', '9876543211', '1111-2222-3333',
   'Flat 102, Commercial Street', 1200, 3000000,
   'Indiranagar', 'Bangalore South', 'Bangalore Urban', 'Karnataka', 'Commercial', 'Joint',
   'Kavya Sharma', 'Priya Patel'),
  ('Mohammad Yusuf', 'yusuf@email.com', '9876543212', '4444-5555-6666',
   'House 15, Lake Road, Srinagar', 3000, 8000000,
   'Srinagar City', 'Srinagar', 'Srinagar', 'J&K', 'Residential', 'Individual',
   'Abdullah Khan', 'Mohammad Yusuf'),
  ('Arjun Nair', 'arjun@email.com', '9876543213', '7777-8888-9999',
   'Plot 200, Tech Park', 5000, 15000000,
   'Whitefield', 'Yelahanka', 'Bangalore Urban', 'Karnataka', 'Commercial', 'Company',
   'Infosys Ltd', 'TCS Ltd')
ON CONFLICT (aadhaar_number) DO NOTHING;

-- Insert fraud logs for duplicate Aadhaar
INSERT INTO fraud_detection_logs (
  application_id, fraud_type, severity, description, evidence
) SELECT
  a.id, 'Duplicate Aadhaar', 'critical',
  'Same Aadhaar number used in multiple applications',
  'Duplicate found with another application in system'
FROM applications a
WHERE a.aadhaar_number = '1111-2222-3333';

-- Insert fraud logs for suspicious transfer
INSERT INTO fraud_detection_logs (
  application_id, fraud_type, severity, description, evidence
) SELECT
  id, 'Suspicious Ownership Transfer', 'high',
  'Property value appears low for location and type',
  'Market analysis suggests undervaluation by 40%'
FROM applications
WHERE aadhaar_number = '4444-5555-6666';

INSERT INTO fraud_detection_logs (
  application_id, fraud_type, severity, description, evidence
) SELECT
  id, 'Document Mismatch', 'medium',
  'Transferring to person with different background',
  'Relationship between parties not clearly established'
FROM applications
WHERE aadhaar_number = '4444-5555-6666';

-- Insert fraud logs for high-value transfer
INSERT INTO fraud_detection_logs (
  application_id, fraud_type, severity, description, evidence
) SELECT
  id, 'Rapid High-Value Transfer', 'high',
  'Large commercial property transfer with minimal documentation',
  'Company-to-company transfer requires additional verification'
FROM applications
WHERE aadhaar_number = '7777-8888-9999';

-- Insert initial workflow steps for sample applications
DO $$
DECLARE
  app_id uuid;
  step_id uuid;
BEGIN
  FOR app_id IN SELECT id FROM applications LIMIT 4 LOOP
    FOR step_id IN SELECT id FROM workflow_steps ORDER BY step_order LOOP
      INSERT INTO step_progress (application_id, step_id, status)
      VALUES (app_id, step_id, 'pending')
      ON CONFLICT DO NOTHING;
    END LOOP;
  END LOOP;
END $$;

-- Insert sample notifications
INSERT INTO notifications (
  application_id, notification_type, channel, recipient, message_content
) SELECT
  a.id, 'application_submitted', 'email', a.citizen_email,
  'Your property registration application has been submitted successfully. Reference: ' || a.id
FROM applications a LIMIT 4;

INSERT INTO notifications (
  application_id, notification_type, channel, recipient, message_content
) SELECT
  a.id, 'application_submitted', 'sms', a.citizen_phone,
  'GovOS: Application submitted. You will receive updates via SMS and email.'
FROM applications a LIMIT 4;
