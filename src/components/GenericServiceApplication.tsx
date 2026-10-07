import React, { useMemo, useState } from 'react';

type Props = {
  serviceId: string;
  title: string;
  description: string;
  defaultCustomerType?: string;
};

export const GenericServiceApplication: React.FC<Props> = ({
  serviceId,
  title,
  description,
  defaultCustomerType = 'citizen',
}) => {
  const [objective, setObjective] = useState(title);
  const [customerType, setCustomerType] = useState(defaultCustomerType);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<string>('');

  const endpoint = useMemo(
    () => import.meta.env.VITE_API_URL || 'http://localhost:8081',
    []
  );

  async function analyze() {
    setSubmitting(true);
    setResult('');
    try {
      const response = await fetch(endpoint + '/api/aether/v2/understand', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          objective,
          customer_type: customerType,
          jurisdiction: { country: 'India' },
        }),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(body.detail || 'Unable to analyze this service request.');
      }
      const matched = body.service_name || body.service_id;
      setResult(
        matched
          ? `Aether matched this request to ${matched}. Continue in the secure Command Center to submit the case and complete required documents.`
          : 'Aether needs more context before starting this service.'
      );
    } catch (error) {
      setResult(error instanceof Error ? error.message : 'Unable to analyze this service request.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="w-full max-w-2xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <div className="text-xs font-semibold uppercase tracking-wider text-emerald-700">
          Aether service
        </div>
        <h2 className="mt-1 text-2xl font-bold text-slate-900">{title}</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
        <p className="mt-2 text-[11px] text-slate-500">
          Service contract: <span className="font-mono">{serviceId}</span>
        </p>
      </div>

      <label className="block text-xs font-semibold text-slate-700">What do you need?</label>
      <textarea
        value={objective}
        onChange={(event) => setObjective(event.target.value)}
        className="mt-2 h-28 w-full rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-900 outline-none focus:border-emerald-500"
      />

      <label className="mt-4 block text-xs font-semibold text-slate-700">Applicant type</label>
      <select
        value={customerType}
        onChange={(event) => setCustomerType(event.target.value)}
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white p-3 text-sm text-slate-900"
      >
        <option value="citizen">Citizen</option>
        <option value="business">Business</option>
        <option value="bank">Bank / NBFC</option>
        <option value="developer">Developer / Real Estate</option>
        <option value="insurer">Insurer</option>
        <option value="enterprise">Enterprise</option>
      </select>

      <button
        type="button"
        onClick={analyze}
        disabled={submitting || !objective.trim()}
        className="mt-5 w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-bold text-white disabled:opacity-50"
      >
        {submitting ? 'Understanding…' : 'Understand with Aether'}
      </button>

      {result && (
        <div className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-900">
          {result}
        </div>
      )}

      <p className="mt-4 text-[11px] leading-5 text-slate-500">
        This surface uses Aether’s controlled/sandbox execution backbone. Official
        government issuance remains subject to the responsible authority and an
        authorized connector.
      </p>
    </section>
  );
};

export default GenericServiceApplication;
