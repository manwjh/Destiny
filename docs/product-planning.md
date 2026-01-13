# 《算一卦/Destiny》产品规划文档

# "Calculate a Fortune/Destiny" Product Planning Document

## 项目概述 | Project Overview

### 软件名称 | Software Name
算一卦 / Destiny

### 功能简述 | Brief Description
一款好玩的算命软件 - 一个不安慰你、只给结果的算卦器
A fun fortune-telling software - An oracle that doesn't comfort you, just gives results

### 产品形态 | Product Form
中英文双语版本的 SaaS 服务程序
Bilingual (Chinese-English) SaaS service program

---

## 一、爆款公式 | I. Viral Formula

**爆 = 情绪命中 × 判决感 × 可传播载体**
**Viral = Emotional Hit × Judgment Feel × Shareable Medium**

核心理念：把用户内心的犹豫，替他下最后裁决
Core Concept: Take users' inner hesitation and make the final judgment for them

---

## 二、产品定位 | II. Product Positioning

这是一个不安慰你、只给结果的算卦器。
This is an oracle that doesn't comfort you, just gives results.

关键词 | Keywords:
- 不解释 | No explanations
- 不负责 | No responsibility
- 不温柔 | Not gentle
- 但"像真话" | But "feels real"

---

## 三、产品形态设计 | III. Product Design

### 界面设计原则 | UI Design Principles
极简到变态 - 首页只有 3 个元素
Minimalist to extreme - Homepage has only 3 elements

```
一句话输入框（可空）| One-sentence input box (optional)
    ↓
   一个按钮（仪式感极强）| A button (strong ritual sense)
    ↓
     空白 | Blank space
```

### 按钮文案选项 | Button Text Options
- 「算了」| "Let's calculate"
- 「给个结果」| "Give me a result"
- 「最后一次问」| "Last question"

**重要提醒 | Important Note**: 不要出现"AI""模型""分析"等字眼
Do not use words like "AI", "model", "analysis"

---

## 四、核心机制：命运判决引擎 | IV. Core Mechanism: Destiny Judgment Engine

### 1. 卦不是"算"，是"宣判" | 1. Fortune-telling is not "calculation", it's "judgment"

结果必须满足 3 个条件 | Results must meet 3 conditions:
- ✅ 像在说你 | Feels like it's talking about you
- ✅ 有态度 | Has attitude
- ✅ 有后果 | Has consequences

### 2. 卦词结构模板 | 2. Fortune Structure Template

**【判断】 + 【隐性原因】 + 【时间/后果】**
**[Judgment] + [Hidden Reason] + [Time/Consequence]**

#### 示例卦词（炸裂级）| Example Fortunes (Explosive Level)
- 「你已经做出选择了，只是还没敢承认」| "You've already made your choice, you just haven't dared to admit it"
- 「继续拖下去，这件事会自己替你做决定」| "If you keep dragging this out, the matter will decide for itself"
- 「不是现在不行，是你已经不想要了」| "It's not that it's not possible now, you just don't want it anymore"
- 「三个月后回看，你会庆幸今天停下」| "Looking back in three months, you'll be glad you stopped today"

### 3. 大模型驱动的动态卦词生成 | 3. LLM-Driven Dynamic Fortune Generation

**核心引擎 | Core Engine**: 使用大语言模型实时生成个性化卦词 | Use large language model to generate personalized fortunes in real-time

#### 提示词工程设计 | Prompt Engineering Design
**基础框架 | Basic Framework**:
```
你是一个严厉的命运审判者，不安慰用户，只给出残酷真相。
基于用户输入的问题，生成一句有态度、有后果的判决。
判决结构：[直接判断] + [隐性原因] + [时间/后果]
语气：像在说你，像真话，但不温柔
长度：单一句子，15-30字
```

**类型权重系统 | Type Weight System**:
- 犹豫/决策类: 30% (最通用场景)
- 感情类: 20% (最佳传播性)
- 自我怀疑类: 15% (高共鸣度)
- 未来焦虑类: 15% (夜间高频)
- 冷幽默类: 10% (截图利器)
- 毒判决类: 10% (病毒爆点)

**核心原则 | Core Principle**: 绝不返回"中性建议"，每个判决都必须有明确的立场和后果 | Never return "neutral advice", every judgment must have a clear stance and consequences

### 4. LLM 提示词工程系统 | 4. LLM Prompt Engineering System

