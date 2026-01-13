"""
算卦API路由
"""
import logging
import time
import hashlib
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional

from app.services.database_service import get_database_service
from app.agents.fortune_agent import get_fortune_agent
from app.models.user_interaction import UserSession, UserInteraction
from app.utils.security import get_client_ip, hash_ip, generate_user_id, hash_question

logger = logging.getLogger(__name__)

router = APIRouter()


class DivineRequest(BaseModel):
    """算卦请求"""
    question: str = Field(..., min_length=0, max_length=200, description="用户问题")
    language: Optional[str] = Field('zh', description="语言（zh或en）")
    clientId: Optional[str] = Field(None, description="客户端标识")


class FortuneResult(BaseModel):
    """算卦结果"""
    id: str = Field(..., description="结果ID")
    text: str = Field(..., description="判决文本")
    language: str = Field(..., description="语言")
    timestamp: int = Field(..., description="时间戳")
    shareText: str = Field(..., description="分享文案")
    category: str = Field(default="general", description="类别")


class DivineResponse(BaseModel):
    """算卦响应"""
    success: bool = Field(..., description="是否成功")
    data: Optional[FortuneResult] = Field(None, description="结果数据")
    error: Optional[str] = Field(None, description="错误信息")
    message: Optional[str] = Field(None, description="消息")


@router.post("/divine", response_model=DivineResponse)
async def divine(request: DivineRequest, http_request: Request):
    """
    算卦接口
    
    接收用户问题，返回命运判决
    """
    start_time = time.time()
    
    try:
        # 获取服务实例
        agent = get_fortune_agent()
        db_service = get_database_service()
        
        # 获取用户信息（基于IP）
        client_ip = get_client_ip(http_request)
        ip_hashed = hash_ip(client_ip)
        user_id = generate_user_id(ip_hashed)
        user_agent = http_request.headers.get("User-Agent")
        
        logger.info(f"Request from user: {user_id} (IP hash: {ip_hashed[:8]}...)")
        
        # 处理问题：超长直接截取，不报错
        question = request.question.strip() if request.question else ''
        if len(question) > 200:
            question = question[:200]
        
        # 使用前端传递的语言设置（界面语言决定回复语言）
        # 如果未指定或无效，使用默认值 'zh'
        if not request.language or request.language not in ['zh', 'en']:
            request.language = 'zh'  # 默认中文
        
        # 记录/更新用户会话
        if db_service:
            try:
                session = UserSession(
                    user_id=user_id,
                    ip_hash=ip_hashed,
                    first_visit=datetime.now(),
                    last_visit=datetime.now(),
                    visit_count=1,
                    user_agent=user_agent,
                    language=request.language
                )
                db_service.save_or_update_session(session)
            except Exception as e:
                logger.warning(f"Failed to save session: {e}")
        
        logger.info(f"Generating fortune for question: {question[:50]}... (lang: {request.language})")
        
        # 使用 Agent 生成结果
        agent_result = await agent.execute(
            question=question,
            language=request.language,
            enable_reasoning=False
        )
        result_text = agent_result['result']
        
        # 判断是否夜间模式（用于记录）
        hour = datetime.now().hour
        is_night = hour >= 23 or hour < 3
        
        # 生成结果ID
        result_id = str(uuid.uuid4())[:8]
        
        # 生成分享文案
        share_texts = {
            'zh': "我刚算了一卦，有点不舒服。",
            'en': "I just had my fortune told, and it hit too close to home."
        }
        share_text = share_texts.get(request.language, share_texts['zh'])
        
        # 计算响应时间
        response_time = int((time.time() - start_time) * 1000)
        
        # 记录用户交互
        if db_service:
            try:
                interaction = UserInteraction(
                    user_id=user_id,
                    session_id=None,
                    question=question,
                    question_hash=hash_question(question),
                    result=result_text,
                    language=request.language,
                    category="general",
                    is_night=is_night,
                    timestamp=datetime.now(),
                    response_time_ms=response_time,
                    llm_model="fortune_agent",
                    result_id=result_id
                )
                db_service.save_interaction(interaction)
            except Exception as e:
                logger.warning(f"Failed to save interaction: {e}")
        
        # 构建结果
        fortune_result = FortuneResult(
            id=result_id,
            text=result_text,
            language=request.language,
            timestamp=int(time.time() * 1000),
            shareText=share_text,
            category="general"
        )
        
        logger.info(f"Fortune generated successfully in {response_time}ms for user: {user_id}")
        
        return DivineResponse(
            success=True,
            data=fortune_result
        )
        
    except Exception as e:
        logger.error(f"Divine endpoint error: {str(e)}", exc_info=True)
        error_messages = {
            'zh': '命运之轮暂时卡住了，请稍后再试',
            'en': 'The wheel of destiny is stuck, please try again later'
        }
        error_message = error_messages.get(request.language, error_messages['zh'])
        
        return DivineResponse(
            success=False,
            error="INTERNAL_ERROR",
            message=error_message
        )


