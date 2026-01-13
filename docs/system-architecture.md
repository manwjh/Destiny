# 《算一卦/Destiny》系统架构文档

# "Calculate a Fortune/Destiny" System Architecture Document

## 概述 | Overview

### 项目背景 | Project Background
《算一卦/Destiny》是一个基于大语言模型的中英文双语SaaS算命服务，采用极简设计理念，专注于提供"不安慰、只给结果"的命运判决体验。

### 架构目标 | Architecture Goals
- **高可用性**: 7×24小时稳定服务，支持高并发访问
- **低延迟**: 快速响应，确保用户体验流畅
- **成本控制**: 优化LLM API调用成本
- **可扩展性**: 支持业务快速增长
- **安全性**: 保护用户隐私，合规运营

### 核心业务流程 | Core Business Process
1. 用户输入问题 → 2. 语言检测 → 3. LLM生成判决 → 4. 内容审核 → 5. 结果展示 → 6. 行为记录

---

## 整体架构 | Overall Architecture

### 架构图 | Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    《算一卦/Destiny》 SaaS 平台                      │
│                    Calculate a Fortune/Destiny SaaS Platform     │
└─────────────────┬───────────────────────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │   用户界面层     │  ← Web前端 (React/Vue)
         │ User Interface  │
         └────────┬────────┘
                  │ HTTP/HTTPS
         ┌────────▼────────┐
         │   API网关层     │  ← Nginx/Cloudflare
         │   API Gateway   │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │   应用服务层     │  ← Node.js/Python + Express/FastAPI
         │ Application Layer│
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐   ┌────▼────┐   ┌───▼────┐
│ 大模型  │   │ 缓存层  │   │ 数据库  │
│  LLM    │   │  Cache  │   │   DB    │
│ Service │   │  Redis  │   │   PG    │
└────────┘   └─────────┘   └────────┘
```

### 架构分层 | Architecture Layers

#### 1. 用户界面层 | User Interface Layer
**技术栈**: React 18 + TypeScript + Tailwind CSS
**职责**:
- 极简UI设计（输入框+按钮+结果显示）
- 中英文动态切换
- 响应式设计，支持移动端
- 无需登录，匿名使用

#### 2. API网关层 | API Gateway Layer
**技术栈**: Nginx + Cloudflare
**职责**:
- 请求路由和负载均衡
- 速率限制和DDoS防护
- SSL/TLS终止
- 静态资源缓存

#### 3. 应用服务层 | Application Service Layer
**技术栈**: Node.js + Express 或 Python + FastAPI
**职责**:
- 业务逻辑处理
- LLM API集成
- 数据验证和转换
- 用户行为分析

#### 4. 数据存储层 | Data Storage Layer
**数据库**: PostgreSQL (主数据库)
**缓存**: Redis (热点数据缓存)
**对象存储**: AWS S3 (日志和备份)

#### 5. 大模型服务层 | LLM Service Layer
**供应商**: OpenAI GPT-4 + Anthropic Claude-3
**集成方式**: RESTful API + Streaming
**备用方案**: 本地预设卦词库

---

## 核心组件详解 | Core Components Details

### 1. 前端组件 | Frontend Components

#### 主页面组件 | Main Page Component
```typescript
interface DestinyAppProps {
  language: 'zh' | 'en';
  onLanguageSwitch: (lang: string) => void;
}

interface FortuneResult {
  text: string;
  timestamp: number;
  language: string;
  shareable: boolean;
}
```

**核心特性**:
- 单输入框设计（可空）
- 仪式感按钮（多种文案随机）
- 结果卡片式展示
- 自动截图优化

#### 语言检测与切换 | Language Detection & Switching
- 自动检测用户输入语言
- 提供手动切换选项
- 结果与输入语言保持一致

### 2. 后端服务架构 | Backend Service Architecture

#### API设计 | API Design
```
POST /api/v1/divine
Content-Type: application/json

{
  "question": "我应该辞职吗？",
  "language": "zh",
  "client_id": "anonymous_123"
}

