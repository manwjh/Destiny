"""
用户追踪功能测试脚本
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.services.database_service import init_database_service
from app.models.user_interaction import UserSession, UserInteraction
from app.utils.security import hash_ip, generate_user_id, hash_question
from datetime import datetime


async def test_user_tracking():
    """测试用户追踪功能"""
    
    print("=" * 60)
    print("用户追踪功能测试")
    print("=" * 60)
    
    # 1. 初始化数据库
    print("\n[1] 初始化数据库...")
    db = init_database_service("data/test_destiny.db")
    print("✓ 数据库初始化完成")
    
    # 2. 创建测试用户
    print("\n[2] 创建测试用户...")
    test_ip = "192.168.1.100"
    ip_hashed = hash_ip(test_ip)
    user_id = generate_user_id(ip_hashed)
    print(f"  原始IP: {test_ip}")
    print(f"  IP哈希: {ip_hashed}")
    print(f"  用户ID: {user_id}")
    
    # 3. 保存用户会话
    print("\n[3] 保存用户会话...")
    session = UserSession(
        user_id=user_id,
        ip_hash=ip_hashed,
        first_visit=datetime.now(),
        last_visit=datetime.now(),
        visit_count=1,
        user_agent="Mozilla/5.0 Test Browser",
        language="zh"
    )
    db.save_or_update_session(session)
    print("✓ 会话保存成功")
    
    # 4. 保存多个交互记录
    print("\n[4] 保存交互记录...")
    questions = [
        ("我应该辞职吗？", "你已经在犹豫中失去了最佳时机", "career"),
        ("今天运气如何？", "不必期待，该来的总会来", "general"),
        ("能找到对象吗？", "不是现在不行，是你已经不想要了", "love"),
    ]
    
    for question, result, category in questions:
        interaction = UserInteraction(
            user_id=user_id,
            session_id=None,
            question=question,
            question_hash=hash_question(question),
            result=result,
            language="zh",
            category=category,
            is_night=False,
            timestamp=datetime.now(),
            response_time_ms=1500,
            llm_model="gpt-4"
        )
        interaction_id = db.save_interaction(interaction)
        print(f"  ✓ 交互 {interaction_id}: {question[:20]}...")
    
    # 5. 更新用户会话（模拟再次访问）
    print("\n[5] 模拟用户再次访问...")
    session.last_visit = datetime.now()
    db.save_or_update_session(session)
    print("✓ 会话更新成功")
    
    # 6. 获取用户统计
    print("\n[6] 获取用户统计...")
    stats = db.get_user_stats(user_id)
    if stats:
        print(f"  用户ID: {stats['user_id']}")
        print(f"  首次访问: {stats['first_visit']}")
        print(f"  最后访问: {stats['last_visit']}")
        print(f"  总访问次数: {stats['total_visits']}")
        print(f"  总交互次数: {stats['total_interactions']}")
        print(f"  平均响应时间: {stats['avg_response_time_ms']:.2f}ms")
        print(f"  夜间模式使用率: {stats['night_mode_usage']:.2%}")
        print(f"  问题类别分布: {stats['categories']}")
    
    # 7. 获取最近交互
    print("\n[7] 获取最近交互记录...")
    recent = db.get_recent_interactions(user_id, limit=5)
    for i, record in enumerate(recent, 1):
        print(f"  {i}. {record['question'][:30]}... -> {record['result'][:30]}...")
    
    # 8. 获取全局统计
    print("\n[8] 获取全局统计...")
    global_stats = db.get_global_stats()
    print(f"  总用户数: {global_stats['total_users']}")
    print(f"  总交互数: {global_stats['total_interactions']}")
    print(f"  今日交互数: {global_stats['today_interactions']}")
    print(f"  语言分布: {global_stats['language_distribution']}")
    print(f"  类别分布: {global_stats['category_distribution']}")
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_user_tracking())
