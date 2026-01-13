"""
用户交互数据模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserSession(BaseModel):
    """用户会话模型"""
    id: Optional[str] = None
    user_id: str = Field(..., description="用户ID (IP哈希)")
    ip_hash: str = Field(..., description="IP地址哈希")
    first_visit: datetime = Field(default_factory=datetime.now, description="首次访问时间")
    last_visit: datetime = Field(default_factory=datetime.now, description="最后访问时间")
    visit_count: int = Field(default=1, description="访问次数")
    user_agent: Optional[str] = Field(None, description="用户代理")
    language: Optional[str] = Field(None, description="首选语言")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_abc123",
                "ip_hash": "5d41402abc4b2a76b9719d911017c592",
                "first_visit": "2024-01-01T12:00:00",
                "last_visit": "2024-01-01T12:30:00",
                "visit_count": 5,
                "user_agent": "Mozilla/5.0...",
                "language": "zh"
            }
        }


class UserInteraction(BaseModel):
    """用户交互记录模型"""
    id: Optional[str] = None
    user_id: str = Field(..., description="用户ID")
    session_id: Optional[str] = Field(None, description="会话ID")
    question: str = Field(..., description="用户问题")
    question_hash: str = Field(..., description="问题哈希（用于去重）")
    result: str = Field(..., description="算卦结果")
    language: str = Field(..., description="语言")
    category: Optional[str] = Field(None, description="问题类别")
    is_night: bool = Field(default=False, description="是否夜间模式")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    response_time_ms: Optional[int] = Field(None, description="响应时间(毫秒)")
    llm_model: Optional[str] = Field(None, description="使用的LLM模型")
    result_id: Optional[str] = Field(None, description="结果ID（用于分享）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_abc123",
                "session_id": "session_xyz789",
                "question": "我应该辞职吗？",
                "question_hash": "abc123def456",
                "result": "你已经在犹豫中失去了最佳时机",
                "language": "zh",
                "category": "career",
                "is_night": False,
                "timestamp": "2024-01-01T12:00:00",
                "response_time_ms": 1500,
                "llm_model": "gpt-4"
            }
        }


class UserStats(BaseModel):
    """用户统计数据"""
    user_id: str
    total_interactions: int
    first_visit: datetime
    last_visit: datetime
    favorite_language: str
    question_categories: dict
    night_mode_usage: float  # 夜间模式使用比例
    avg_response_time_ms: float
