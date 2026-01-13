"""
应用配置
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

# 导入版本信息
import sys
from pathlib import Path
# 添加父目录到路径
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))
from __version__ import __version__, get_full_version


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用基本配置
    APP_NAME: str = "Destiny API"
    APP_VERSION: str = __version__
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: Optional[str] = None
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600  # 1小时
    
    # LLM配置
    LLM_PROVIDER: str = "openai"  # openai, anthropic, azure, perfxcloud等
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: Optional[str] = None  # 自定义API端点
    LLM_MODEL: str = "gpt-4"
    LLM_MAX_CONTEXT_TOKENS: int = 128000
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 300
    
    # 旧版配置（保留向后兼容）
    DEFAULT_LLM_MODEL: Optional[str] = None
    FALLBACK_LLM_MODEL: Optional[str] = None
    
    # OpenAI配置
    OPENAI_API_KEY: Optional[str] = None
    
    # Anthropic配置
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Azure OpenAI配置（可选）
    AZURE_API_KEY: Optional[str] = None
    AZURE_API_BASE: Optional[str] = None
    AZURE_API_VERSION: Optional[str] = None
    
    # 速率限制
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # CORS配置
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://destiny.yourdomain.com"
    ]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置（单例模式）"""
    return Settings()


# 验证必需的环境变量
def validate_settings(settings: Settings):
    """验证设置"""
    # 优先检查新版LLM配置
    if settings.LLM_API_KEY:
        if not settings.LLM_MODEL:
            raise ValueError("LLM_MODEL is required when LLM_API_KEY is provided")
        return
    
    # 检查旧版配置
    if not any([
        settings.OPENAI_API_KEY,
        settings.ANTHROPIC_API_KEY,
        settings.AZURE_API_KEY
    ]):
        raise ValueError(
            "At least one LLM API key is required: "
            "LLM_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, or AZURE_API_KEY"
        )