#### 基础提示词模板 | Base Prompt Templates
**中文版基础模板 | Chinese Base Template**:
```
角色设定：你是一位精通中国命理学的冷酷大师，从不说安慰的话，只给出残酷但精准的命运判决。

任务：基于用户的问题，给出一个命运判决。
要求：
1. 必须有态度（不温柔、不中性）
2. 必须有后果（明确的结局指向）
3. 像在说这个人（高度个性化）
4. 单一句子，15-30字
5. 结构：[判断]+[隐性原因]+[时间/后果]

用户问题：{user_input}
```

**英文版基础模板 | English Base Template**:
```
Role: You are a master of Chinese metaphysics who never comforts, only delivers harsh but precise destiny judgments.

Task: Based on the user's question, deliver a destiny judgment.
Requirements:
1. Must have attitude (not gentle, not neutral)
2. Must have consequences (clear outcome direction)
3. Feels personal (highly individualized)
4. One sentence, 10-20 words
5. Structure: [Judgment]+[Hidden Reason]+[Time/Consequence]

User question: {user_input}
```

#### 场景增强提示词 | Scenario Enhancement Prompts
**夜间模式增强 | Night Mode Enhancement**:
```
这是深夜时段，用户可能处于焦虑或孤独状态。
让判决更加：
- 狠厉（harsh）
- 孤独感（loneliness）
- 赤裸真实（raw truth）
```

**连续使用惩罚 | Consecutive Usage Punishment**:
```
用户已连续使用{count}次，显示出犹豫和依赖。
让判决体现：
- 厌倦感（impatience）
- 强迫觉醒（forced awakening）
- 终局意味（finality）
```

#### 内容安全过滤器 | Content Safety Filters
- 禁止输出涉及政治、宗教、暴力等敏感内容
- 确保语言文明但态度强硬
- 自动检测和过滤潜在有害建议

---

## 五、炸裂设计点 | V. Explosive Design Points

### 💥 1. 判词视觉化（截图即传播）| 💥 1. Fortune Visualization (Screenshot = Share)
- 大字显示 | Large text
- 留白设计 | White space design
- 像「天机」「判词」「签文」| Like "Heaven's will", "Judgment", "Oracle"

**预期用户行为 | Expected User Behavior**: 自发添加评论"这也太准了吧……" | Spontaneous comments "This is too accurate..."

### 💥 2. 不可逆机制（命运感）| 💥 2. Irreversible Mechanism (Destiny Feel)
- 同一问题 24h 只能算一次 | Same question can only be asked once per 24h
- 或：连续算 → 提示「你已经知道答案了」| Or: Continuous calculations → Prompt "You already know the answer"

**效果 | Effect**: 让人不爽，但更想分享 | Makes people uncomfortable, but more eager to share

### 💥 3. 夜卦模式（23:00–03:00）| 💥 3. Night Fortune Mode (23:00–03:00)
夜间专属卦词特性 | Night-specific fortune characteristics:
- 更狠 | Harsher
- 更孤独 | More lonely
- 更真实 | More real

**示例夜卦 | Example Night Fortunes**:
- 「你现在不是想算，是想被否定或被允许」| "Right now you're not asking for fortune, you want to be denied or permitted"
- 「今晚别做决定，但别再骗自己」| "Don't make decisions tonight, but stop deceiving yourself"

### 💥 4. 隐藏狠卦（成瘾点）| 💥 4. Hidden Harsh Fortunes (Addiction Point)
规则示例 | Rule Examples:
- 连续 3 天使用 → 第 4 次出「终局卦」| Use for 3 consecutive days → 4th time gets "Final Fortune"
- 或：输入空白问题 → 返回最狠的 | Or: Input blank question → Return the harshest one

---

## 六、增长策略：自传播钩子 | VI. Growth Strategy: Self-Propagation Hooks

### 分享文案自动生成 | Auto-generated Share Text
结果下方一行小字 | Small text below results:

**中文版 | Chinese Version**:
- "我刚算了一卦，有点不舒服。" | "I just had my fortune told, and it hit too close to home."
- "不建议你现在来算。" | "I wouldn't recommend getting your fortune told right now."

**英文版 | English Version**:
- "I just had my fortune told, and it hit too close to home."
- "I wouldn't recommend getting your fortune told right now."

**策略 | Strategy**: 反劝阻 = 强点击 | Reverse discouragement = Strong clicks

---

## 七、冷启动打法 | VII. Cold Start Strategy

