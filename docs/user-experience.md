# 《算一卦/Destiny》用户体验流程文档

# "Calculate a Fortune/Destiny" User Experience Flow Document

## 概述 | Overview

### 产品定位 | Product Positioning
《算一卦》是一个**不安慰你、只给结果**的算命服务。用户体验设计原则：
- **极简**: 界面元素最少，专注核心功能
- **仪式感**: 营造神秘而庄重的体验
- **真实性**: 结果像"真话"，不回避残酷现实
- **分享性**: 结果天然适合截图分享

### 目标用户 | Target Users
- **情绪化决策者**: 面临选择时寻求外部意见
- **年轻人**: 18-35岁，对玄学感兴趣但理性
- **夜猫子**: 深夜时分寻求精神寄托
- **好奇者**: 对算命感兴趣但不迷信

---

## 用户旅程图 | User Journey Map

### 完整用户旅程 | Complete User Journey

```
用户发现 → 进入网站 → 首次交互 → 获得结果 → 结果消费 → 分享传播 → 重复使用
   ↓         ↓         ↓         ↓         ↓         ↓         ↓
好奇      吸引      引导      震惊      反思      病毒      习惯
```

#### 阶段1：发现阶段 (Awareness)
**触发点**: 朋友分享、社交媒体、自然搜索
**心理状态**: 好奇、犹豫、寻求答案
**目标**: 吸引用户点击进入

#### 阶段2：进入阶段 (Entry)
**首次印象**: 极简神秘的界面
**停留时间**: 3-5秒决定是否继续
**目标**: 降低认知负荷，快速引导操作

#### 阶段3：交互阶段 (Interaction)
**核心动作**: 输入问题，点击算卦
**等待时间**: 2-5秒 (LLM生成时间)
**目标**: 营造仪式感，管理期望

#### 阶段4：结果阶段 (Result)
**关键时刻**: 看到命运判决
**情绪反应**: 震惊、认同、否认、不适
**目标**: 引发共鸣，激发分享欲望

#### 阶段5：消费阶段 (Consumption)
**用户行为**: 反复阅读、截图保存、@朋友
**停留时间**: 1-3分钟
**目标**: 延长 engagement，增加分享

---

## 详细交互流程 | Detailed Interaction Flow

### 1. 页面加载 | Page Loading

#### 初始状态 | Initial State
```
┌─────────────────────────────────────┐
│                                     │
│           《算一卦》                  │
│        Calculate a Fortune          │
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │        输入你的问题...        │   │
│  │     What's on your mind?     │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│         [   算了   ]               │
│                                     │
└─────────────────────────────────────┘
```

**设计要点**:
- 背景: 深色渐变，营造神秘氛围
- 字体: 书法风格标题，现代简洁正文
- 布局: 居中对齐，垂直居中
- 颜色: 主色调 #2D1B69 (深紫)，强调色 #FF6B6B (珊瑚红)

### 2. 输入交互 | Input Interaction

#### 输入框设计 | Input Design
```javascript
// 输入框状态管理
const [question, setQuestion] = useState('');
const [isFocused, setIsFocused] = useState(false);

<input
  placeholder={language === 'zh' ? "输入你的问题..." : "What's on your mind?"}
  value={question}
  onChange={(e) => setQuestion(e.target.value)}
  onFocus={() => setIsFocused(true)}
  onBlur={() => setIsFocused(false)}
  maxLength={200}
  className={`input ${isFocused ? 'focused' : ''}`}
/>
```

**交互特性**:
- **自动聚焦**: 页面加载后自动聚焦输入框
- **字符限制**: 最多200字符，实时显示计数
- **语言切换**: 支持中英文无缝切换
- **键盘优化**: 移动端自动弹出合适键盘

#### 输入验证 | Input Validation
```javascript
const validateQuestion = (question) => {
  if (!question.trim()) {
    return { valid: false, message: "请输入你的问题" };
  }
  if (question.length < 3) {
    return { valid: false, message: "问题太短了，请详细描述" };
  }
  if (question.length > 200) {
    return { valid: false, message: "问题太长了，请精简一下" };
  }
  return { valid: true };
};
```