@router.get("/share/{share_id}", response_model=DivineResponse)
async def get_shared_result(share_id: str):
    """
    根据分享ID获取算卦结果
    
    Args:
        share_id: 分享ID（8位UUID）
        
    Returns:
        算卦结果数据
    """
    try:
        db_service = get_database_service()
        
        if not db_service:
            logger.warning("Database service not available")
            return DivineResponse(
                success=False,
                error="SERVICE_UNAVAILABLE",
                message="分享服务暂时不可用"
            )
        
        # 查询分享结果
        interaction = db_service.get_interaction_by_result_id(share_id)
        
        if not interaction:
            logger.warning(f"Share ID not found: {share_id}")
            error_messages = {
                'zh': '分享链接已失效或不存在',
                'en': 'Share link has expired or does not exist'
            }
            # 默认返回中文错误信息
            return DivineResponse(
                success=False,
                error="NOT_FOUND",
                message=error_messages.get('zh', 'Share link not found')
            )
        
        # 生成分享文案
        share_texts = {
            'zh': "我刚算了一卦，有点不舒服。",
            'en': "I just had my fortune told, and it hit too close to home."
        }
        language = interaction.get('language', 'zh')
        share_text = share_texts.get(language, share_texts['zh'])
        
        # 处理时间戳
        try:
            if isinstance(interaction['timestamp'], str):
                # SQLite返回的是ISO格式字符串
                timestamp_dt = datetime.fromisoformat(interaction['timestamp'].replace('Z', '+00:00'))
                timestamp_ms = int(timestamp_dt.timestamp() * 1000)
            else:
                timestamp_ms = int(time.time() * 1000)
        except Exception as e:
            logger.warning(f"Error parsing timestamp: {e}, using current time")
            timestamp_ms = int(time.time() * 1000)
        
        # 构建结果
        fortune_result = FortuneResult(
            id=share_id,
            text=interaction['result'],
            language=language,
            timestamp=timestamp_ms,
            shareText=share_text,
            category=interaction.get('category', 'general')
        )
        
        logger.info(f"Retrieved shared result for share_id: {share_id}")
        
        return DivineResponse(
            success=True,
            data=fortune_result
        )
        
    except Exception as e:
        logger.error(f"Get shared result error: {str(e)}", exc_info=True)
        error_messages = {
            'zh': '获取分享结果失败，请稍后再试',
            'en': 'Failed to retrieve shared result, please try again later'
        }
        return DivineResponse(
            success=False,
            error="INTERNAL_ERROR",
            message=error_messages.get('zh', 'Internal error')
        )


@router.get("/test")
async def test_agent():
    """
    测试 Agent 连接
    """
    try:
        agent = get_fortune_agent()
        # 简单测试：空问题
        result = await agent.execute(
            question="",
            language="zh",
            enable_reasoning=False
        )
        return {
            "status": "ok",
            "agent_result": result
        }
    except Exception as e:
        logger.error(f"Agent test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
