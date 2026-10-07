-- Aether MVP performance hardening.
-- Adds covering indexes for existing foreign keys and removes one duplicate
-- service index reported by the Supabase database advisor.

create index if not exists idx_certificates_citizen_id
  on public.certificates(citizen_id);

create index if not exists idx_fraud_detection_logs_property_id
  on public.fraud_detection_logs(property_id);

create index if not exists idx_fraud_detection_logs_workflow_id
  on public.fraud_detection_logs(workflow_id);

create index if not exists idx_properties_owner_citizen_id
  on public.properties(owner_citizen_id);

create index if not exists idx_workflow_states_citizen_id
  on public.workflow_states(citizen_id);

create index if not exists idx_workflow_states_property_id
  on public.workflow_states(property_id);

drop index if exists aether_internal.idx_aether_v2_cases_service;