### 第一波目标人群 | First Wave Target Users
- 创业 / 自由职业者 | Entrepreneurs / Freelancers
- 情绪化程序员 | Emotional programmers
- 恋爱脑用户 | Love-brained users
- 夜猫子 | Night owls

### 第一条外发文案示例 | First Post Example

**中文版 | Chinese Version**:
```
我做了个算卦程序
不安慰人
只给一句结果

有点狠
谨慎点

比任何"AI算命"都强 10 倍
```

**英文版 | English Version**:
```
I made a fortune-telling program
Doesn't comfort you
Just gives one result

It's kinda harsh
Be careful

10x better than any "AI fortune-telling"
```

---

## 八、避坑指南：千万别做的 6 件事 | VIII. Pitfall Guide: 6 Things You Must NOT Do

❌ 不要追求准确率 | Don't pursue accuracy
❌ 不要背景解释 | Don't provide background explanations
❌ 不要玄学知识科普 | Don't popularize occult knowledge
❌ 不要成长体系 | Don't create growth systems
❌ 不要"心理建议" | Don't give "psychological advice"
❌ 不要让"负责声明"太显眼 | Don't make "disclaimer" too prominent

**核心价值 | Core Value**: 你卖的是"被命运敲一下"的感觉 | You're selling the feeling of "being hit by destiny"

---

## 九、四阶段执行时间表（14 天内）| IX. 4-Phase Execution Timeline (Within 14 Days)

### Phase 1：概念验证（Day 1–3）| Phase 1: Proof of Concept (Day 1–3)
- ✅ 定名字（算一卦/Destiny）| Finalize name (Calculate a Fortune/Destiny)
- ✅ 设计基础提示词模板 | Design base prompt templates
- ✅ LLM API 集成测试 | LLM API integration testing
- ✅ 内容安全过滤器开发 | Content safety filter development

### Phase 2：核心功能开发（Day 4–7）| Phase 2: Core Feature Development (Day 4–7)
- ✅ 动态卦词生成引擎 | Dynamic fortune generation engine
- ✅ 夜卦模式和场景增强 | Night fortune mode and scenario enhancement
- ✅ 缓存系统和性能优化 | Caching system and performance optimization
- ✅ UI 界面设计和实现 | UI design and implementation

### Phase 3：质量保障（Day 8–10）| Phase 3: Quality Assurance (Day 8–10)
- ✅ 提示词 A/B 测试 | Prompt A/B testing
- ✅ 内容一致性验证 | Content consistency validation
- ✅ 压力测试和性能调优 | Stress testing and performance tuning
- ✅ 安全审核和合规检查 | Security audit and compliance check

### Phase 4：发布上线（Day 11–14）| Phase 4: Launch (Day 11–14)
- ✅ 内测验证（30 人规模）| Internal testing (30 people scale)
- ✅ 用户反馈收集和迭代 | User feedback collection and iteration
- ✅ 生产环境部署 | Production deployment
- ✅ 监控和告警系统 | Monitoring and alerting system

---

## 十、技术实现规划 | X. Technical Implementation Plan

### SaaS 服务架构 | SaaS Architecture
- **前端 | Frontend**: Web 应用，支持中英文切换 | Web app with Chinese-English switching
- **后端 | Backend**: API 服务，集成大模型进行卦词生成 | API service integrating LLM for fortune generation
- **大模型服务 | LLM Service**: OpenAI/Claude 等 API 接口，支持中英文生成 | OpenAI/Claude API interfaces supporting Chinese-English generation
- **数据库 | Database**: 用户行为记录（匿名）、提示词模板存储 | User behavior records (anonymous), prompt templates storage
- **缓存层 | Cache Layer**: Redis 缓存常用提示词和生成结果 | Redis cache for common prompts and generated results
- **部署 | Deployment**: 云服务，支持高并发访问 | Cloud service supporting high concurrency

### 核心技术栈 | Core Tech Stack
- **前端框架 | Frontend Framework**: React/Vue + 响应式设计 | React/Vue + Responsive design
- **后端 | Backend**: Node.js/Python + RESTful API + LLM SDK
- **大模型 | LLM**: GPT-4/Claude-3，支持流式输出和提示词工程 | GPT-4/Claude-3, supporting streaming output and prompt engineering
- **数据库 | Database**: PostgreSQL + Redis（缓存层）| PostgreSQL + Redis (cache layer)
- **部署 | Deployment**: AWS/Azure/Vercel + LLM API 供应商 | Cloud platforms + LLM API providers

