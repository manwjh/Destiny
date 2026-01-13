import { useState, useEffect } from 'react';
import { translations } from '../i18n/locales';
import type { Language, Translations } from '../i18n/locales';

// 本地存储键
const STORAGE_KEY = 'destiny-language';

// 检测浏览器语言
const detectBrowserLanguage = (): Language => {
  const browserLang = navigator.language.toLowerCase();
  
  if (browserLang.startsWith('zh')) {
    // 根据地区判断繁简体
    if (browserLang.includes('tw') || browserLang.includes('hk') || browserLang.includes('mo')) {
      return 'zh-TW';
    }
    return 'zh-CN';
  }
  
  return 'en';
};

// 获取初始语言
const getInitialLanguage = (): Language => {
  // 先检查本地存储
  const stored = localStorage.getItem(STORAGE_KEY) as Language;
  if (stored && translations[stored]) {
    return stored;
  }
  
  // 否则检测浏览器语言
  return detectBrowserLanguage();
};

export const useLanguage = () => {
  const [language, setLanguage] = useState<Language>(getInitialLanguage);
  const [t, setT] = useState<Translations>(translations[language]);

  // 更新语言
  const changeLanguage = (newLang: Language) => {
    setLanguage(newLang);
    setT(translations[newLang]);
    localStorage.setItem(STORAGE_KEY, newLang);
  };

  // 循环切换语言 (简中 -> 繁中 -> 英文 -> 简中)
  const toggleLanguage = () => {
    const languages: Language[] = ['zh-CN', 'zh-TW', 'en'];
    const currentIndex = languages.indexOf(language);
    const nextIndex = (currentIndex + 1) % languages.length;
    changeLanguage(languages[nextIndex]);
  };

  // 语言变化时更新翻译
  useEffect(() => {
    setT(translations[language]);
  }, [language]);

  return {
    language,
    t,
    changeLanguage,
    toggleLanguage,
  };
};