### 3. 算卦按钮 | Divine Button

#### 按钮状态 | Button States
```javascript
const [isLoading, setIsLoading] = useState(false);
const [isDisabled, setIsDisabled] = useState(false);

// 按钮文案随机池
const buttonTexts = {
  zh: ["算了", "给个结果", "最后一次问", "告诉我真相"],
  en: ["Calculate", "Give me an answer", "Final question", "Tell me the truth"]
};

const getRandomButtonText = () => {
  const texts = buttonTexts[language];
  return texts[Math.floor(Math.random() * texts.length)];
};
```

**按钮设计**:
- **形状**: 圆角矩形，仪式感强
- **动画**: 点击时有微妙的光晕效果
- **状态**: 正常/加载中/禁用 三种状态
- **文案**: 每次刷新随机变化

#### 点击交互 | Click Interaction
```javascript
const handleDivine = async () => {
  if (!validateQuestion(question).valid) {
    showToast(validateQuestion(question).message);
    return;
  }

  setIsLoading(true);
  setIsDisabled(true);

  try {
    const result = await api.divine(question, language);
    setResult(result);
    setShowResult(true);
  } catch (error) {
    showError("命运之轮暂时卡住了，请稍后再试");
  } finally {
    setIsLoading(false);
    setIsDisabled(false);
  }
};
```

### 4. 加载状态 | Loading State

#### 加载动画 | Loading Animation
```
┌─────────────────────────────────────┐
│                                     │
│           《算一卦》                  │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 正在解读命运之轮...          │   │
│  │ Interpreting the wheel...    │   │
│  └─────────────────────────────┘   │
│                                     │
│         [命运之轮转动中...]        │
│                                     │
│  ⏳ 加载指示器动画                 │
│                                     │
└─────────────────────────────────────┘
```

**加载设计**:
- **时长**: 2-4秒 (模拟仪式感)
- **动画**: 旋转的命运轮盘或水波纹
- **文案**: 神秘而有趣的提示文字
- **进度**: 不显示具体进度条，保持神秘感

### 5. 结果展示 | Result Display

#### 结果卡片 | Result Card
```javascript
const ResultCard = ({ result, language }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // 延迟显示，营造戏剧效果
    const timer = setTimeout(() => setIsVisible(true), 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`result-card ${isVisible ? 'visible' : ''}`}>
      <div className="result-header">
        {language === 'zh' ? '命运判决' : 'Destiny Judgment'}
      </div>
      <div className="result-content">
        {result.text}
      </div>
      <div className="result-footer">
        <ShareButton result={result} />
        <NewQuestionButton />
      </div>
    </div>
  );
};
```

**视觉设计**:
- **字体**: 大字号 (24-32px)，易读性强
- **留白**: 大量留白，营造庄重感
- **边框**: 古风装饰边框
- **动画**: 从下往上滑入效果

#### 结果内容 | Result Content
```javascript
// 示例结果结构
const sampleResult = {
  text: "你已经在犹豫中失去了最佳时机",
  language: "zh",
  timestamp: 1703123456,
  shareText: "我刚算了一卦，有点不舒服。",
  category: "decision"
};
```

### 6. 分享机制 | Sharing Mechanism

#### 一键分享 | One-Click Share
```javascript
const ShareButton = ({ result }) => {
  const shareUrl = `${window.location.origin}?share=${encodeURIComponent(result.id)}`;
  const shareText = result.shareText;

  const handleShare = async () => {
    if (navigator.share) {
      // 原生分享API (移动端)
      await navigator.share({
        title: '《算一卦》',
        text: shareText,
        url: shareUrl
      });
    } else {
      // 复制到剪贴板
      await navigator.clipboard.writeText(`${shareText} ${shareUrl}`);
      showToast("已复制到剪贴板");
    }
  };

  return (
    <button onClick={handleShare} className="share-btn">
      📤 {language === 'zh' ? '分享' : 'Share'}
    </button>
  );
};
```

