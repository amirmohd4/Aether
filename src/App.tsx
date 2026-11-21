import React, { useState } from 'react';
import { ArrowRight, Building2, Code2, Globe2, Landmark, PlayCircle, ShieldCheck, Workflow } from 'lucide-react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';
import { AetherCommandCenter } from './pages/AetherCommandCenter';
import { DeliveryOpsConsole } from './components/DeliveryOpsConsole';
import { IndiaAdminIntelligence } from './components/IndiaAdminIntelligence';
import { PublicMvpNotice } from './components/PublicMvpNotice';
import { GlobalMockStudio } from './components/GlobalMockStudio';

type View = 'home' | 'workspace' | 'sandbox' | 'government';

const navigation: Array<{ id: View; label: string }> = [
  { id: 'home', label: 'Overview' },
  { id: 'workspace', label: 'Start a request' },
  { id: 'sandbox', label: 'Product sandbox' },
  { id: 'government', label: 'Government workspace' },
];

function MainAppContent() {
  const [view, setView] = useState<View>('home');

  const openWorkspace = () => {
    setView('workspace');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <PublicMvpNotice />

      <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
          <button type="button" onClick={() => setView('home')} className="flex items-center gap-3 text-left">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-400 text-slate-950">
              <Globe2 className="h-6 w-6" />
            </span>
            <span>
              <span className="block text-lg font-bold tracking-tight text-white">Aether</span>
              <span className="block text-[10px] font-semibold uppercase tracking-[0.18em] text-emerald-300">Government execution platform</span>
            </span>
          </button>

          <nav aria-label="Main navigation" className="hidden items-center gap-1 md:flex">
            {navigation.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setView(item.id)}
                aria-current={view === item.id ? 'page' : undefined}
                className={`rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  view === item.id ? 'bg-white/10 text-white' : 'text-slate-400 hover:bg-white/5 hover:text-white'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>

          <button
            type="button"
            onClick={openWorkspace}
            className="inline-flex items-center gap-2 rounded-xl bg-emerald-400 px-4 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-emerald-300"
          >
            Open workspace <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        <nav aria-label="Mobile navigation" className="flex gap-2 overflow-x-auto border-t border-white/5 px-4 py-2 md:hidden">
          {navigation.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setView(item.id)}
              aria-current={view === item.id ? 'page' : undefined}
              className={`shrink-0 rounded-lg px-3 py-2 text-xs font-semibold ${
                view === item.id ? 'bg-white/10 text-white' : 'text-slate-400'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </header>

      {view === 'home' && (
        <main>
          <section className="relative isolate overflow-hidden border-b border-white/10">
            <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,rgba(16,185,129,0.16),transparent_45%),radial-gradient(ellipse_at_bottom_left,rgba(14,165,233,0.10),transparent_45%)]" />
            <div className="mx-auto grid max-w-7xl gap-12 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:px-8">
              <div>
                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-400/25 bg-emerald-400/10 px-3 py-1.5 text-xs font-semibold text-emerald-200">
                  <ShieldCheck className="h-4 w-4" /> One coordinated workflow across services
                </div>
                <h1 className="max-w-3xl text-4xl font-black leading-tight tracking-tight text-white sm:text-6xl">
                  Government work, <span className="text-emerald-300">connected.</span>
                </h1>
                <p className="mt-6 max-w-2xl text-base leading-8 text-slate-300 sm:text-lg">
                  Describe what you need to accomplish. Aether helps map the service, requirements,
                  departments, evidence and work that move the case forward—through one coordinated workspace.
                </p>
                <div className="mt-9 flex flex-col gap-3 sm:flex-row">
                  <button type="button" onClick={openWorkspace} className="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-400 px-6 py-4 font-bold text-slate-950 transition hover:bg-emerald-300">
                    Start with an objective <ArrowRight className="h-5 w-5" />
                  </button>
                  <button type="button" onClick={() => setView('sandbox')} className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/15 px-6 py-4 font-semibold text-white transition hover:bg-white/5">
                    <PlayCircle className="h-5 w-5" /> Explore the sandbox
                  </button>
                </div>
                <p className="mt-4 text-xs leading-6 text-slate-500">
                  Public preview uses synthetic workflows unless a screen explicitly identifies an authorized live integration.
                </p>
              </div>

              <div className="rounded-3xl border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-black/30 sm:p-7">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-300">Aether workflow</p>
                    <h2 className="mt-1 text-lg font-bold text-white">From objective to coordinated work</h2>
                  </div>
                  <Workflow className="h-7 w-7 text-emerald-300" />
                </div>
                <div className="mt-5 space-y-3">
                  {[
                    ['01', 'Understand the objective', 'Identify the likely service and missing context'],
                    ['02', 'Map requirements', 'Surface evidence, departments and jurisdiction scope'],
                    ['03', 'Coordinate execution', 'Create tasks, dependencies and human checkpoints'],
                    ['04', 'Track the case', 'Follow progress, exceptions and recorded outcomes'],
                  ].map(([number, title, description], index) => (
                    <div key={number} className="flex gap-4 rounded-2xl border border-white/5 bg-slate-950/70 p-4">
                      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-400/10 text-sm font-bold text-emerald-300">{number}</span>
                      <div>
                        <h3 className="font-semibold text-white">{title}</h3>
                        <p className="mt-1 text-sm leading-6 text-slate-400">{description}</p>
                      </div>
                      {index === 3 && <ArrowRight className="ml-auto mt-2 h-4 w-4 shrink-0 text-slate-500" />}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="max-w-2xl">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-emerald-300">One platform, different workspaces</p>
              <h2 className="mt-3 text-3xl font-bold tracking-tight text-white">Built around the people doing the work.</h2>
              <p className="mt-4 leading-7 text-slate-400">Start from the same coordinated execution layer, then use the workspace that matches your role.</p>
            </div>
            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[
                { icon: Building2, title: 'Citizens & businesses', detail: 'Describe a goal, understand requirements and follow a case.' },
                { icon: Landmark, title: 'Government teams', detail: 'Review queues, exceptions and cross-department work.' },
                { icon: ShieldCheck, title: 'Institutions', detail: 'Explore structured service workflows and integration boundaries.' },
                { icon: Code2, title: 'Developers', detail: 'Build against documented, permissioned execution APIs.' },
              ].map(({ icon: Icon, title, detail }) => (
                <button key={title} type="button" onClick={title === 'Government teams' ? () => setView('government') : openWorkspace} className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 text-left transition hover:border-emerald-400/40 hover:bg-slate-900">
                  <Icon className="h-6 w-6 text-emerald-300" />
                  <h3 className="mt-4 font-bold text-white">{title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-400">{detail}</p>
                  <span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-emerald-300">Open workspace <ArrowRight className="h-4 w-4" /></span>
                </button>
              ))}
            </div>
          </section>
        </main>
      )}

      {view === 'workspace' && (
        <main>
          <div className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8">
            <button type="button" onClick={() => setView('home')} className="text-sm font-semibold text-emerald-300 hover:text-emerald-200">← Back to overview</button>
            <div className="mt-4 mb-6">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-emerald-300">Execution workspace</p>
              <h1 className="mt-2 text-2xl font-bold text-white sm:text-3xl">What are you trying to accomplish?</h1>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">The workspace below connects to Aether V2 APIs for objective understanding, case creation, task execution and case tracking. Availability depends on the configured backend and account permissions.</p>
            </div>
          </div>
          <AetherCommandCenter />
        </main>
      )}

      {view === 'sandbox' && (
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <div className="mb-6">
            <button type="button" onClick={() => setView('home')} className="text-sm font-semibold text-emerald-300 hover:text-emerald-200">← Back to overview</button>
            <h1 className="mt-4 text-2xl font-bold text-white sm:text-3xl">Synthetic product sandbox</h1>
            <p className="mt-2 text-sm leading-6 text-slate-400">Explore illustrative scenarios. Sandbox references and outcomes are simulated; they are not official submissions or government decisions.</p>
          </div>
          <GlobalMockStudio />
        </main>
      )}

      {view === 'government' && (
        <main className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
          <div>
            <button type="button" onClick={() => setView('home')} className="text-sm font-semibold text-emerald-300 hover:text-emerald-200">← Back to overview</button>
            <p className="mt-4 text-xs font-bold uppercase tracking-[0.18em] text-emerald-300">Role-restricted tools</p>
            <h1 className="mt-2 text-2xl font-bold text-white sm:text-3xl">Government operations</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">Operational tools depend on authenticated roles and server-side authorization. Access is not granted by this navigation.</p>
          </div>
          <DeliveryOpsConsole />
          <IndiaAdminIntelligence />
        </main>
      )}

      <footer className="border-t border-white/10 px-4 py-8 text-center text-xs leading-6 text-slate-500">
        Aether is an independent software platform. External government actions and statutory outcomes are shown only when verified through an authorized integration.
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
