# Destiny Backend (Python + LiteLLM)

《算一卦》后端服务 - 使用 FastAPI + LiteLLM

## 技术栈

- **FastAPI**: 现代化的 Python Web 框架
- **LiteLLM**: 统一的 LLM API 接口层
- **Uvicorn**: ASGI 服务器
- **Redis**: 缓存服务
- **PostgreSQL**: 数据库（可选）

## 环境要求

- Python 3.9+
- Redis (可选，用于缓存)
- PostgreSQL (可选，用于数据持久化)

## 安装

### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# 应用配置
DEBUG=true
PORT=8000

# LLM配置
DEFAULT_LLM_MODEL=gpt-4
OPENAI_API_KEY=your_openai_api_key_here

# Redis配置（可选）
REDIS_URL=redis://localhost:6379

# 日志配置
LOG_LEVEL=INFO
```

## 运行

### 开发环境

```bash
# 方式1：使用Python直接运行
python -m app.main

# 方式2：使用uvicorn（支持热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要接口

### POST /api/v1/divine

算卦接口

**请求示例：**

```json
{
  "question": "我应该辞职吗？",
  "language": "zh",
  "clientId": "optional_client_id"
}
```

**响应示例：**

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4",
    "text": "你已经在犹豫中失去了最佳时机",
    "language": "zh",
    "timestamp": 1703123456000,
    "shareText": "我刚算了一卦，有点不舒服。",
    "category": "general"
  }
}
```

## LiteLLM 配置

LiteLLM 支持多个 LLM 提供商：

### OpenAI (默认)

```bash
OPENAI_API_KEY=sk-...
DEFAULT_LLM_MODEL=gpt-4
```

### Anthropic Claude

```bash
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_MODEL=claude-3-sonnet-20240229
```

### Azure OpenAI

```bash
AZURE_API_KEY=your_azure_key
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_API_VERSION=2023-05-15
DEFAULT_LLM_MODEL=azure/gpt-4
```

### 其他支持的提供商

- Google PaLM/Gemini
- Cohere
- Hugging Face
- Replicate
- 更多...

详见 [LiteLLM 文档](https://docs.litellm.ai/docs/)

## 项目结构

```
backend_python/
├── app/
│   ├── api/              # API 路由
│   │   └── divine.py     # 算卦接口
│   ├── config/           # 配置
│   │   └── settings.py   # 应用设置
│   ├── services/         # 业务服务
│   │   ├── llm_service.py    # LLM服务（使用LiteLLM）
│   │   └── prompt_service.py # 提示词服务
│   └── main.py          # 主应用
├── requirements.txt     # Python依赖
└── README.md           # 本文档
```

## 开发指南

### 添加新的 LLM 提供商

LiteLLM 会自动处理不同提供商的API调用。只需配置环境变量即可：

```python
# 在 settings.py 中添加配置
DEFAULT_LLM_MODEL: str = "gpt-4"  # OpenAI
# 或
DEFAULT_LLM_MODEL: str = "claude-3-sonnet-20240229"  # Anthropic
# 或
DEFAULT_LLM_MODEL: str = "azure/gpt-4"  # Azure OpenAI
```

### 自定义提示词模板

编辑 `app/services/prompt_service.py` 中的 `BASE_TEMPLATES`：

```python
BASE_TEMPLATES = {
    'zh': """你的中文提示词模板...""",
    'en': """Your English prompt template..."""
}
```

### 添加夜间模式增强

编辑 `app/services/prompt_service.py` 中的 `NIGHT_ENHANCEMENTS`。

## 测试

### 测试 LLM 连接

```bash
curl http://localhost:8000/api/v1/test
```

### 测试算卦接口

```bash
curl -X POST http://localhost:8000/api/v1/divine \
  -H "Content-Type: application/json" \
  -d '{"question": "我应该辞职吗？", "language": "zh"}'
```

## 部署

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 监控

查看日志：

```bash
tail -f logs/combined.log
```

## 常见问题

### Q: 如何切换 LLM 提供商？

A: 修改环境变量 `DEFAULT_LLM_MODEL` 即可。LiteLLM 会自动识别提供商。

### Q: 如何添加速率限制？

A: 在 `app/main.py` 中添加 FastAPI 的速率限制中间件。

### Q: 如何启用缓存？

A: 配置 `REDIS_URL` 环境变量，系统会自动使用 Redis 缓存结果。

## 许可证

MIT License