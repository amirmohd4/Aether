import React, { useState } from 'react';
import { Languages, ChevronDown, Check } from 'lucide-react';
import { useTranslation } from '../hooks/useTranslation';
import { LANGUAGES } from '../languages/data';

export const LanguageSwitcher: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { currentLang, setLanguage, t } = useTranslation();
  const activeLang = LANGUAGES[currentLang] || LANGUAGES['en'];

  const handleSelect = (code: string) => {
    setLanguage(code);
    setIsOpen(false);
  };

  return (
    <div className="relative inline-block text-left">
      <button
        id="btn-language-switcher-dropdown"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-700 border border-slate-700 text-white text-xs font-medium transition-all shadow-sm"
        title={t('select_language', 'Language')}
      >
        <Languages className="w-3.5 h-3.5 text-blue-400" />
        <span className="text-base leading-none">{activeLang.flag}</span>
        <span className="hidden sm:inline font-medium text-slate-200">{activeLang.name}</span>
        <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 mt-2 w-48 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl z-50 overflow-hidden backdrop-blur-md">
            <div className="px-3 py-2 border-b border-slate-800 text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
              {t('select_language', 'Select Language')}
            </div>
            <div className="max-h-64 overflow-y-auto py-1">
              {Object.values(LANGUAGES).map((lang) => {
                const isSelected = lang.code === currentLang;
                return (
                  <button
                    key={lang.code}
                    id={`btn-lang-option-${lang.code}`}
                    onClick={() => handleSelect(lang.code)}
                    className={`w-full flex items-center justify-between px-3.5 py-2 text-xs text-left transition-colors ${
                      isSelected ? 'bg-blue-950/60 text-blue-300 font-medium' : 'text-slate-300 hover:bg-slate-800'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="text-base">{lang.flag}</span>
                      <span>{lang.name}</span>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-blue-400" />}
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
