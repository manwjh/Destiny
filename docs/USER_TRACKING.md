# 用户交互追踪功能说明

## 概述

《算一卦/Destiny》现在支持基于IP地址的用户交互追踪功能，用于记录和分析用户使用情况。

## 🔐 隐私保护

### IP地址处理
- ✅ **不存储原始IP** - 所有IP地址经过SHA256哈希处理
- ✅ **加盐哈希** - 使用盐值增强安全性
- ✅ **匿名化** - 无法从哈希值反推原始IP
- ✅ **GDPR合规** - 遵循数据保护最佳实践

### 数据存储
```
原始IP: 192.168.1.100
     ↓ (SHA256 + Salt)
IP哈希: 5d41402abc4b2a76
     ↓
用户ID: user_5d41402abc4b2a76
```

## 📊 功能特性

### 1. 用户会话管理

记录每个用户的基本信息：
- 首次访问时间
- 最后访问时间
- 访问次数
- 首选语言
- 浏览器信息（匿名化）

### 2. 交互记录

记录每次算卦交互：
- 用户问题（完整保存）
- 算卦结果
- 语言选择
- 问题类别
- 是否夜间模式
- 响应时间
- 使用的LLM模型

### 3. 统计分析

提供多维度统计：
- 用户个人统计
- 全局使用统计
- 语言分布
- 类别分布
- 夜间模式使用率

## 🔧 技术实现

### 数据库架构

使用 **SQLite** 作为轻量级数据库（可迁移到PostgreSQL）

#### 表结构

**user_sessions** - 用户会话表
```sql
- id (主键)
- user_id (用户ID，唯一)
- ip_hash (IP哈希)
- first_visit (首次访问)
- last_visit (最后访问)
- visit_count (访问次数)
- user_agent (浏览器信息)
- language (首选语言)
```

**user_interactions** - 用户交互表
```sql
- id (主键)
- user_id (用户ID)
- session_id (会话ID)
- question (用户问题)
- question_hash (问题哈希)
- result (算卦结果)
- language (语言)
- category (类别)
- is_night (是否夜间)
- timestamp (时间戳)
- response_time_ms (响应时间)
- llm_model (LLM模型)
```

### 自动化流程

```
用户请求
    ↓
获取IP地址 (支持代理、CDN)
    ↓
哈希处理 (SHA256 + Salt)
    ↓
生成用户ID
    ↓
记录/更新会话
    ↓
处理算卦请求
    ↓
记录交互数据
    ↓
返回结果
```

## 📡 API端点

### 1. 获取用户统计
```bash
GET /api/v1/stats/user
```

返回当前用户（基于IP）的统计数据：
- 总访问次数
- 总交互次数
- 首次/最后访问时间
- 平均响应时间
- 夜间模式使用率
- 问题类别分布

### 2. 获取最近交互
```bash
GET /api/v1/stats/user/recent?limit=10
```

返回当前用户最近的交互记录（最多50条）

### 3. 获取全局统计
```bash
GET /api/v1/stats/global
```

返回系统全局统计：
- 总用户数
- 总交互数
- 今日交互数
- 语言分布
- 类别分布

## 🚀 使用示例

### 前端调用示例

```typescript
// 获取用户统计
const getUserStats = async () => {
  const response = await fetch('/api/v1/stats/user');
  const data = await response.json();
  
  if (data.success) {
    console.log('用户统计:', data.data);
    // {
    //   user_id: "user_5d41402abc4b2a76",
    //   total_visits: 15,
    //   total_interactions: 8,
    //   first_visit: "2024-01-01T12:00:00",
    //   last_visit: "2024-01-13T18:30:00",
    //   avg_response_time_ms: 1500,
    //   night_mode_usage: 0.25,
    //   categories: { career: 3, love: 2, general: 3 }
    // }
  }
};

// 获取最近交互
const getRecentInteractions = async () => {
  const response = await fetch('/api/v1/stats/user/recent?limit=5');
  const data = await response.json();
  
  if (data.success) {
    console.log('最近交互:', data.data);
  }
};

// 获取全局统计
const getGlobalStats = async () => {
  const response = await fetch('/api/v1/stats/global');
  const data = await response.json();
  
  if (data.success) {
    console.log('全局统计:', data.data);
  }
};
```

