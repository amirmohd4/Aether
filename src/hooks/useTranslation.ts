import { useLanguageContext } from '../contexts/LanguageContext';

export function useTranslation() {
  const { currentLang, language, setLanguage, t } = useLanguageContext();
  return {
    currentLang,
    language,
    setLanguage,
    t
  };
}
