import React, { useMemo, useState } from 'react';
import { getServiceJurisdictionScope, servicesConfig } from '../servicesConfig';
import { CheckCircle2, CircleAlert, ClipboardCheck, FileText, Globe2, Play, RotateCcw, ShieldAlert } from 'lucide-react';

type Scenario = 'happy' | 'missing' | 'review' | 'retry' | 'rejected';
type JourneyStep = { title: string; detail: string; status: 'complete' | 'attention' | 'pending' };

const scenarioLabels: Record<Scenario, string> = {
  happy: 'Routine path — simulated completion',
  missing: 'Missing evidence — request more information',
  review: 'Authority boundary — human review required',
  retry: 'Temporary system failure — safe retry',
  rejected: 'Adverse scenario — rule or evidence conflict',
};

function requirementsFor(id: string, label: string): string[] {
  const key = (id + ' ' + label).toLowerCase();
  if (/property|mutation|encumbrance|title|land conversion/.test(key)) return ['Applicant identity (fictional)', 'Property/parcel reference', 'Ownership or transaction evidence'];
  if (/building|housing|pmay|rera/.test(key)) return ['Applicant or entity details', 'Site/property reference', 'Plan, eligibility, or project evidence'];
  if (/license|licence|registration|gst|company|factory|food business|trade/.test(key)) return ['Applicant/entity details', 'Business activity and address', 'Supporting compliance evidence'];
  if (/birth|death|passport|visa|police clearance|fir|ration|farmer|scholarship|admission|transfer/.test(key)) return ['Applicant identity (fictional)', 'Relevant event, household, or application reference', 'Supporting evidence'];
  if (/water|vehicle|driving|crop|pds|pf\/esi|medical/.test(key)) return ['Applicant or account details', 'Service/asset reference', 'Supporting evidence'];
  return ['Applicant or organisation details', 'Service-specific reference', 'Supporting evidence'];
}

function workflowStages(serviceId: string, serviceLabel: string): Array<{ title: string; detail: string }> {
  const key = (serviceId + ' ' + serviceLabel).toLowerCase();
  if (/property|mutation|encumbrance|title|land conversion/.test(key)) return [
    { title: 'Resolve property or parcel', detail: 'Match the fictional parcel reference and identify the relevant land-record source.' },
    { title: 'Check ownership and restrictions', detail: 'Compare mock ownership, encumbrance, tax, or transaction evidence; discrepancies become exceptions.' },
    { title: 'Coordinate registry and local checks', detail: 'Prepare dependent registry, valuation, planning, or local-authority tasks for the configured workflow.' },
    { title: 'Authority boundary and record reconciliation', detail: 'A registrar or other authorised person makes any legally required decision. Only a synthetic status is shown here.' },
  ];
  if (/building|housing|pmay|rera|factory|fire|environment/.test(key)) return [
    { title: 'Resolve site, project, or eligibility', detail: 'Validate fictional applicant and site/project references against the selected template.' },
    { title: 'Coordinate technical and compliance checks', detail: 'Model planning, safety, environmental, eligibility, or project-document checks as dependent tasks.' },
    { title: 'Inspection and exception routing', detail: 'Flag any inspection, disputed evidence, or professional sign-off for an authorised person.' },
    { title: 'Permit / benefit status reconciliation', detail: 'Reconcile only synthetic task results. No permit, benefit, or approval is issued by this preview.' },
  ];
  if (/gst|tax|pf|esi|pds|ration|pension|scholarship|farmer|crop|pmay|subsidy/.test(key)) return [
    { title: 'Resolve applicant and programme', detail: 'Match the fictional person or organisation to the selected tax, contribution, insurance, or welfare workflow.' },
    { title: 'Check eligibility and evidence', detail: 'Compare illustrative identity, income, household, contribution, or supporting-evidence fields.' },
    { title: 'Duplicate, liability, and exception checks', detail: 'Model possible duplicate records, missing evidence, mismatches, or a referral for manual review.' },
    { title: 'Authorised determination and status check', detail: 'Any legal entitlement, tax determination, or payment decision remains with the responsible authority.' },
  ];
  if (/birth|death|passport|visa|police clearance|fir|driving|vehicle|marriage/.test(key)) return [
    { title: 'Resolve identity and application reference', detail: 'Match fictional applicant and event, travel, driver, vehicle, or report references.' },
    { title: 'Cross-check supporting records', detail: 'Compare illustrative source records and identify mismatches or missing evidence.' },
    { title: 'Route statutory or physical checks', detail: 'Identity adjudication, interview, biometric capture, investigation, or other required action stays with authorised people.' },
    { title: 'Registry status reconciliation', detail: 'Show a synthetic status only; this preview cannot issue a certificate, passport, licence, visa, or police record.' },
  ];
  if (/company|business|trade|license|licence|food|medical|admission|transfer|water/.test(key)) return [
    { title: 'Validate applicant and service scope', detail: 'Check fictional entity/person details, activity, location, and selected service template.' },
    { title: 'Coordinate department prerequisites', detail: 'Represent dependent registration, premises, tax, utility, or institutional checks without contacting official systems.' },
    { title: 'Resolve missing items and compliance exceptions', detail: 'Pause for additional evidence, an inspection, or an authorised review where required.' },
    { title: 'Reconcile synthetic service status', detail: 'Return a demo reference and workflow state, not an official registration, licence, admission, or connection.' },
  ];
  return [
    { title: 'Validate fictional intake', detail: 'Check minimum fields and the illustrative evidence checklist for this template.' },
    { title: 'Resolve source records and dependencies', detail: 'Map the workflow to mock source checks; jurisdiction-specific rules remain unverified until configured.' },
    { title: 'Coordinate exceptions and human review', detail: 'Pause when evidence is incomplete or a legal, professional, or physical action is required.' },
    { title: 'Reconcile synthetic outcome', detail: 'Record a demo state only. No official record, decision, or certificate is created.' },
  ];
}

