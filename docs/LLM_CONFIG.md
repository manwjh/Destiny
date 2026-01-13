# LLM 配置说明

## 环境变量配置

本项目支持多种 LLM 服务提供商。配置信息存储在 `.env` 文件中。

### 核心配置参数

```bash
# LLM服务提供商
LLM_PROVIDER=your_provider_name

# API密钥（请替换为你的实际密钥）
LLM_API_KEY=your-api-key-here

# API端点
LLM_BASE_URL=https://api.example.com/v1

# 使用的模型
LLM_MODEL=your-model-name

# 最大上下文tokens
LLM_MAX_CONTEXT_TOKENS=128000

# 生成参数
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=300
```

## 配置文件位置

- **环境变量文件**: `backend_python/.env`
- **配置模块**: `backend_python/app/config/settings.py`
- **LLM服务**: `backend_python/app/services/llm_service.py`

## 使用说明

### 1. 自动加载

应用启动时会自动从 `.env` 文件加载环境变量：

```python
from app.config.settings import get_settings

settings = get_settings()
# 配置会自动从.env文件加载
```

### 2. LLM服务初始化

在 `app/main.py` 中，应用启动时会自动初始化 LLM 服务：

```python
llm_config = {
    'provider': settings.LLM_PROVIDER,
    'api_key': settings.LLM_API_KEY,
    'base_url': settings.LLM_BASE_URL,
    'model': settings.LLM_MODEL,
    'max_context_tokens': settings.LLM_MAX_CONTEXT_TOKENS,
    'temperature': settings.LLM_TEMPERATURE,
    'max_tokens': settings.LLM_MAX_TOKENS,
}
init_llm_service(llm_config)
```

### 3. 调用LLM

在代码中使用LLM服务：

```python
from app.services.llm_service import get_llm_service

llm_service = get_llm_service()
result = await llm_service.generate(prompt, language='zh')
```

## 支持的LLM提供商

- **OpenAI**: 标准OpenAI API
- **Anthropic**: Claude系列模型
- **Azure**: Azure OpenAI服务
- **PerfXCloud**: 自定义端点（当前配置）
- **其他**: 任何兼容OpenAI API格式的服务

## 切换LLM服务商

如需切换到其他LLM服务商，只需修改 `.env` 文件中的相关配置：

### 示例：切换到OpenAI

```bash
LLM_PROVIDER=openai
LLM_API_KEY=your-openai-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
LLM_MAX_CONTEXT_TOKENS=128000
```

### 示例：切换到Anthropic

```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=your-anthropic-api-key
LLM_BASE_URL=https://api.anthropic.com/v1
LLM_MODEL=claude-3-opus-20240229
LLM_MAX_CONTEXT_TOKENS=200000
```

## 注意事项

1. **安全性**: `.env` 文件包含敏感信息（API密钥），已添加到 `.gitignore`，不会被提交到版本控制
2. **示例文件**: `.env.example` 提供了配置模板，可用于参考和部署
3. **兼容性**: 代码使用 LiteLLM 库，支持多种LLM提供商的统一接口
4. **环境变量**: 应用启动时会将 `LLM_API_KEY` 和 `LLM_BASE_URL` 设置为环境变量，供 LiteLLM 使用

## 验证配置

启动应用后，查看日志确认配置是否正确加载：

```bash
cd backend_python
python -m app.main
```

应该看到类似的日志：

```
INFO - LLM API key configured for provider: your_provider
INFO - LLM base URL configured: https://api.example.com/v1
INFO - LLM service initialized with provider: your_provider, model: your-model-name
```

## 故障排除

### 问题1: API密钥未生效

确保 `.env` 文件在 `backend_python/` 目录下，且格式正确（没有多余空格）。

### 问题2: 模型调用失败

检查：
- API密钥是否正确
- Base URL 是否可访问
- 模型名称是否正确
- 网络连接是否正常

### 问题3: 环境变量未加载

确保安装了 `python-dotenv` 和 `pydantic-settings`：

```bash
pip install python-dotenv pydantic-settings
```
