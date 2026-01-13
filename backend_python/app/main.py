"""
主应用文件
"""
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 添加父目录到路径以导入版本信息
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))
from __version__ import get_full_version

from app.config.settings import get_settings, validate_settings
from app.services.llm_service import init_llm_service, get_llm_service
from app.services.database_service import init_database_service
from app.agents.fortune_agent import init_fortune_agent
from app.api import divine

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 获取配置
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    logger.info("Starting Destiny API...")
    
    # 验证配置
    try:
        validate_settings(settings)
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    # 初始化数据库服务
    db_path = settings.DATABASE_URL if settings.DATABASE_URL and settings.DATABASE_URL.startswith('sqlite:///') else "data/destiny.db"
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    init_database_service(db_path)
    logger.info(f"Database service initialized: {db_path}")
    
    # 初始化LLM服务
    llm_config = {
        'provider': settings.LLM_PROVIDER,
        'api_key': settings.LLM_API_KEY,
        'base_url': settings.LLM_BASE_URL,
        'model': settings.LLM_MODEL,
        'max_context_tokens': settings.LLM_MAX_CONTEXT_TOKENS,
        'temperature': settings.LLM_TEMPERATURE,
        'max_tokens': settings.LLM_MAX_TOKENS,
        # 向后兼容旧配置
        'default_model': settings.DEFAULT_LLM_MODEL or settings.LLM_MODEL,
        'fallback_model': settings.FALLBACK_LLM_MODEL or settings.LLM_MODEL,
    }
    init_llm_service(llm_config)
    logger.info(f"LLM service initialized with provider: {settings.LLM_PROVIDER}, model: {settings.LLM_MODEL}")
    
    # 初始化 Agent
    llm_service = get_llm_service()
    init_fortune_agent(llm_service)
    logger.info("Fortune Agent initialized successfully")
    
    yield
    
    # 关闭时清理
    logger.info("Shutting down Destiny API...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="算一卦 - 命运判决API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置受信任主机（生产环境）
# 开发环境暂时禁用，避免localhost访问问题
# if not settings.DEBUG:
#     app.add_middleware(
#         TrustedHostMiddleware,
#         allowed_hosts=["destiny.yourdomain.com", "*.yourdomain.com"]
#     )

# 注册路由
app.include_router(divine.router, prefix="/api/v1", tags=["divine"])

# 导入统计路由
from app.api import stats
app.include_router(stats.router, prefix="/api/v1", tags=["stats"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@app.get("/api/v1/version")
async def get_version():
    """获取版本信息"""
    return get_full_version()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
