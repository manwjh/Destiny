"""
安全工具函数 - IP处理、数据匿名化
"""
import hashlib
import logging
from typing import Optional
from fastapi import Request

logger = logging.getLogger(__name__)


def hash_ip(ip_address: str, salt: str = "destiny_salt_2024") -> str:
    """
    对IP地址进行哈希处理（保护隐私）
    
    Args:
        ip_address: IP地址
        salt: 盐值（应该从环境变量读取）
        
    Returns:
        IP地址的SHA256哈希值
    """
    if not ip_address:
        return "unknown"
    
    # 使用SHA256 + 盐值进行哈希
    hash_input = f"{ip_address}{salt}".encode('utf-8')
    ip_hash = hashlib.sha256(hash_input).hexdigest()[:16]  # 取前16位
    
    return ip_hash


def get_client_ip(request: Request) -> str:
    """
    获取客户端真实IP地址
    支持代理和负载均衡器场景
    
    Args:
        request: FastAPI Request对象
        
    Returns:
        客户端IP地址
    """
    # 优先级顺序检查各种可能的IP头
    # 1. X-Forwarded-For (最常用的代理头)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For 可能包含多个IP，取第一个
        ip = forwarded_for.split(",")[0].strip()
        logger.debug(f"IP from X-Forwarded-For: {ip}")
        return ip
    
    # 2. X-Real-IP (Nginx常用)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        logger.debug(f"IP from X-Real-IP: {real_ip}")
        return real_ip
    
    # 3. CF-Connecting-IP (Cloudflare)
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        logger.debug(f"IP from CF-Connecting-IP: {cf_ip}")
        return cf_ip
    
    # 4. X-Client-IP
    client_ip = request.headers.get("X-Client-IP")
    if client_ip:
        logger.debug(f"IP from X-Client-IP: {client_ip}")
        return client_ip
    
    # 5. 直接连接的IP
    if request.client:
        ip = request.client.host
        logger.debug(f"IP from direct connection: {ip}")
        return ip
    
    logger.warning("Could not determine client IP, using 'unknown'")
    return "unknown"


def anonymize_user_agent(user_agent: Optional[str]) -> Optional[str]:
    """
    匿名化User Agent（移除可能的唯一标识符）
    
    Args:
        user_agent: 原始User Agent字符串
        
    Returns:
        匿名化后的User Agent
    """
    if not user_agent:
        return None
    
    # 只保留浏览器和操作系统信息，移除版本号细节
    # 示例: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) -> Mozilla/5.0 (Macintosh)
    
    # 简单实现：截取前100个字符
    return user_agent[:100] if len(user_agent) > 100 else user_agent


def hash_question(question: str) -> str:
    """
    对问题进行哈希（用于去重和缓存）
    
    Args:
        question: 用户问题
        
    Returns:
        问题的MD5哈希值
    """
    question_normalized = question.strip().lower()
    return hashlib.md5(question_normalized.encode('utf-8')).hexdigest()[:16]


def generate_user_id(ip_hash: str) -> str:
    """
    生成用户ID
    
    Args:
        ip_hash: IP哈希值
        
    Returns:
        用户ID
    """
    return f"user_{ip_hash}"