Response:
{
  "result": "你已经在犹豫中失去了最佳时机",
  "language": "zh",
  "timestamp": 1703123456,
  "share_text": "我刚算了一卦，有点不舒服。"
}
```

#### 核心服务模块 | Core Service Modules

##### 命理引擎 | Destiny Engine
```python
class DestinyEngine:
    def __init__(self, llm_provider: str, cache_client: Redis):
        self.llm = LLMProvider(llm_provider)
        self.cache = cache_client
        self.templates = PromptTemplates()

    async def divine(self, question: str, language: str) -> FortuneResult:
        # 1. 检查缓存
        cached_result = await self.cache.get(f"{language}:{hash(question)}")
        if cached_result:
            return cached_result

        # 2. 生成提示词
        prompt = self.templates.generate_base_prompt(question, language)

        # 3. 调用LLM
        result = await self.llm.generate(prompt)

        # 4. 内容审核
        if not self.content_filter(result):
            result = self.fallback_fortune(language)

        # 5. 缓存结果
        await self.cache.set(f"{language}:{hash(question)}", result, ttl=3600)

        return result
```

##### 内容审核系统 | Content Review System
```python
class ContentFilter:
    def __init__(self):
        self.sensitive_words = self.load_sensitive_words()
        self.tone_analyzer = ToneAnalyzer()

    def filter(self, content: str, language: str) -> bool:
        # 检查敏感词
        if self.contains_sensitive_words(content):
            return False

        # 检查语气是否符合产品调性
        if not self.tone_analyzer.is_harsh_enough(content, language):
            return False

        return True
```

### 3. 数据存储设计 | Data Storage Design

#### 数据库表结构 | Database Schema

##### 用户行为表 | User Behavior Table
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id VARCHAR(255), -- 匿名用户标识
    question TEXT NOT NULL,
    language VARCHAR(2) NOT NULL,
    result TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_agent TEXT,
    ip_hash VARCHAR(64), -- 隐私保护
    response_time INTEGER -- 响应时间(ms)
);

-- 分区表，按月分区
CREATE TABLE user_sessions_y2024m01 PARTITION OF user_sessions
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

##### 提示词模板表 | Prompt Templates Table
```sql
CREATE TABLE prompt_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    language VARCHAR(2) NOT NULL,
    template_type VARCHAR(50), -- base/night/special
    template_content TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

##### 缓存设计 | Cache Design
```python
# Redis键设计
USER_QUESTION_CACHE_KEY = "destiny:question:{language}:{question_hash}"
TEMPLATE_CACHE_KEY = "destiny:template:{name}:{version}"
STATS_CACHE_KEY = "destiny:stats:daily:{date}"
```

### 4. 大模型集成 | LLM Integration

#### 多供应商架构 | Multi-Provider Architecture
```python
class LLMProviderManager:
    def __init__(self):
        self.providers = {
            'openai': OpenAIProvider(api_key=os.getenv('OPENAI_API_KEY')),
            'anthropic': AnthropicProvider(api_key=os.getenv('ANTHROPIC_API_KEY'))
        }
        self.current_provider = 'openai'  # 默认供应商

    async def generate(self, prompt: str) -> str:
        # 主供应商调用
        try:
            return await self.providers[self.current_provider].generate(prompt)
        except Exception as e:
            logger.warning(f"Primary provider failed: {e}")
            # 自动切换到备用供应商
            alt_provider = 'anthropic' if self.current_provider == 'openai' else 'openai'
            return await self.providers[alt_provider].generate(prompt)
```

#### 提示词管理系统 | Prompt Management System
- **版本控制**: 支持提示词A/B测试
- **性能监控**: 记录各版本生成质量和响应时间
- **自动优化**: 基于用户反馈调整提示词参数

---

## 部署架构 | Deployment Architecture

### 简化云服务架构 | Simplified Cloud Architecture

#### 阶段1：单服务器部署 (推荐初始方案) | Phase 1: Single Server Deployment (Recommended for Start)

```
┌─────────────────────────────────────────────────────┐
│                单台云服务器 (VPS)                     │
│              Single Cloud Server (VPS)              │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │   Nginx     │ │   Node.js   │ │ PostgreSQL  │   │
│  │  (Web服务器) │ │   API服务   │ │   数据库     │   │
│  │  Web Server │ │ API Service │ │  Database   │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
│         │               │                 │         │
│         └───────────────┼─────────────────┘         │
│                         │                           │
│              ┌──────────▼──────────┐                │
│              │     Redis缓存        │                │
│              │   Redis Cache       │                │
│              └─────────────────────┘                │
│                                                     │
│  ┌─────────────────────────────────────────────────┐ │
│  │           静态文件 (HTML/CSS/JS)                │ │
│  │         Static Files (HTML/CSS/JS)             │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                      │
           ┌──────────▼──────────┐
           │   LLM API服务       │
           │  LLM API Services   │
           │ (OpenAI/Claude)     │
           └─────────────────────┘
```