function tasksFor(serviceId: string, serviceLabel: string, scenario: Scenario): JourneyStep[] {
  const stages = workflowStages(serviceId, serviceLabel);
  const base: JourneyStep[] = [
    { title: 'Intake and validation', detail: 'A fictional request was received and checked for basic completeness.', status: 'complete' },
    { title: 'Service and jurisdiction routing', detail: 'Aether selected a reusable workflow template. The jurisdiction label does not certify local law or service availability.', status: 'complete' },
    { title: 'Evidence and dependency checks', detail: 'The mock engine created a checklist and mapped dependent work; no official records were queried.', status: 'complete' },
  ];
  if (scenario === 'missing') return [
    ...base,
    { title: 'Applicant action needed', detail: 'The simulation found an evidence gap. The workflow pauses until the fictional item is supplied or clarified.', status: 'attention' },
    { title: 'Downstream processing', detail: 'Not started because the mock intake is incomplete.', status: 'pending' },
  ];
  if (scenario === 'review') return [
    ...base,
    { title: stages[2]?.title || 'Authority / physical review', detail: 'A legally authorised person or physical inspection may be required in a real process. Aether does not make that decision.', status: 'attention' },
    { title: 'Official outcome', detail: 'Held for the responsible authority; no approval, entitlement, certificate, or official record is issued in this demo.', status: 'pending' },
  ];
  if (scenario === 'retry') return [
    ...base,
    { title: 'Synthetic connector request', detail: 'The first mock attempt failed with a simulated transient error. A stable idempotency key is retained for retry.', status: 'attention' },
    { title: 'Retry and reconcile', detail: 'The mock retry recovered without creating a duplicate simulated request.', status: 'complete' },
    { title: 'Synthetic outcome verification', detail: 'The response was reconciled against the simulator only; no real source of record was contacted.', status: 'complete' },
  ];
  if (scenario === 'rejected') return [
    ...base,
    { title: 'Evidence / rule conflict detected', detail: 'The synthetic scenario deliberately introduces a mismatch or failed illustrative condition. This is not a real legal assessment.', status: 'attention' },
    { title: 'Stop and explain the reason', detail: 'Aether pauses downstream work, records the mock reason, and identifies what evidence or authorised review may be needed.', status: 'complete' },
    { title: 'Official decision remains external', detail: 'No official rejection or adverse decision is made. A real determination belongs to the responsible authority with applicable review rights.', status: 'pending' },
  ];
  return [
    ...base,
    ...stages.map((stage, index) => ({
      title: stage.title,
      detail: stage.detail,
      status: index === stages.length - 1 ? 'attention' as const : 'complete' as const,
    })),
  ];
}

