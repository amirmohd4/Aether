import React from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';
import { AetherCommandCenter } from './pages/AetherCommandCenter';
import { DeliveryOpsConsole } from './components/DeliveryOpsConsole';
import { IndiaAdminIntelligence } from './components/IndiaAdminIntelligence';
import { PublicMvpNotice } from './components/PublicMvpNotice';
import { GlobalMockStudio } from './components/GlobalMockStudio';

function MainAppContent() {
  return (
    <>
      <PublicMvpNotice />
      <GlobalMockStudio />
      <AetherCommandCenter />
      <DeliveryOpsConsole />
      <IndiaAdminIntelligence />
    </>
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
