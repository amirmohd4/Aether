import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { LANGUAGES, Language } from '../languages/data';

interface LanguageContextType {
  currentLang: string;
  language: Language;
  setLanguage: (langCode: string) => void;
  t: (key: string, fallback?: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentLang, setCurrentLangState] = useState<string>(() => {
    const saved = localStorage.getItem('aether_lang');
    if (saved && LANGUAGES[saved]) return saved;
    const browserLang = navigator.language ? navigator.language.split('-')[0] : 'en';
    return LANGUAGES[browserLang] ? browserLang : 'en';
  });

  const language = LANGUAGES[currentLang] || LANGUAGES['en'];

  useEffect(() => {
    localStorage.setItem('aether_lang', currentLang);
    document.documentElement.dir = language.dir;
    document.documentElement.lang = currentLang;
  }, [currentLang, language]);

  const setLanguage = (langCode: string) => {
    if (LANGUAGES[langCode]) {
      setCurrentLangState(langCode);
    }
  };

  const t = (key: string, fallback?: string): string => {
    if (language.translations[key]) {
      return language.translations[key];
    }
    if (LANGUAGES['en'].translations[key]) {
      return LANGUAGES['en'].translations[key];
    }
    return fallback || key;
  };

  return (
    <LanguageContext.Provider value={{ currentLang, language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguageContext = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguageContext must be used within a LanguageProvider');
  }
  return context;
};