export const GlobalMockStudio: React.FC = () => {
  const [serviceId, setServiceId] = useState(servicesConfig[0]?.id || '');
  const [jurisdiction, setJurisdiction] = useState('Global mock environment');
  const [applicant, setApplicant] = useState('Individual applicant');
  const [objective, setObjective] = useState('');
  const [evidence, setEvidence] = useState<string[]>([]);
  const [scenario, setScenario] = useState<Scenario>('happy');
  const [journey, setJourney] = useState<JourneyStep[] | null>(null);
  const [reference, setReference] = useState('');
  const [rating, setRating] = useState('5');
  const [feedback, setFeedback] = useState('');
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const service = useMemo(() => servicesConfig.find(item => item.id === serviceId) || servicesConfig[0], [serviceId]);
  const requirements = useMemo(() => service ? requirementsFor(service.id, service.label) : [], [service]);
  const missingEvidence = requirements.filter(item => !evidence.includes(item));
  const steps = ['Choose service', 'Fictional intake', 'Simulate workflow', 'Review and feedback'];

  function runSimulation() {
    if (!service) return;
    const ref = 'SIM-' + Math.random().toString(36).slice(2, 10).toUpperCase();
    setReference(ref);
    if (scenario === 'missing' && missingEvidence.length === 0) {
      setJourney([
        { title: 'Intake and validation', detail: 'The supplied checklist is complete, but this scenario deliberately marks one evidence item as unverified to test recovery.', status: 'complete' },
        { title: 'Evidence validation', detail: 'A mock evidence item needs confirmation. The user must confirm or replace it before the journey can continue.', status: 'attention' },
        { title: 'Processing', detail: 'Paused until evidence is resolved.', status: 'pending' },
      ]);
    } else if (scenario !== 'missing' && missingEvidence.length > 0) {
      setJourney([
        { title: 'Intake and validation', detail: 'The fictional request has been received.', status: 'complete' },
        { title: 'Evidence validation', detail: 'Missing checklist items: ' + missingEvidence.join(', ') + '. The workflow pauses instead of pretending the case is complete.', status: 'attention' },
        { title: 'Processing', detail: 'Not started until the required mock evidence is marked as supplied.', status: 'pending' },
      ]);
    } else {
      setJourney(tasksFor(service.id, service.label, scenario));
    }
    setFeedbackMessage('');
  }

  function copyFeedback() {
    const text = [
      'Aether GovOS — mock journey feedback',
      'Service: ' + (service?.label || serviceId),
      'Jurisdiction label: ' + jurisdiction,
      'Scenario: ' + scenarioLabels[scenario],
      'Rating: ' + rating + '/5',
      'Feedback: ' + feedback,
      'Demo reference: ' + reference,
      'Note: synthetic test only; no official application submitted.',
    ].join('\n');
    void navigator.clipboard?.writeText(text).then(() => setFeedbackMessage('Feedback copied. Paste it into the feedback page or your message to the Aether team.')).catch(() => setFeedbackMessage(text));
  }

  return (
    <section className="mb-8 rounded-3xl border border-cyan-300/20 bg-gradient-to-br from-cyan-300/[0.08] via-white/[0.025] to-violet-300/[0.06] p-5 md:p-7">
      <div className="flex flex-col gap-3 border-b border-white/10 pb-5 md:flex-row md:items-start md:justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-cyan-200"><Globe2 className="h-4 w-4" /> Global research preview</div>
          <h2 className="mt-2 text-2xl font-bold text-white md:text-3xl">Test a complete mock journey</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">Choose any of the 32 service templates, test different workflow paths, and tell us where Aether should reduce friction. Some templates are India-specific references; all actual requirements and availability must be configured and verified for the relevant jurisdiction. Use fictional details only.</p>
        </div>
        <div className="flex items-center gap-2 rounded-xl border border-amber-300/20 bg-amber-300/[0.07] px-3 py-2 text-[11px] text-amber-100"><ShieldAlert className="h-4 w-4 shrink-0" /> SYNTHETIC ONLY · NOT AN OFFICIAL RECORD</div>
      </div>

      <div className="mt-5 grid gap-5 xl:grid-cols-[1fr_1fr]">
        <div className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-xs font-semibold text-slate-300">1. Service ({servicesConfig.length} available)
              <select value={serviceId} onChange={e => { setServiceId(e.target.value); setJourney(null); setEvidence([]); }} className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white">
                {servicesConfig.map(item => <option key={item.id} value={item.id}>{item.icon} {item.label}</option>)}
              </select>
              <span className="mt-1 block text-[10px] font-normal text-cyan-200">{service ? getServiceJurisdictionScope(service.id) : ''}</span>
            </label>
            <label className="text-xs font-semibold text-slate-300">Demo jurisdiction label
              <select value={jurisdiction} onChange={e => setJurisdiction(e.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white">
                <option>Global mock environment</option><option>India — synthetic only</option><option>United States — synthetic only</option><option>United Kingdom — synthetic only</option><option>Other jurisdiction — synthetic only</option>
              </select>
            </label>
          </div>
          <label className="block text-xs font-semibold text-slate-300">2. What outcome are you testing?
            <textarea value={objective} onChange={e => setObjective(e.target.value)} placeholder={'Example: I need to renew a driving licence'} className="mt-2 h-20 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white placeholder:text-slate-500" />
          </label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-xs font-semibold text-slate-300">Applicant type
              <select value={applicant} onChange={e => setApplicant(e.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white">
                <option>Individual applicant</option><option>Business / company</option><option>Bank / financial institution</option><option>Developer / service integrator</option><option>Public-sector employee</option>
              </select>
            </label>
            <label className="text-xs font-semibold text-slate-300">Test scenario
              <select value={scenario} onChange={e => setScenario(e.target.value as Scenario)} className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white">
                {Object.entries(scenarioLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
              </select>
            </label>
          </div>
          <div className="rounded-2xl border border-white/10 bg-black/10 p-4">
            <div className="flex items-center justify-between gap-2"><h3 className="text-sm font-semibold text-white">Evidence checklist</h3><span className="text-[10px] text-slate-400">{evidence.length}/{requirements.length} marked supplied</span></div>
            <p className="mt-1 text-xs text-slate-400">Checklist templates are illustrative and do not represent verified legal requirements for your jurisdiction.</p>
            <div className="mt-3 space-y-2">
              {requirements.map(item => <label key={item} className="flex items-start gap-2 rounded-lg border border-white/5 p-2 text-xs text-slate-300"><input type="checkbox" checked={evidence.includes(item)} onChange={e => setEvidence(old => e.target.checked ? [...old, item] : old.filter(x => x !== item))} className="mt-0.5 accent-cyan-300" /><span>{item}</span></label>)}
            </div>
          </div>
          <button type="button" onClick={runSimulation} className="flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-300 px-4 py-3 text-sm font-bold text-slate-950 hover:bg-cyan-200"><Play className="h-4 w-4" /> Run synthetic journey</button>
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
            <h3 className="text-sm font-semibold text-white">Journey monitor</h3>
            <div className="mt-3 grid grid-cols-4 gap-2">
              {steps.map((step, i) => <div key={step} className="rounded-lg border border-white/5 bg-white/[0.03] p-2"><div className="text-[10px] text-cyan-200">0{i + 1}</div><div className="mt-1 text-[10px] leading-4 text-slate-300">{step}</div></div>)}
            </div>
            {!journey ? <div className="mt-4 rounded-xl border border-dashed border-white/10 p-8 text-center"><ClipboardCheck className="mx-auto h-8 w-8 text-slate-500" /><p className="mt-3 text-sm text-slate-300">Your simulated process graph will appear here.</p><p className="mt-1 text-xs text-slate-500">No government connector is called by this studio.</p></div> : <>
              <p className="mt-4 text-xs text-slate-300"><span className="font-semibold text-white">Outcome being tested:</span> {objective.trim() || service?.label || 'Selected service'}</p>
              <div className="mt-3 flex flex-wrap items-center justify-between gap-2 rounded-xl border border-cyan-300/20 bg-cyan-300/[0.05] p-3"><div><div className="text-[10px] uppercase tracking-wide text-cyan-200">Simulation reference</div><div className="mt-1 font-mono text-sm text-white">{reference}</div></div><span className="rounded-full border border-amber-300/20 bg-amber-300/[0.06] px-2 py-1 text-[10px] text-amber-100">NOT OFFICIAL</span></div>
              <div className="mt-3 space-y-2">
                {journey.map((step, i) => <div key={step.title} className="flex gap-3 rounded-xl border border-white/5 bg-white/[0.025] p-3"><div className="mt-0.5">{step.status === 'complete' ? <CheckCircle2 className="h-4 w-4 text-emerald-300" /> : step.status === 'attention' ? <CircleAlert className="h-4 w-4 text-amber-300" /> : <FileText className="h-4 w-4 text-slate-500" />}</div><div><div className="text-sm font-medium text-slate-100">{i + 1}. {step.title}</div><p className="mt-1 text-xs leading-5 text-slate-400">{step.detail}</p></div></div>)}
              </div>
              <p className="mt-3 text-[11px] leading-5 text-amber-100/80">Applicant label: {applicant}. {jurisdiction} is only a label. This is a client-side scenario simulation; no request was sent to a government service and no real application was created.</p>
            </>}
          </div>

          <div className="rounded-2xl border border-white/10 bg-black/10 p-4">
            <h3 className="text-sm font-semibold text-white">4. Share feedback</h3>
            <p className="mt-1 text-xs text-slate-400">Tell us what was confusing, missing, or worth automating. Feedback is not sent automatically from this mock screen.</p>
            <a href={`/feedback.html?workflow=${encodeURIComponent(service?.label || serviceId)}&jurisdiction=${encodeURIComponent(jurisdiction)}&scenario=${encodeURIComponent(scenarioLabels[scenario])}&rating=${encodeURIComponent(rating)}`} className="mt-2 inline-flex text-xs font-semibold text-cyan-200 underline underline-offset-4">Open feedback form with this test pre-filled</a>
            <div className="mt-3 grid gap-3 sm:grid-cols-[120px_1fr]">
              <label className="text-xs text-slate-300">Rating
                <select value={rating} onChange={e => setRating(e.target.value)} className="mt-2 w-full rounded-lg border border-white/10 bg-slate-900 p-2 text-sm text-white">{['5','4','3','2','1'].map(x => <option key={x} value={x}>{x} / 5</option>)}</select>
              </label>
              <label className="text-xs text-slate-300">Your feedback
                <textarea value={feedback} onChange={e => setFeedback(e.target.value)} placeholder="What should we improve in this service journey?" className="mt-2 h-20 w-full rounded-lg border border-white/10 bg-slate-900 p-3 text-sm font-normal text-white placeholder:text-slate-500" />
              </label>
            </div>
            <button type="button" onClick={copyFeedback} disabled={!feedback.trim()} className="mt-3 flex items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-xs font-semibold text-slate-200 disabled:opacity-40"><ClipboardCheck className="h-4 w-4" /> Copy feedback to share</button>
            {feedbackMessage && <p className="mt-2 whitespace-pre-wrap text-xs text-cyan-200">{feedbackMessage}</p>}
          </div>
        </div>
      </div>
      <div className="mt-5 flex flex-wrap items-center justify-between gap-2 border-t border-white/10 pt-4 text-[10px] text-slate-500"><span>Mock templates: {servicesConfig.length} · Scenarios: routine path, missing evidence, human review, retry · synthetic only</span><button type="button" onClick={() => { setJourney(null); setReference(''); setEvidence([]); setFeedback(''); setFeedbackMessage(''); }} className="flex items-center gap-1 rounded-lg border border-white/10 px-3 py-2 text-slate-300"><RotateCcw className="h-3 w-3" /> Reset mock</button></div>
    </section>
  );
};

export default GlobalMockStudio;
