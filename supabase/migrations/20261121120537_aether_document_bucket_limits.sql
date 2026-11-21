-- Provision the private Aether document bucket with application-aligned limits.
-- 15 MiB max; keep this in sync with DocumentStore._max_bytes() and MIME allowlist.

insert into storage.buckets
  (id, name, public, file_size_limit, allowed_mime_types)
values
  (
    'aether-documents',
    'aether-documents',
    false,
    15728640,
    ARRAY[
      'application/pdf',
      'text/plain',
      'text/csv',
      'application/json',
      'image/jpeg',
      'image/png',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]::text[]
  )
on conflict (id) do update
set
  name = excluded.name,
  public = false,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;
