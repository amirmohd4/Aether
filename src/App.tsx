import React, { useState } from 'react';
import { 
  Globe, Play, Layers, Code, DollarSign, Cpu, Award, Shield, 
  Github, ChevronRight, Sparkles, Terminal, ArrowRight
} from 'lucide-react';
import { LanguageProvider } from './contexts/LanguageContext';
import { CountrySelector } from './components/CountrySelector';
import { LanguageSwitcher } from './components/LanguageSwitcher';
import { GlobalLanding } from './pages/GlobalLanding';
import { StartFlow } from './components/StartFlow';
import { useTranslation } from './hooks/useTranslation';

function MainAppContent() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans antialiased">
      <GlobalLanding />
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <MainAppContent />
    </LanguageProvider>
  );
}