#### 分享优化 | Share Optimization
- **文案**: 自动生成吸引人的分享文案
- **截图友好**: 结果卡片设计适合截图
- **链接**: 支持分享链接再次访问
- **社交**: 集成微信、微博等平台分享

---

## 错误处理流程 | Error Handling Flow

### 1. 网络错误 | Network Error

#### 错误状态展示 | Error State Display
```
┌─────────────────────────────────────┐
│                                     │
│           ⚠️ 连接超时                │
│        Connection Timeout          │
│                                     │
│  命运之轮暂时卡住了，请稍后再试     │
│  The wheel of destiny is stuck...   │
│                                     │
│         [   重试   ]               │
│                                     │
└─────────────────────────────────────┘
```

**错误处理策略**:
- **重试机制**: 自动重试3次
- **降级方案**: 网络错误时显示预设结果
- **用户提示**: 友好的错误信息，不透露技术细节

### 2. LLM服务错误 | LLM Service Error

#### 备用机制 | Fallback Mechanism
```javascript
const FALLBACK_FORTUNES = {
  zh: [
    "时机未到，继续等待。",
    "答案在你心中，自己寻找。",
    "改变想法，重新选择。"
  ],
  en: [
    "The time is not right, keep waiting.",
    "The answer is in your heart, seek it yourself.",
    "Change your mind, choose again."
  ]
};

const getFallbackFortune = (language) => {
  const fortunes = FALLBACK_FORTUNES[language];
  return fortunes[Math.floor(Math.random() * fortunes.length)];
};
```

### 3. 输入验证错误 | Input Validation Error

#### 即时反馈 | Instant Feedback
```javascript
const Toast = ({ message, type }) => (
  <div className={`toast toast-${type}`}>
    {type === 'error' && '❌'}
    {type === 'success' && '✅'}
    {type === 'warning' && '⚠️'}
    {message}
  </div>
);
```

---

## 响应式设计 | Responsive Design

### 桌面端 (>1024px) | Desktop (>1024px)
- **布局**: 居中固定宽度 (800px)
- **交互**: 鼠标悬停效果丰富
- **展示**: 多列布局，更多信息

### 平板端 (768px-1024px) | Tablet (768px-1024px)
- **布局**: 自适应宽度，保持居中
- **交互**: 触摸优化，大按钮
- **字体**: 适当调整字号

### 移动端 (<768px) | Mobile (<768px)
- **布局**: 全宽设计，充分利用屏幕
- **输入**: 虚拟键盘优化
- **分享**: 原生分享API优先
- **加载**: 优化动画性能

---

## 性能优化 | Performance Optimization

### 1. 首屏加载 | First Screen Loading

#### 关键指标 | Key Metrics
- **First Contentful Paint**: < 1.5秒
- **Largest Contentful Paint**: < 2.5秒
- **First Input Delay**: < 100毫秒

#### 优化策略 | Optimization Strategies
```javascript
// 延迟加载非关键资源
const LazyResultCard = lazy(() => import('./ResultCard'));

// 预加载关键字体
const fontLink = document.createElement('link');
fontLink.rel = 'preload';
fontLink.href = '/fonts/destiny-font.woff2';
fontLink.as = 'font';
document.head.appendChild(fontLink);
```

### 2. 交互性能 | Interaction Performance

#### 动画优化 | Animation Optimization
```css
/* 使用transform和opacity优化动画性能 */
.result-card {
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity;
}

.result-card.entering {
  transform: translateY(20px);
  opacity: 0;
}

.result-card.entered {
  transform: translateY(0);
  opacity: 1;
}
```

### 3. 缓存策略 | Caching Strategy

#### 浏览器缓存 | Browser Caching
```javascript
// Service Worker缓存策略
const CACHE_NAME = 'destiny-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        '/',
        '/static/css/main.css',
        '/static/js/main.js',
        '/manifest.json'
      ]);
    })
  );
});
```

---

## 无障碍设计 | Accessibility Design

### 1. 键盘导航 | Keyboard Navigation
- **Tab键**: 支持完整的键盘导航
- **Enter键**: 激活主要操作
- **Escape键**: 关闭模态框或返回

