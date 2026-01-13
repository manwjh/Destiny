// 语言类型定义
export type Language = 'zh-CN' | 'zh-TW' | 'en';

// 翻译文本接口
export interface Translations {
  // 应用标题
  appTitle: string;
  
  // 输入界面
  inputPlaceholder: string;
  characterCount: string;
  
  // 按钮文案
  buttonTexts: string[];
  
  // 加载状态
  loadingText: string;
  
  // 结果页面
  resultTitle: string;
  shareButton: string;
  restartButton: string;
  
  // 错误页面
  errorTitle: string;
  retryButton: string;
  
  // 验证消息
  validation: {
    empty: string;
    tooShort: string;
    tooLong: string;
  };
  
  // Toast 消息
  toast: {
    copied: string;
    shareFailed: string;
  };
  
  // 分享文案
  shareTexts: string[];
  
  // 错误消息
  errorMessage: string;
  
  // 卦词示例（用于模拟API）
  fortuneExamples: string[];
  
  // 语言切换
  languageSwitch: string;
}

// 简体中文
export const zhCN: Translations = {
  appTitle: '《算一卦》',
  inputPlaceholder: '输入你的问题...',
  characterCount: '/200',
  buttonTexts: ['算了', '给个结果', '最后一次问', '告诉我真相'],
  loadingText: '正在解读命运之轮...',
  resultTitle: '命运判决',
  shareButton: '分享',
  restartButton: '重新算',
  errorTitle: '连接超时',
  retryButton: '重试',
  validation: {
    empty: '请输入你的问题',
    tooShort: '问题太短了，请详细描述',
    tooLong: '问题太长了，请精简一下',
  },
  toast: {
    copied: '已复制到剪贴板',
    shareFailed: '分享失败',
  },
  shareTexts: [
    '我刚算了一卦，有点不舒服。',
    '不建议你现在来算。',
  ],
  errorMessage: '命运之轮暂时卡住了，请稍后再试',
  fortuneExamples: [
    '你已经在犹豫中失去了最佳时机',
    '继续拖下去，这件事会自己替你做决定',
    '不是现在不行，是你已经不想要了',
    '三个月后回看，你会庆幸今天停下',
    '你所谓的"还没准备好"，其实是"不敢面对"',
    '你已经做出选择了，只是还没敢承认',
    '你现在不是想算，是想被否定或被允许',
    '今晚别做决定，但别再骗自己',
  ],
  languageSwitch: '切换语言',
};

// 繁体中文
export const zhTW: Translations = {
  appTitle: '《算一卦》',
  inputPlaceholder: '輸入你的問題...',
  characterCount: '/200',
  buttonTexts: ['算了', '給個結果', '最後一次問', '告訴我真相'],
  loadingText: '正在解讀命運之輪...',
  resultTitle: '命運判決',
  shareButton: '分享',
  restartButton: '重新算',
  errorTitle: '連接超時',
  retryButton: '重試',
  validation: {
    empty: '請輸入你的問題',
    tooShort: '問題太短了，請詳細描述',
    tooLong: '問題太長了，請精簡一下',
  },
  toast: {
    copied: '已複製到剪貼板',
    shareFailed: '分享失敗',
  },
  shareTexts: [
    '我剛算了一卦，有點不舒服。',
    '不建議你現在來算。',
  ],
  errorMessage: '命運之輪暫時卡住了，請稍後再試',
  fortuneExamples: [
    '你已經在猶豫中失去了最佳時機',
    '繼續拖下去，這件事會自己替你做決定',
    '不是現在不行，是你已經不想要了',
    '三個月後回看，你會慶幸今天停下',
    '你所謂的「還沒準備好」，其實是「不敢面對」',
    '你已經做出選擇了，只是還沒敢承認',
    '你現在不是想算，是想被否定或被允許',
    '今晚別做決定，但別再騙自己',
  ],
  languageSwitch: '切換語言',
};

// 英文
export const en: Translations = {
  appTitle: 'Calculate a Fortune',
  inputPlaceholder: 'What\'s on your mind?',
  characterCount: '/200',
  buttonTexts: ['Calculate', 'Give me an answer', 'Final question', 'Tell me the truth'],
  loadingText: 'Interpreting the wheel of destiny...',
  resultTitle: 'Destiny Judgment',
  shareButton: 'Share',
  restartButton: 'Try Again',
  errorTitle: 'Connection Timeout',
  retryButton: 'Retry',
  validation: {
    empty: 'Please enter your question',
    tooShort: 'Question too short, please be more specific',
    tooLong: 'Question too long, please shorten it',
  },
  toast: {
    copied: 'Copied to clipboard',
    shareFailed: 'Share failed',
  },
  shareTexts: [
    'I just had my fortune told, and it hit too close to home.',
    'I wouldn\'t recommend getting your fortune told right now.',
  ],
  errorMessage: 'The wheel of destiny is stuck, please try again later',
  fortuneExamples: [
    'You\'ve already lost the best timing in your hesitation',
    'If you keep dragging this out, the matter will decide for itself',
    'It\'s not that it\'s not possible now, you just don\'t want it anymore',
    'Looking back in three months, you\'ll be glad you stopped today',
    'What you call "not ready yet" is actually "not daring to face it"',
    'You\'ve already made your choice, you just haven\'t dared to admit it',
    'Right now you\'re not asking for fortune, you want to be denied or permitted',
    'Don\'t make decisions tonight, but stop deceiving yourself',
  ],
  languageSwitch: 'Switch Language',
};

// 语言配置映射
export const translations: Record<Language, Translations> = {
  'zh-CN': zhCN,
  'zh-TW': zhTW,
  'en': en,
};

// 语言显示名称
export const languageNames: Record<Language, string> = {
  'zh-CN': '简体中文',
  'zh-TW': '繁體中文',
  'en': 'English',
};
