import React from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider } from './contexts/AuthContext';
import { AetherCommandCenter } from './pages/AetherCommandCenter';

function MainAppContent() {
  return <AetherCommandCenter />;
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
