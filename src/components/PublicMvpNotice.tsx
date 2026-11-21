import React from 'react';

/**
 * Persistent disclosure for the independent, non-government public MVP.
 * Keep this visible until an authorized live integration is explicitly identified.
 */
export function PublicMvpNotice() {
  return (
    <aside
      role="note"
      aria-label="Aether public MVP notice"
      style={{
        padding: '10px 16px',
        borderBottom: '1px solid rgba(148, 163, 184, 0.35)',
        background: 'rgba(15, 23, 42, 0.06)',
        color: 'inherit',
        fontSize: '13px',
        lineHeight: 1.5,
      }}
    >
      <strong>Aether is an independent platform, not a government website.</strong>{' '}
      Public MVP workflows use public information and/or simulated data unless a
      screen explicitly identifies an authorized live integration. Sandbox
      completion does not submit an application or create an official government
      record.
    </aside>
  );
}