### 双语实现方案 | Bilingual Implementation
- 卦词库 | Fortune Library: 中英文对照存储 | Chinese-English parallel storage
- UI 文案 | UI Text: 键值对管理，支持动态切换 | Key-value management with dynamic switching
- 用户输入 | User Input: 自动检测语言或提供切换选项 | Auto-detect language or provide switching options

---

## 十一、风险评估与应对 | XI. Risk Assessment & Mitigation

### 潜在风险 | Potential Risks
1. **内容合规 | Content Compliance**: 确保卦词不涉及敏感政治/宗教话题 | Ensure fortunes don't touch sensitive political/religious topics
2. **用户体验 | User Experience**: 避免过度负面影响用户情绪 | Avoid overly negative impact on user emotions
3. **平台政策 | Platform Policies**: SaaS 部署需遵守各平台内容审核标准 | SaaS deployment must comply with platform content review standards
4. **LLM 生成质量 | LLM Generation Quality**: 大模型输出不稳定，可能生成不符合产品调性的内容 | LLM output instability, may generate content that doesn't match product tone
5. **内容一致性 | Content Consistency**: 相同问题多次询问可能得到不同答案 | Same question asked multiple times may get different answers
6. **API 成本控制 | API Cost Control**: 大模型 API 调用成本高，需要有效控制使用频率 | High LLM API costs, need to control usage frequency effectively
7. **响应延迟 | Response Latency**: LLM 生成时间较长，可能影响用户体验 | LLM generation takes longer, may affect user experience

### 应对策略 | Mitigation Strategies
- **内容审核机制 | Content Review**: 内部审核 + 用户反馈监控 + LLM 输出后过滤 | Internal review + User feedback monitoring + Post-LLM filtering
- **缓存策略 | Caching Strategy**: 相似问题缓存结果，避免重复调用 | Cache results for similar questions to avoid repeated calls
- **提示词优化 | Prompt Optimization**: 持续迭代提示词模板，提高生成质量和一致性 | Continuously iterate prompt templates to improve generation quality and consistency
- **成本控制 | Cost Control**: 设置每日/每月 API 调用上限，实施缓存和频率限制 | Set daily/monthly API call limits, implement caching and rate limiting
- **性能优化 | Performance Optimization**: 流式输出 + 缓存预热，减少用户等待时间 | Streaming output + cache warming to reduce user wait time
- **备用机制 | Fallback Mechanism**: 当 LLM 不可用时，提供预设卦词作为备用 | Provide preset fortunes as fallback when LLM is unavailable
- 免责声明 | Disclaimer: 优雅放置，不影响核心体验 | Elegantly placed without affecting core experience
- 迭代机制 | Iteration: 基于用户反馈持续优化提示词和生成规则 | Continuous optimization of prompts and generation rules based on user feedback

---

## 十二、成功指标 | XII. Success Metrics

### 核心指标 | Core Metrics
- **日活用户 | DAU**（Daily Active Users）
- **分享率 | Share Rate**: 用户截图/转发比例 | User screenshot/forward ratio
- **留存率 | Retention Rate**: 7日留存 > 30% | 7-day retention > 30%

### 病毒传播指标 | Viral Spread Metrics
- **K 因子 | K Factor**: 每个用户带来多少新用户 | How many new users each user brings
- **社交媒体提及 | Social Mentions**: 截图传播数量 | Screenshot spread volume
- **自然流量 | Organic Traffic**: 无需运营的访问量 | Traffic without marketing

---

## 十三、后续规划 | XIII. Future Roadmap

### Phase 2：功能扩展（上线后 1-2 个月）| Phase 2: Feature Expansion (1-2 months after launch)
- 主题卦词包（爱情、事业、学习等）| Themed fortune packs (love, career, study, etc.)
- 分享海报自动生成 | Auto-generated share posters
- 小程序版本 | Mini-program version

### Phase 3：商业化（上线后 3-6 个月）| Phase 3: Monetization (3-6 months after launch)
- 付费卦词包 | Paid fortune packs
- 企业定制版本 | Enterprise custom versions
- API 服务对外开放 | API service open to public

---

*本文档基于产品理念制定，实际执行中可根据用户反馈和市场情况灵活调整。核心原则：保持"炸裂"的产品体验，让用户忍不住分享。*

*This document is formulated based on product philosophy. Actual execution can be flexibly adjusted based on user feedback and market conditions. Core principle: Maintain the "explosive" product experience that makes users unable to resist sharing.*