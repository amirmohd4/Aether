import React, { useState } from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';
import { AetherCommandCenter } from './pages/AetherCommandCenter';
import { DeliveryOpsConsole } from './components/DeliveryOpsConsole';
import { IndiaAdminIntelligence } from './components/IndiaAdminIntelligence';
import { PublicMvpNotice } from './components/PublicMvpNotice';
import { GlobalMockStudio } from './components/GlobalMockStudio';

type Workspace = 'overview' | 'case' | 'departments' | 'operations';

const navigation: Array<{ id: Workspace; label: string; audience: string }> = [
  { id: 'overview', label: 'Explore Aether', audience: 'Everyone' },
  { id: 'case', label: 'Start a case', audience: 'Citizens & businesses' },
  { id: 'departments', label: 'Department map', audience: 'Institutions & partners' },
  { id: 'operations', label: 'Operations', audience: 'Authorized teams' },
];

function MainAppContent() {
  const [workspace, setWorkspace] = useState<Workspace>('overview');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <PublicMvpNotice />
      <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <a href="/" className="flex items-center gap-3" aria-label="Aether GovOS home">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-300/30 bg-cyan-300/10 text-lg font-black text-cyan-200">A</span>
            <span>
              <span className="block text-base font-bold tracking-tight">Aether <span className="text-cyan-200">GovOS</span></span>
              <span className="block text-[10px] uppercase tracking-[0.18em] text-slate-500">Government execution layer</span>
            </span>
          </a>
          <nav aria-label="Main navigation" className="flex flex-wrap gap-2">
            {navigation.map(item => (
              <button
                key={item.id}
                type="button"
                onClick={() => { setWorkspace(item.id); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                aria-current={workspace === item.id ? 'page' : undefined}
                className={`rounded-xl border px-3 py-2 text-left transition ${workspace === item.id ? 'border-cyan-300/40 bg-cyan-300/10 text-cyan-100' : 'border-white/10 text-slate-300 hover:bg-white/5'}`}
              >
                <span className="block text-xs font-semibold">{item.label}</span>
                <span className="hidden text-[9px] text-slate-500 sm:block">{item.audience}</span>
              </button>
            ))}
          </nav>
        </div>
      </header>

      {workspace === 'overview' && (
        <main>
          <section className="relative overflow-hidden border-b border-white/10">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(34,211,238,0.12),transparent_48%)]" />
            <div className="relative mx-auto grid max-w-7xl gap-10 px-5 py-14 md:grid-cols-[1.2fr_0.8fr] md:items-center md:py-20 lg:px-8">
              <div>
                <p className="mb-4 text-xs font-bold uppercase tracking-[0.2em] text-cyan-200">One execution layer · many public services</p>
                <h1 className="max-w-3xl text-4xl font-black leading-tight tracking-tight md:text-6xl">Government work, <span className="text-cyan-200">coordinated.</span></h1>
                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300 md:text-lg">Start with the outcome you need. Aether helps map the service, organize requirements, coordinate dependent work, track evidence and surface the steps that still need an authorized person or government authority.</p>
                <div className="mt-7 flex flex-wrap gap-3">
                  <button onClick={() => setWorkspace('case')} className="rounded-xl bg-cyan-300 px-5 py-3 text-sm font-bold text-slate-950 hover:bg-cyan-200">Start a service case</button>
                  <button onClick={() => document.getElementById('preview-studio')?.scrollIntoView({ behavior: 'smooth' })} className="rounded-xl border border-white/15 px-5 py-3 text-sm font-semibold text-slate-200 hover:bg-white/5">Try the synthetic demo</button>
                </div>
                <p className="mt-4 max-w-xl text-xs leading-5 text-slate-500">Independent software preview. Government integrations and legal requirements are only treated as live when explicitly configured and verified.</p>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                {[
                  ['01', 'Understand', 'Interpret the objective and identify likely services.'],
                  ['02', 'Prepare', 'Surface requirements, evidence gaps and dependencies.'],
                  ['03', 'Coordinate', 'Track tasks, handoffs, exceptions and human review.'],
                  ['04', 'Verify', 'Keep evidence and distinguish internal progress from official outcomes.'],
                ].map(([number, title, detail]) => (
                  <div key={number} className="rounded-2xl border border-white/10 bg-white/[0.035] p-5">
                    <span className="text-xs font-mono text-cyan-200">{number}</span>
                    <h2 className="mt-3 text-lg font-bold">{title}</h2>
                    <p className="mt-2 text-sm leading-6 text-slate-400">{detail}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
          <section id="preview-studio" className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
            <div className="mb-5 max-w-3xl">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-cyan-200">Interactive product preview</p>
              <h2 className="mt-2 text-2xl font-bold md:text-3xl">Explore a workflow before you commit to a process</h2>
              <p className="mt-2 text-sm leading-6 text-slate-400">The studio below is a browser-side simulation. It is useful for exploring scenarios, not for submitting an application or creating a persisted government case.</p>
            </div>
            <GlobalMockStudio />
          </section>
        </main>
      )}

      {workspace === 'case' && <AetherCommandCenter />}
      {workspace === 'departments' && <IndiaAdminIntelligence />}
      {workspace === 'operations' && (
        <main className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
          <section>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-cyan-200">Authorized workspace</p>
            <h1 className="mt-2 text-3xl font-bold">Delivery operations</h1>
            <p className="mt-2 text-sm text-slate-400">Case workload, handoffs and internal actions are available only to authenticated users with the required server-side permissions.</p>
          </section>
          <DeliveryOpsConsole />
        </main>
      )}

      <footer className="border-t border-white/10 px-5 py-8 text-center text-xs leading-6 text-slate-500">
        <p className="font-semibold text-slate-300">Aether GovOS · Independent government execution software</p>
        <p className="mx-auto mt-1 max-w-3xl">Aether does not represent a government authority. Synthetic demonstrations do not submit official applications, issue certificates, or create official decisions. Always verify statutory requirements with the responsible authority.</p>
        <div className="mt-3 flex flex-wrap justify-center gap-4">
          <a className="text-cyan-200 hover:underline" href="/feedback.html">Send product feedback</a>
          <a className="text-cyan-200 hover:underline" href="https://github.com/amirmohd4/Aether" target="_blank" rel="noreferrer">Developer repository</a>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <MainAppContent />
      </LanguageProvider>
    </AuthProvider>
  );
}