**服务器配置建议 | Server Configuration Recommendations**:
- **CPU**: 2-4核 (AMD/Intel)
- **内存**: 4-8GB RAM
- **存储**: 50-100GB SSD
- **带宽**: 3-5Mbps
- **月成本**: $20-50/月 (DigitalOcean/Linode等)

#### 阶段2：分离部署 (用户增长后) | Phase 2: Separated Deployment (After User Growth)

```
┌─────────────────────────────────┐    ┌─────────────────────────────────┐
│        前端服务器                  │    │        后端服务器                  │
│      Frontend Server             │    │      Backend Server              │
├─────────────────────────────────┤    ├─────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ │    │  ┌─────────────┐ ┌─────────────┐ │
│  │   Nginx     │ │   React     │ │    │  │   Node.js   │ │ PostgreSQL  │ │
│  │ Web Server  │ │    App      │ │    │  │ API Service │ │  Database   │ │
│  └─────────────┘ └─────────────┘ │    │  └─────────────┘ └─────────────┘ │
└─────────────────────────────────┘    │          │                         │
                                       │  ┌───────▼───────┐               │
                                       │  │   Redis缓存    │               │
                                       │  │ Redis Cache   │               │
                                       │  └───────────────┘               │
                                       └─────────────────────────────────┘
                                                │
                                     ┌──────────▼──────────┐
                                     │   LLM API服务       │
                                     │  LLM API Services   │
                                     │ (OpenAI/Claude)     │
                                     └─────────────────────┘
```

### 容器化部署 | Containerized Deployment

#### Docker Compose (开发环境) | Docker Compose (Development)
```yaml
version: '3.8'
services:
  web:
    build: ./frontend
    ports:
      - "80:80"
    volumes:
      - ./frontend/build:/usr/share/nginx/html:ro

  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/destiny
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: destiny
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
```

#### 生产环境部署脚本 | Production Deployment Script
```bash
#!/bin/bash
# 生产环境一键部署脚本 | Production deployment script

# 1. 更新系统 | Update system
sudo apt update && sudo apt upgrade -y

# 2. 安装 Docker 和 Docker Compose | Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. 创建项目目录 | Create project directory
sudo mkdir -p /opt/destiny
sudo chown $USER:$USER /opt/destiny

# 4. 复制项目文件 | Copy project files
cp -r . /opt/destiny/
cd /opt/destiny

# 5. 创建环境变量文件 | Create environment variables file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/destiny
REDIS_URL=redis://localhost:6379
NODE_ENV=production
EOF

# 6. 启动服务 | Start services
docker-compose up -d

# 7. 配置 Nginx 反向代理 | Configure Nginx reverse proxy
sudo apt install nginx -y
sudo tee /etc/nginx/sites-available/destiny << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/destiny /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo "部署完成！请配置域名和SSL证书。"
echo "Deployment completed! Please configure domain and SSL certificate."
```

---

## 性能优化策略 | Performance Optimization Strategies

### 1. 缓存策略 | Caching Strategies

#### 多层缓存架构 | Multi-Level Caching
- **浏览器缓存**: 静态资源缓存
- **CDN缓存**: 全球分布式缓存
- **应用缓存**: API响应缓存
- **数据库缓存**: 查询结果缓存

#### 智能缓存键设计 | Smart Cache Key Design
```python
def generate_cache_key(question: str, language: str) -> str:
    # 相似问题归一化
    normalized = normalize_question(question, language)
    question_hash = hashlib.md5(normalized.encode()).hexdigest()[:16]
    return f"destiny:{language}:{question_hash}"
```

### 2. LLM优化 | LLM Optimizations

#### 请求合并与批处理 | Request Batching
```python
class LLMRequestBatcher:
    def __init__(self, batch_size: int = 10, timeout: float = 0.1):
        self.batch_size = batch_size
        self.timeout = timeout
        self.requests = []

    async def add_request(self, prompt: str) -> Future[str]:
        future = Future()
        self.requests.append((prompt, future))

        # 如果达到批处理大小或超时，执行批处理
        if len(self.requests) >= self.batch_size:
            await self._execute_batch()
        else:
            asyncio.create_task(self._delayed_execute())

        return future
```