### 2. 屏幕阅读器 | Screen Reader Support
```html
<!-- ARIA标签支持 -->
<div role="main" aria-labelledby="app-title">
  <h1 id="app-title">《算一卦》</h1>
  <input
    aria-label="输入你的问题"
    aria-describedby="input-help"
    autocomplete="off"
  />
  <button aria-describedby="button-help">
    算了
  </button>
</div>
```

### 3. 高对比度支持 | High Contrast Support
- **颜色对比度**: 至少4.5:1
- **焦点指示器**: 清晰的焦点样式
- **字体大小**: 支持缩放至200%

---

## 数据收集与隐私 | Data Collection & Privacy

### 匿名数据收集 | Anonymous Data Collection
```javascript
const trackEvent = (eventName, data) => {
  // 匿名化处理
  const anonymousData = {
    event: eventName,
    timestamp: Date.now(),
    userId: hashUserIdentifier(), // 哈希处理，不存储原始标识
    language: data.language,
    questionLength: data.question?.length || 0,
    resultCategory: data.category,
    sessionDuration: data.duration
  };

  // 发送到分析服务
  analytics.track(anonymousData);
};
```

### 隐私保护措施 | Privacy Protection Measures
- **不存储问题原文**: 只存储问题长度和类别
- **匿名用户标识**: 使用哈希值而非真实ID
- **本地存储**: 敏感数据只在本地存储
- **透明声明**: 清晰的隐私政策链接

---

## 测试与迭代 | Testing & Iteration

### 1. 用户测试 | User Testing

#### A/B测试 | A/B Testing
```javascript
const experiments = {
  button_text: {
    control: "算了",
    variant: "告诉我真相"
  },
  loading_animation: {
    control: "命运之轮转动中...",
    variant: "正在解读天机..."
  }
};
```

#### 用户访谈要点 | User Interview Points
- 首次使用体验如何？
- 结果是否觉得"准"？
- 是否有分享欲望？
- 界面是否够简洁？
- 等待时间是否合适？

### 2. 指标监控 | Metrics Monitoring

#### 核心指标 | Core Metrics
- **转化率**: 访问 → 输入 → 算卦 → 分享
- **停留时间**: 平均会话时长
- **分享率**: 结果分享比例
- **重复访问**: 用户回访率

#### 体验指标 | Experience Metrics
- **加载时间**: 各步骤耗时
- **错误率**: 各类错误发生率
- **满意度**: 用户反馈评分

---

## 总结 | Summary

### 用户体验核心原则 | UX Core Principles

#### 🎯 极简至上 | Minimalism First
- **界面元素**: 最少化设计，专注核心功能
- **认知负荷**: 降低理解成本，快速上手
- **视觉干扰**: 去除冗余元素，保持专注

#### 🎭 仪式感营造 | Ritual Creation
- **神秘氛围**: 深色调、书法字体营造神秘感
- **等待体验**: 适当加载时间增强期待
- **结果呈现**: 戏剧化展示增强冲击力

#### 🔥 病毒传播 | Viral Spread
- **截图友好**: 结果卡片天然适合分享
- **文案优化**: 自动生成吸引人的分享内容
- **社交机制**: 一键分享到各大平台

#### 💡 真实反馈 | Authentic Feedback
- **不回避残酷**: 结果真实不粉饰
- **引发共鸣**: 戳中用户痛点
- **促进反思**: 让用户思考而非逃避

### 设计验证 | Design Validation

#### 用户反馈收集 | User Feedback Collection
- **定性研究**: 用户访谈和可用性测试
- **定量分析**: 数据指标和A/B测试结果
- **迭代优化**: 基于反馈持续改进

#### 成功指标 | Success Metrics
- **用户增长**: 日活跃用户 > 1000
- **分享率**: 每次算卦分享率 > 30%
- **留存率**: 7日留存率 > 25%
- **用户满意**: NPS评分 > 50

这个用户体验流程文档为《算一卦/Destiny》定义了完整的产品体验蓝图，确保用户从进入到分享的每一个环节都能获得优质体验！🎨✨