## 📁 数据存储位置

```
backend_python/
├── data/
│   └── destiny.db          # SQLite数据库文件
└── app/
    ├── models/
    │   └── user_interaction.py
    ├── services/
    │   └── database_service.py
    └── utils/
        └── security.py
```

## 🔍 查询示例

### Python查询示例

```python
from app.services.database_service import get_database_service

db = get_database_service()

# 获取用户统计
user_stats = db.get_user_stats("user_abc123")

# 获取最近交互
recent = db.get_recent_interactions("user_abc123", limit=10)

# 获取全局统计
global_stats = db.get_global_stats()
```

### SQL直接查询

```bash
# 连接数据库
sqlite3 data/destiny.db

# 查看总用户数
SELECT COUNT(*) FROM user_sessions;

# 查看总交互数
SELECT COUNT(*) FROM user_interactions;

# 查看今日交互
SELECT COUNT(*) FROM user_interactions 
WHERE DATE(timestamp) = DATE('now');

# 查看语言分布
SELECT language, COUNT(*) as count 
FROM user_interactions 
GROUP BY language;

# 查看最活跃用户
SELECT user_id, COUNT(*) as interactions 
FROM user_interactions 
GROUP BY user_id 
ORDER BY interactions DESC 
LIMIT 10;
```

## ⚙️ 配置选项

在 `.env` 文件中配置：

```bash
# 数据库路径
DATABASE_URL=sqlite:///data/destiny.db

# IP哈希盐值（建议修改）
IP_HASH_SALT=your_random_salt_here

# 是否启用数据收集（未来功能）
DATA_COLLECTION_ENABLED=true
```

## 🛡️ 安全考虑

### 1. IP地址保护
- ✅ 使用SHA256哈希
- ✅ 添加随机盐值
- ✅ 只存储哈希值，不存储原始IP

### 2. 数据最小化
- ✅ 只收集必要数据
- ✅ User-Agent匿名化
- ✅ 不收集敏感个人信息

### 3. 访问控制
- ✅ 用户只能查看自己的数据
- ✅ 全局统计只显示聚合数据
- ✅ 不暴露其他用户的原始数据

### 4. GDPR合规
- ✅ 数据匿名化
- ✅ 可删除用户数据（未来功能）
- ✅ 数据导出功能（未来功能）

## 📈 未来扩展

### 计划功能
- [ ] 用户数据导出
- [ ] 用户数据删除（GDPR Right to be Forgotten）
- [ ] 更详细的分析报表
- [ ] 问题相似度分析
- [ ] 用户行为预测

### 数据库迁移
当用户量增长时，可以轻松迁移到PostgreSQL：

```python
# 修改配置
DATABASE_URL=postgresql://user:pass@localhost:5432/destiny

# 迁移数据
# 1. 导出SQLite数据
sqlite3 data/destiny.db .dump > destiny_dump.sql

# 2. 转换为PostgreSQL格式
# 3. 导入PostgreSQL
psql -U user -d destiny < destiny_pg.sql
```

## 📝 日志记录

系统会自动记录：
- ✅ 用户会话创建/更新
- ✅ 交互记录保存
- ✅ 数据库操作错误
- ✅ IP地址处理日志

查看日志：
```bash
# 后端日志
tail -f backend_python/logs/destiny.log

# 或在代码中查看
grep "user_" backend_python/logs/destiny.log
```

## 🤝 贡献

如需改进用户追踪功能，请确保：
1. 遵循隐私保护原则
2. 保持数据匿名化
3. 添加适当的测试
4. 更新相关文档

## 📞 技术支持

如有问题，请查看：
- `app/services/database_service.py` - 数据库服务实现
- `app/utils/security.py` - 安全工具函数
- `app/models/user_interaction.py` - 数据模型定义