#### 流式输出 | Streaming Output
```python
@app.post("/api/v1/divine")
async def divine_endpoint(request: DivineRequest):
    return StreamingResponse(
        generate_fortune_stream(request.question, request.language),
        media_type="text/plain"
    )

async def generate_fortune_stream(question: str, language: str):
    async for chunk in llm_provider.stream_generate(prompt):
        yield chunk
        await asyncio.sleep(0.01)  # 控制输出速度
```

### 3. 数据库优化 | Database Optimizations

#### 分表策略 | Table Partitioning
```sql
-- 按时间分区
CREATE TABLE user_sessions_y2024 PARTITION OF user_sessions
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
    PARTITION BY RANGE (timestamp);

-- 按月份子分区
CREATE TABLE user_sessions_y2024m01 PARTITION OF user_sessions_y2024
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

#### 索引优化 | Index Optimization
```sql
-- 复合索引用于查询优化
CREATE INDEX idx_user_sessions_query ON user_sessions (
    language, timestamp DESC, client_id
);

-- 部分索引用于活跃用户
CREATE INDEX idx_active_sessions ON user_sessions (client_id, timestamp)
WHERE timestamp > NOW() - INTERVAL '30 days';
```

---

## 安全架构 | Security Architecture

### 1. 数据隐私保护 | Data Privacy Protection

#### 匿名化策略 | Anonymization Strategies
- **IP地址**: 只存储哈希值，不存储原始IP
- **用户标识**: 使用客户端生成的匿名ID
- **行为数据**: 聚合统计，不存储个人行为轨迹

#### 数据加密 | Data Encryption
```python
class DataEncryptor:
    def __init__(self, key: bytes):
        self.key = key
        self.cipher = AES.new(key, AES.MODE_GCM)

    def encrypt_sensitive_data(self, data: str) -> str:
        nonce = os.urandom(12)
        ciphertext, tag = self.cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(nonce + tag + ciphertext).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        raw = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = raw[:12], raw[12:28], raw[28:]
        return self.cipher.decrypt_and_verify(ciphertext, tag).decode()
```

### 2. API安全 | API Security

#### 速率限制 | Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/divine")
@limiter.limit("10/minute")
async def divine_endpoint(request: DivineRequest):
    # 单个IP每分钟最多10次请求
    return await destiny_engine.divine(request.question, request.language)
```

#### 输入验证 | Input Validation
```python
from pydantic import BaseModel, validator
from typing import Optional

class DivineRequest(BaseModel):
    question: str
    language: Optional[str] = "zh"

    @validator('question')
    def question_must_be_valid(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Question cannot be empty')
        if len(v) > 500:
            raise ValueError('Question too long')
        return v.strip()

    @validator('language')
    def language_must_be_supported(cls, v):
        if v not in ['zh', 'en']:
            raise ValueError('Unsupported language')
        return v
```

---

## 监控与运维 | Monitoring & Operations

### 简化监控方案 | Simplified Monitoring Solution

#### 基础监控指标 | Basic Monitoring Metrics
- **服务状态**: 应用是否正常运行
- **响应时间**: 平均API响应时间 (< 3秒)
- **错误率**: 每日错误请求比例
- **存储使用**: 数据库和服务器磁盘使用率
- **LLM调用**: 每日API调用次数和费用

#### 日志记录 | Logging
```python
# 简单的日志记录 | Simple logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def divine_with_logging(question: str, language: str):
    logger.info(f"Divine request: {question[:50]}... ({language})")

    try:
        result = destiny_engine.divine(question, language)
        logger.info(f"Divine success: {len(result)} chars")
        return result
    except Exception as e:
        logger.error(f"Divine failed: {str(e)}")
        raise
```

#### 基础告警 | Basic Alerting
- **邮件通知**: 服务宕机时发送邮件
- **日志监控**: 定期检查错误日志
- **手动检查**: 每日人工检查关键指标

---

## 风险评估与应急方案 | Risk Assessment & Contingency Plans

### 常见风险与应对 | Common Risks & Solutions

#### 1. LLM服务中断 | LLM Service Outage
**影响**: 无法生成新卦词
**应对策略**:
- 准备10-20条预设卦词作为备用
- 在界面显示"服务维护中，请稍后再试"
- 监控服务状态，及时切换供应商

#### 2. 服务器故障 | Server Failure
**影响**: 服务完全不可用
**应对策略**:
- 定期备份数据库和代码
- 准备备用服务器，可以快速切换
- 使用监控服务及时发现问题

