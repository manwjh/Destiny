"""
统计数据API路由
"""
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.services.database_service import get_database_service
from app.utils.security import get_client_ip, hash_ip, generate_user_id

logger = logging.getLogger(__name__)

router = APIRouter()


class UserStatsResponse(BaseModel):
    """用户统计响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class GlobalStatsResponse(BaseModel):
    """全局统计响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class RecentInteractionsResponse(BaseModel):
    """最近交互记录响应"""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


@router.get("/stats/user", response_model=UserStatsResponse)
async def get_user_stats(request: Request):
    """
    获取当前用户的统计数据
    
    基于IP地址识别用户
    """
    try:
        db_service = get_database_service()
        if not db_service:
            return UserStatsResponse(
                success=False,
                error="Database service not available"
            )
        
        # 获取用户ID
        client_ip = get_client_ip(request)
        ip_hashed = hash_ip(client_ip)
        user_id = generate_user_id(ip_hashed)
        
        # 获取统计数据
        stats = db_service.get_user_stats(user_id)
        
        if not stats:
            return UserStatsResponse(
                success=True,
                data={
                    'user_id': user_id,
                    'message': 'No data available for this user'
                }
            )
        
        return UserStatsResponse(
            success=True,
            data=stats
        )
        
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}", exc_info=True)
        return UserStatsResponse(
            success=False,
            error=str(e)
        )


@router.get("/stats/user/recent", response_model=RecentInteractionsResponse)
async def get_user_recent_interactions(request: Request, limit: int = 10):
    """
    获取当前用户最近的交互记录
    
    Args:
        limit: 返回记录数量（默认10条，最多50条）
    """
    try:
        db_service = get_database_service()
        if not db_service:
            return RecentInteractionsResponse(
                success=False,
                error="Database service not available"
            )
        
        # 限制查询数量
        limit = min(limit, 50)
        
        # 获取用户ID
        client_ip = get_client_ip(request)
        ip_hashed = hash_ip(client_ip)
        user_id = generate_user_id(ip_hashed)
        
        # 获取最近交互
        interactions = db_service.get_recent_interactions(user_id, limit)
        
        return RecentInteractionsResponse(
            success=True,
            data=interactions
        )
        
    except Exception as e:
        logger.error(f"Error getting recent interactions: {str(e)}", exc_info=True)
        return RecentInteractionsResponse(
            success=False,
            error=str(e)
        )


@router.get("/stats/global", response_model=GlobalStatsResponse)
async def get_global_stats():
    """
    获取全局统计数据
    
    返回系统整体使用情况
    """
    try:
        db_service = get_database_service()
        if not db_service:
            return GlobalStatsResponse(
                success=False,
                error="Database service not available"
            )
        
        # 获取全局统计
        stats = db_service.get_global_stats()
        
        return GlobalStatsResponse(
            success=True,
            data=stats
        )
        
    except Exception as e:
        logger.error(f"Error getting global stats: {str(e)}", exc_info=True)
        return GlobalStatsResponse(
            success=False,
            error=str(e)
        )
