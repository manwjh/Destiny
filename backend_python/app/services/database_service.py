"""
数据库服务 - 处理用户交互数据的存储和查询
使用 SQLite 作为轻量级数据库（可以轻松迁移到 PostgreSQL）
"""
import sqlite3
import logging
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from app.models.user_interaction import UserSession, UserInteraction, UserStats

logger = logging.getLogger(__name__)


class DatabaseService:
    """数据库服务类"""
    
    def __init__(self, db_path: str = "data/destiny.db"):
        """
        初始化数据库服务
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        
        # 确保数据目录存在
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        logger.info(f"Database service initialized: {db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典格式
        return conn
    
    def _init_database(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 创建用户会话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL UNIQUE,
                    ip_hash TEXT NOT NULL,
                    first_visit TEXT NOT NULL,
                    last_visit TEXT NOT NULL,
                    visit_count INTEGER DEFAULT 1,
                    user_agent TEXT,
                    language TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建用户交互表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT,
                    question TEXT NOT NULL,
                    question_hash TEXT NOT NULL,
                    result TEXT NOT NULL,
                    language TEXT NOT NULL,
                    category TEXT,
                    is_night INTEGER DEFAULT 0,
                    timestamp TEXT NOT NULL,
                    response_time_ms INTEGER,
                    llm_model TEXT,
                    result_id TEXT UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_sessions(user_id)
                )
            """)
            
            # 如果表已存在，添加 result_id 字段（用于分享功能）
            result_id_exists = False
            column_just_added = False
            try:
                cursor.execute("ALTER TABLE user_interactions ADD COLUMN result_id TEXT")
                logger.info("Added result_id column to user_interactions table")
                result_id_exists = True
                column_just_added = True
            except sqlite3.OperationalError as e:
                # 检查是否因为列已存在而失败
                error_msg = str(e).lower()
                if "duplicate column name" in error_msg or "already exists" in error_msg:
                    result_id_exists = True
                    logger.debug("result_id column already exists")
                else:
                    # 其他错误，检查列是否存在
                    cursor.execute("PRAGMA table_info(user_interactions)")
                    columns = [row[1] for row in cursor.fetchall()]
                    result_id_exists = "result_id" in columns
                    if result_id_exists:
                        logger.debug("result_id column exists (verified via PRAGMA)")
            
            # 创建索引
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id 
                ON user_sessions(user_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_interactions_user_id 
                ON user_interactions(user_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_interactions_timestamp 
                ON user_interactions(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_interactions_question_hash 
                ON user_interactions(question_hash)
            """)
            
            # 只有在 result_id 列存在时才创建索引
            if result_id_exists:
                try:
                    # 如果列是刚添加的，创建唯一索引以保持数据完整性
                    if column_just_added:
                        cursor.execute("""
                            CREATE UNIQUE INDEX IF NOT EXISTS idx_interactions_result_id 
                            ON user_interactions(result_id)
                        """)
                        logger.info("Created unique index on result_id column")
                    else:
                        cursor.execute("""
                            CREATE INDEX IF NOT EXISTS idx_interactions_result_id 
                            ON user_interactions(result_id)
                        """)
                except sqlite3.OperationalError as e:
                    logger.warning(f"Failed to create index on result_id: {e}")
            else:
                logger.warning("result_id column does not exist, skipping index creation")
            
            conn.commit()
            logger.info("Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def save_or_update_session(self, session: UserSession) -> str:
        """
        保存或更新用户会话
        
        Args:
            session: 用户会话对象
            
        Returns:
            用户ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 检查会话是否存在
            cursor.execute(
                "SELECT id, visit_count FROM user_sessions WHERE user_id = ?",
                (session.user_id,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # 更新现有会话
                cursor.execute("""
                    UPDATE user_sessions 
                    SET last_visit = ?,
                        visit_count = visit_count + 1,
                        user_agent = ?,
                        language = ?,
                        updated_at = ?
                    WHERE user_id = ?
                """, (
                    session.last_visit.isoformat(),
                    session.user_agent,
                    session.language,
                    datetime.now().isoformat(),
                    session.user_id
                ))
                logger.debug(f"Updated session for user: {session.user_id}")
            else:
                # 创建新会话
                cursor.execute("""
                    INSERT INTO user_sessions 
                    (user_id, ip_hash, first_visit, last_visit, visit_count, user_agent, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.user_id,
                    session.ip_hash,
                    session.first_visit.isoformat(),
                    session.last_visit.isoformat(),
                    session.visit_count,
                    session.user_agent,
                    session.language
                ))
                logger.info(f"Created new session for user: {session.user_id}")
            
            conn.commit()
            return session.user_id
            
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def save_interaction(self, interaction: UserInteraction) -> int:
        """
        保存用户交互记录
        
        Args:
            interaction: 用户交互对象
            
        Returns:
            交互记录ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO user_interactions 
                (user_id, session_id, question, question_hash, result, language, 
                 category, is_night, timestamp, response_time_ms, llm_model, result_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                interaction.user_id,
                interaction.session_id,
                interaction.question,
                interaction.question_hash,
                interaction.result,
                interaction.language,
                interaction.category,
                1 if interaction.is_night else 0,
                interaction.timestamp.isoformat(),
                interaction.response_time_ms,
                interaction.llm_model,
                getattr(interaction, 'result_id', None)
            ))
            
            conn.commit()
            interaction_id = cursor.lastrowid
            logger.info(f"Saved interaction {interaction_id} for user: {interaction.user_id}")
            return interaction_id
            
        except Exception as e:
            logger.error(f"Error saving interaction: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            统计数据字典
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 获取基础会话信息
            cursor.execute("""
                SELECT first_visit, last_visit, visit_count, language
                FROM user_sessions 
                WHERE user_id = ?
            """, (user_id,))
            session = cursor.fetchone()
            
            if not session:
                return None
            
            # 获取交互统计
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_interactions,
                    AVG(response_time_ms) as avg_response_time,
                    SUM(CASE WHEN is_night = 1 THEN 1 ELSE 0 END) as night_interactions,
                    language,
                    category
                FROM user_interactions 
                WHERE user_id = ?
                GROUP BY language, category
            """, (user_id,))
            interactions = cursor.fetchall()
            
            # 构建统计数据
            stats = {
                'user_id': user_id,
                'first_visit': session['first_visit'],
                'last_visit': session['last_visit'],
                'total_visits': session['visit_count'],
                'total_interactions': sum(row['total_interactions'] for row in interactions),
                'favorite_language': session['language'],
                'avg_response_time_ms': 0,
                'night_mode_usage': 0,
                'categories': {}
            }
            
            # 计算详细统计
            total_interactions = stats['total_interactions']
            if total_interactions > 0:
                total_response_time = sum(
                    row['total_interactions'] * (row['avg_response_time'] or 0) 
                    for row in interactions
                )
                stats['avg_response_time_ms'] = total_response_time / total_interactions
                
                night_total = sum(row['night_interactions'] for row in interactions)
                stats['night_mode_usage'] = night_total / total_interactions
                
                # 统计各类别的交互数量
                for row in interactions:
                    category = row['category'] or 'general'
                    if category not in stats['categories']:
                        stats['categories'][category] = 0
                    stats['categories'][category] += row['total_interactions']
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return None
        finally:
            conn.close()
    
    def get_recent_interactions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取用户最近的交互记录
        
        Args:
            user_id: 用户ID
            limit: 返回记录数量
            
        Returns:
            交互记录列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, question, result, language, category, 
                       is_night, timestamp, response_time_ms
                FROM user_interactions 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting recent interactions: {e}")
            return []
        finally:
            conn.close()
    
    def get_global_stats(self) -> Dict[str, Any]:
        """
        获取全局统计数据
        
        Returns:
            全局统计数据
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # 用户总数
            cursor.execute("SELECT COUNT(*) as total_users FROM user_sessions")
            total_users = cursor.fetchone()['total_users']
            
            # 交互总数
            cursor.execute("SELECT COUNT(*) as total_interactions FROM user_interactions")
            total_interactions = cursor.fetchone()['total_interactions']
            
            # 今日交互数
            cursor.execute("""
                SELECT COUNT(*) as today_interactions 
                FROM user_interactions 
                WHERE DATE(timestamp) = DATE('now')
            """)
            today_interactions = cursor.fetchone()['today_interactions']
            
            # 各语言使用统计
            cursor.execute("""
                SELECT language, COUNT(*) as count 
                FROM user_interactions 
                GROUP BY language
            """)
            language_stats = {row['language']: row['count'] for row in cursor.fetchall()}
            
            # 各类别统计
            cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM user_interactions 
                GROUP BY category
            """)
            category_stats = {row['category']: row['count'] for row in cursor.fetchall()}
            
            return {
                'total_users': total_users,
                'total_interactions': total_interactions,
                'today_interactions': today_interactions,
                'language_distribution': language_stats,
                'category_distribution': category_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting global stats: {e}")
            return {}
        finally:
            conn.close()
    
    def get_interaction_by_result_id(self, result_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 result_id 获取交互记录（用于分享功能）
        
        Args:
            result_id: 结果ID
            
        Returns:
            交互记录字典，如果不存在则返回 None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, user_id, question, result, language, category, 
                       is_night, timestamp, result_id
                FROM user_interactions 
                WHERE result_id = ?
            """, (result_id,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Error getting interaction by result_id: {e}")
            return None
        finally:
            conn.close()


# 全局数据库服务实例
_db_service: Optional[DatabaseService] = None


def init_database_service(db_path: str = "data/destiny.db") -> DatabaseService:
    """初始化数据库服务"""
    global _db_service
    _db_service = DatabaseService(db_path)
    return _db_service


def get_database_service() -> Optional[DatabaseService]:
    """获取数据库服务实例"""
    return _db_service