#### 3. 流量突然增加 | Traffic Spike
**影响**: 响应变慢或服务崩溃
**应对策略**:
- 设置API请求频率限制
- 使用缓存减少服务器负载
- 准备升级服务器配置的方案

### 容量规划 | Capacity Planning

#### 初期容量目标 | Initial Capacity Goals
- **并发用户**: 100-500人同时在线
- **每日请求**: 5,000-10,000次请求
- **存储容量**: 1-5GB数据/月
- **LLM调用**: 500-1,000次/天

#### 扩展计划 | Scaling Plan
- **3个月后**: 如果日活 > 1,000，考虑升级服务器
- **6个月后**: 如果日活 > 5,000，考虑分离前后端
- **1年后**: 如果日活 > 10,000，考虑云服务迁移

---

## 成本控制 | Cost Control

### LLM API成本优化 | LLM API Cost Optimization

#### 基础缓存策略 | Basic Caching Strategy
```python
class DestinyCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get_or_generate(self, question: str, language: str):
        # 生成缓存键
        cache_key = f"destiny:{language}:{hash(question)}"

        # 检查缓存
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return cached_result

        # 调用LLM生成
        result = await llm_provider.generate(question, language)

        # 缓存1小时
        await self.redis.set(cache_key, result, ex=3600)

        return result
```

#### 成本控制措施 | Cost Control Measures
- **缓存时间**: 相同问题1小时内不重复调用
- **每日限额**: 设置每日最大调用次数 (1000次)
- **备用方案**: LLM失败时使用预设回答

### 服务器成本 | Server Cost

#### 经济型云服务器选择 | Budget Cloud Server Options
- **DigitalOcean**: $12/月 (1GB RAM, 1 vCPU)
- **Linode**: $10/月 (1GB RAM, 1 vCPU)
- **Vultr**: $6/月 (1GB RAM, 1 vCPU)

#### 成本估算 | Cost Estimation
- **服务器**: $10-20/月
- **数据库**: $5-10/月 (PostgreSQL)
- **LLM API**: $5-20/月 (视使用量)
- **域名**: $10-15/年
- **总计**: $30-65/月 (初期)

---

## 总结 | Summary

### 简化架构优势 | Simplified Architecture Advantages

#### ✅ 快速启动 | Quick Launch
- 单服务器部署，5分钟内完成
- Docker容器化，一键部署
- 降低技术门槛，专注产品

#### ✅ 成本可控 | Cost Control
- 月成本 $30-65，适合初创项目
- 按需升级，无前期大额投入
- LLM API费用透明可控

#### ✅ 渐进扩展 | Progressive Scaling
- 从单服务器到分离部署
- 业务增长驱动技术升级
- 避免过度设计和资源浪费

#### ✅ 维护简单 | Simple Maintenance
- 基础监控和日志记录
- 手动运维，降低复杂度
- 问题定位和修复快速

### 技术债务考虑 | Technical Debt Considerations

#### 初期重点 | Initial Focus
1. **核心功能完善**: 确保算卦逻辑准确稳定
2. **用户体验优化**: 界面简洁，响应快速
3. **数据积累**: 收集用户行为数据
4. **成本监控**: 跟踪LLM API使用情况

#### 后续关注 | Future Considerations
1. **性能监控**: 用户增长后的性能优化
2. **安全加固**: 数据保护和隐私安全
3. **自动化运维**: 监控和告警自动化
4. **架构升级**: 业务增长后的架构重构

### 实施路线图 | Implementation Roadmap

#### 第1周：基础搭建 | Week 1: Basic Setup
- [ ] 购买云服务器和域名
- [ ] 配置基础环境 (Docker, Nginx)
- [ ] 部署PostgreSQL和Redis

#### 第2周：核心开发 | Week 2: Core Development
- [ ] 开发前端界面 (React)
- [ ] 开发后端API (Node.js)
- [ ] 集成LLM API (OpenAI)

#### 第3周：测试优化 | Week 3: Testing & Optimization
- [ ] 功能测试和BUG修复
- [ ] 性能优化和缓存实现
- [ ] 安全检查和部署上线

#### 第4周：监控运营 | Week 4: Monitoring & Operations
- [ ] 设置基础监控
- [ ] 配置日志记录
- [ ] 开始用户运营

---

*本文档基于产品规划要求制定，将根据实际实施情况和新技术发展进行更新。*

*This document is formulated based on product planning requirements and will be updated according to actual implementation and technological developments.*