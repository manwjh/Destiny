import React, { useState, useEffect, useRef } from 'react';
import { Languages, Share2, RotateCcw, ChevronDown } from 'lucide-react';
import { useLanguage } from './hooks/useLanguage';
import { languageNames } from './i18n/locales';
import type { Language } from './i18n/locales';

// 类型定义
interface FortuneResult {
  text: string;
  language: Language;
  timestamp: number;
  shareText: string;
  id: string;
}

type AppState = 'input' | 'loading' | 'result' | 'error';

const App: React.FC = () => {
  const { language, t, changeLanguage } = useLanguage();
  const [question, setQuestion] = useState('');
  const [state, setState] = useState<AppState>('input');
  const [result, setResult] = useState<FortuneResult | null>(null);
  const [error, setError] = useState('');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'warning' } | null>(null);
  const [showLangMenu, setShowLangMenu] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const langMenuRef = useRef<HTMLDivElement>(null);

  // 页面加载时聚焦输入框
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // 处理URL分享参数
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const shareId = params.get('share');
    if (shareId) {
      // 根据shareId获取分享的算卦结果
      loadSharedResult(shareId);
    }
  }, []);

  // 加载分享的结果
  const loadSharedResult = async (shareId: string) => {
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    setState('loading');
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/share/${shareId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.message || 'Failed to load shared result');
      }

      // 设置结果并显示
      setResult({
        text: data.data.text,
        language: data.data.language,
        timestamp: data.data.timestamp,
        shareText: data.data.shareText,
        id: data.data.id
      });
      setState('result');
      
      // 清除URL中的share参数（可选，保持分享链接可再次访问）
      // window.history.replaceState({}, '', window.location.pathname);
      
    } catch (err) {
      console.error('Load shared result error:', err);
      setError(err instanceof Error ? err.message : t.errorMessage);
      setState('error');
    }
  };

  // 点击外部关闭语言菜单
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (langMenuRef.current && !langMenuRef.current.contains(event.target as Node)) {
        setShowLangMenu(false);
      }
    };

    if (showLangMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showLangMenu]);

  // Toast 提示
  const showToast = (message: string, type: 'success' | 'error' | 'warning' = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  // 验证输入（允许空输入）
  const validateQuestion = (q: string): { valid: boolean; message?: string } => {
    // 允许空输入，只检查最大长度
    if (q.length > 200) {
      return { valid: false, message: t.validation.tooLong };
    }
    return { valid: true };
  };

  // 随机按钮文案
  const getRandomButtonText = () => {
    return t.buttonTexts[Math.floor(Math.random() * t.buttonTexts.length)];
  };

  // 真实API调用
  const divineFortune = async (question: string): Promise<FortuneResult> => {
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/divine`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          language
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.message || 'Divine failed');
      }

      return {
        text: data.data.text,
        language: data.data.language,
        timestamp: data.data.timestamp,
        shareText: data.data.shareText,
        id: data.data.id
      };
    } catch (error) {
      console.error('API call failed:', error);
      // 如果 API 失败，使用备用方案（可选）
      throw error;
    }
  };

  // 处理算卦
  const handleDivine = async () => {
    const validation = validateQuestion(question);
    if (!validation.valid) {
      showToast(validation.message!, 'warning');
      return;
    }

    setState('loading');
    setError('');

    try {
      const fortuneResult = await divineFortune(question);
      setResult(fortuneResult);
      setState('result');
    } catch (err) {
      console.error('Divine error:', err);
      setError(t.errorMessage);
      setState('error');
    }
  };

  // 重新开始
  const handleRestart = () => {
    setQuestion('');
    setResult(null);
    setError('');
    setState('input');
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  // 分享功能
  const handleShare = async () => {
    if (!result) return;

    const shareUrl = `${window.location.origin}?share=${result.id}`;
    const fullShareText = `${result.shareText} ${shareUrl}`;

    try {
      if (navigator.share) {
        await navigator.share({
          title: t.appTitle,
          text: fullShareText,
          url: shareUrl
        });
      } else {
        await navigator.clipboard.writeText(fullShareText);
        showToast(t.toast.copied, 'success');
      }
    } catch (err) {
      console.error('Share error:', err);
      showToast(t.toast.shareFailed, 'error');
    }
  };

  // 选择语言
  const selectLanguage = (lang: Language) => {
    changeLanguage(lang);
    setShowLangMenu(false);
    setQuestion('');
    setResult(null);
    setState('input');
  };

  // 生成星星背景
  const renderStars = () => {
    const stars = [];
    for (let i = 0; i < 50; i++) {
      const style = {
        top: `${Math.random() * 100}%`,
        left: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        animationDuration: `${2 + Math.random() * 3}s`
      };
      stars.push(<div key={`star-${i}`} className="star" style={style} />);
    }
    return stars;
  };

  // 生成浮动粒子
  const renderParticles = () => {
    const particles = [];
    for (let i = 0; i < 15; i++) {
      const style = {
        left: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 20}s`,
        animationDuration: `${15 + Math.random() * 10}s`
      };
      particles.push(
        <div key={`particle-${i}`} className="floating-particle" style={style} />
      );
    }
    return particles;
  };

  return (
    <>
      {/* 星空背景 */}
      <div className="stars-background">
        {renderStars()}
        {renderParticles()}
      </div>

      <div className="destiny-container">
        {/* 语言切换菜单 - 移至底部 */}
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50" ref={langMenuRef} style={{ bottom: 'max(1.5rem, env(safe-area-inset-bottom) + 1rem)' }}>
        {/* 语言上拉菜单 */}
        {showLangMenu && (
          <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 backdrop-blur-xl bg-white/15 rounded-2xl shadow-2xl overflow-hidden min-w-[180px] border border-white/30 animate-slide-up">
            {(Object.keys(languageNames) as Language[]).map((lang) => (
              <button
                key={lang}
                onClick={() => selectLanguage(lang)}
                className={`w-full px-5 py-3.5 text-center transition-all duration-300 touch-manipulation ${
                  language === lang
                    ? 'bg-white/30 text-white font-bold'
                    : 'text-white/90 hover:bg-white/20 hover:text-white'
                }`}
                style={{ minHeight: '44px' }}
              >
                {languageNames[lang]}
              </button>
            ))}
          </div>
        )}
        
        <button
          onClick={() => setShowLangMenu(!showLangMenu)}
          className="flex items-center space-x-2 px-5 py-2.5 rounded-full backdrop-blur-xl bg-white/5 hover:bg-white/15 active:bg-white/20 transition-all duration-300 touch-manipulation border border-white/10 hover:border-white/25 shadow-lg hover:shadow-xl opacity-60 hover:opacity-100"
          aria-label={t.languageSwitch}
          style={{ minHeight: '44px' }}
        >
          <Languages className="w-4 h-4 text-white/80" />
          <span className="text-white/80 text-xs font-medium">
            {languageNames[language]}
          </span>
          <ChevronDown className={`w-3.5 h-3.5 text-white/80 transition-transform duration-300 ${showLangMenu ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* Toast 提示 */}
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}

      {state === 'input' && (
        <>
          {/* 标题 */}
          <h1 className="destiny-title">
            {t.appTitle}
          </h1>

          {/* 输入框 */}
          <input
            ref={inputRef}
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleDivine()}
            placeholder={t.inputPlaceholder}
            className="destiny-input touch-manipulation"
            maxLength={200}
            autoComplete="off"
            autoCorrect="off"
            autoCapitalize="off"
            spellCheck={false}
          />

          {/* 按钮 */}
          <button
            onClick={handleDivine}
            className="destiny-button mt-6 touch-manipulation"
          >
            {getRandomButtonText()}
          </button>
        </>
      )}

      {state === 'loading' && (
        <div className="destiny-loading">
          <div className="destiny-spinner"></div>
          <p className="text-2xl font-semibold text-white drop-shadow-lg animate-pulse-slow">
            {t.loadingText}
          </p>
        </div>
      )}

      {state === 'result' && result && (
        <div className="destiny-card">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-destiny font-bold mb-4 bg-gradient-to-r from-[#E0C3FC] via-[#8EC5FC] to-[#E0C3FC] bg-clip-text text-transparent drop-shadow-lg">
              {t.resultTitle}
            </h2>
            <div className="flex items-center justify-center gap-2">
              <div className="w-12 h-[2px] bg-gradient-to-r from-transparent via-[#8EC5FC] to-transparent rounded-full"></div>
              <div className="w-2 h-2 rounded-full bg-[#8EC5FC] shadow-lg shadow-[#8EC5FC]/50"></div>
              <div className="w-12 h-[2px] bg-gradient-to-r from-transparent via-[#8EC5FC] to-transparent rounded-full"></div>
            </div>
          </div>

          <p className="destiny-result">
            {result.text}
          </p>

          <div className="flex justify-center gap-4 mt-8 px-4 flex-wrap">
            <button
              onClick={handleShare}
              className="flex items-center space-x-2 px-6 py-3.5 backdrop-blur-xl bg-gradient-to-r from-pink-500/25 to-purple-500/25 hover:from-pink-500/35 hover:to-purple-500/35 active:from-pink-500/40 active:to-purple-500/40 rounded-2xl transition-all duration-300 touch-manipulation border border-white/30 hover:border-white/40 shadow-lg hover:shadow-xl hover:-translate-y-1"
              style={{ minHeight: '48px' }}
            >
              <Share2 className="w-5 h-5" />
              <span className="font-semibold">{t.shareButton}</span>
            </button>

            <button
              onClick={handleRestart}
              className="flex items-center space-x-2 px-6 py-3.5 backdrop-blur-xl bg-white/10 hover:bg-white/20 active:bg-white/25 rounded-2xl transition-all duration-300 touch-manipulation border border-white/30 hover:border-white/40 shadow-lg hover:shadow-xl hover:-translate-y-1"
              style={{ minHeight: '48px' }}
            >
              <RotateCcw className="w-5 h-5" />
              <span className="font-semibold">{t.restartButton}</span>
            </button>
          </div>
        </div>
      )}

      {state === 'error' && (
        <div className="destiny-card">
          <div className="text-center">
            <div className="text-7xl mb-6 animate-bounce-subtle">⚠️</div>
            <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent drop-shadow-lg">
              {t.errorTitle}
            </h2>
            <p className="text-white/90 mb-8 text-lg">
              {error}
            </p>
            <button
              onClick={handleRestart}
              className="destiny-button touch-manipulation"
            >
              {t.retryButton}
            </button>
          </div>
        </div>
      )}
      </div>
    </>
  );
};

export default App;