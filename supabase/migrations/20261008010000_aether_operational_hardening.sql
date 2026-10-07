-- Operational hardening layered after the initial Aether MVP schema.
-- Idempotent: safe to apply to an existing Aether Supabase project.

create schema if not exists aether_internal;

create table if not exists aether_internal.aether_v2_case_leases (
  case_id varchar(64) primary key,
  locked_by varchar(128) not null,
  lease_until timestamptz not null,
  heartbeat_at timestamptz not null
);

create index if not exists idx_aether_v2_case_leases_lease_until
  on aether_internal.aether_v2_case_leases(lease_until);

alter table if exists aether_internal.aether_v2_notifications
  add column if not exists idempotency_key varchar(256);
alter table if exists aether_internal.aether_v2_notifications
  add column if not exists attempts integer not null default 0;
alter table if exists aether_internal.aether_v2_notifications
  add column if not exists locked_by varchar(128);
alter table if exists aether_internal.aether_v2_notifications
  add column if not exists lease_until timestamptz;
alter table if exists aether_internal.aether_v2_notifications
  add column if not exists last_error text;

create unique index if not exists uq_aether_v2_notifications_tenant_idempotency
  on aether_internal.aether_v2_notifications(tenant_id, idempotency_key);

create index if not exists idx_aether_v2_notifications_status
  on aether_internal.aether_v2_notifications(status);
create index if not exists idx_aether_v2_notifications_lease_until
  on aether_internal.aether_v2_notifications(lease_until);

alter table aether_internal.aether_v2_case_leases enable row level security;
alter table aether_internal.aether_v2_notifications enable row level security;

revoke all on aether_internal.aether_v2_case_leases from anon, authenticated;
revoke all on aether_internal.aether_v2_notifications from anon, authenticated;
