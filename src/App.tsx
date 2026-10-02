import React from 'react';
import { LanguageProvider } from './contexts/LanguageContext';
import { AetherCommandCenter } from './pages/AetherCommandCenter';

function MainAppContent() {
  return <AetherCommandCenter />;
}

export default function App() {
  return (
    <LanguageProvider>
      <MainAppContent />
    </LanguageProvider>
  );
}
