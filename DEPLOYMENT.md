# 《算一卦/Destiny》部署文档
# Destiny Deployment Documentation

## 📋 部署摘要 | Deployment Summary

✅ **数据库部署已完成！** | **Database Deployment Completed!**

---

## 🎯 当前状态 | Current Status

### 已完成的服务 | Completed Services

#### 1. PostgreSQL 数据库 | PostgreSQL Database
- **容器名称**: `destiny-db-1`
- **端口映射**: `localhost:5432 -> 5432`
- **状态**: ✅ 运行中 | Running
- **数据库名**: `destiny`
- **用户名**: `destiny`
- **密码**: `destiny`

**已创建的表 | Created Tables:**
- ✅ `user_sessions` - 用户会话表（存储算卦记录）
- ✅ `prompt_templates` - 提示词模板表（存储LLM提示词）
- ✅ `daily_stats` - 统计视图（每日请求统计）

**已创建的索引 | Created Indexes:**
- ✅ 按时间索引
- ✅ 按用户索引
- ✅ 按语言索引
- ✅ 按模板类型索引

**默认数据 | Default Data:**
- ✅ 4个提示词模板（中文base + night，英文base + night）

#### 2. Redis 缓存 | Redis Cache
- **容器名称**: `destiny-redis-1`
- **端口映射**: `localhost:6379 -> 6379`
- **状态**: ✅ 运行中 | Running
- **版本**: Redis 7.4.5

---

## 🚀 下一步操作 | Next Steps

### 1. 配置环境变量 | Configure Environment Variables

创建 `.env` 文件在项目根目录：

```bash
# 数据库配置
DATABASE_URL=postgresql://destiny:destiny@localhost:5432/destiny
REDIS_URL=redis://localhost:6379

# LLM API密钥（必需）
OPENAI_API_KEY=your_openai_api_key_here

# 可选
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 2. 启动后端服务 | Start Backend Service

```bash
# 方式1：使用Docker Compose（推荐）
docker-compose up -d backend

# 方式2：本地开发
cd backend_python
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端服务 | Start Frontend Service

```bash
# 使用Docker Compose
docker-compose up -d frontend

# 或本地开发
cd frontend
npm install
npm start
```

### 4. 验证部署 | Verify Deployment

```bash
# 检查所有服务状态
docker-compose ps

# 测试后端健康检查
curl http://localhost:8000/health

# 测试前端
curl http://localhost:80
```

---

## 🔍 数据库管理 | Database Management

### 连接数据库 | Connect to Database

```bash
# 使用psql连接
docker exec -it destiny-db-1 psql -U destiny -d destiny

# 使用其他工具连接
# Host: localhost
# Port: 5432
# Database: destiny
# Username: destiny
# Password: destiny
```

### 常用SQL命令 | Common SQL Commands

```sql
-- 查看所有表
\dt

-- 查看表结构
\d user_sessions
\d prompt_templates

-- 查看提示词模板
SELECT name, language, template_type FROM prompt_templates;

-- 查看用户会话（如果有数据）
SELECT * FROM user_sessions ORDER BY timestamp DESC LIMIT 10;

-- 查看每日统计
SELECT * FROM daily_stats;
```

### Redis管理 | Redis Management

```bash
# 连接Redis
docker exec -it destiny-redis-1 redis-cli

# Redis命令
PING                    # 测试连接
KEYS *                  # 查看所有键
GET key_name            # 获取值
FLUSHALL                # 清空所有数据（慎用！）
```

---

## 📊 数据库架构 | Database Schema

### user_sessions 表结构 | Table Structure

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| client_id | VARCHAR(255) | 匿名用户标识 |
| question | TEXT | 用户问题 |
| language | VARCHAR(2) | 语言（zh/en） |
| result | TEXT | 算卦结果 |
| timestamp | TIMESTAMP | 时间戳 |
| user_agent | TEXT | 浏览器信息 |
| ip_hash | VARCHAR(64) | IP哈希（隐私保护） |
| response_time | INTEGER | 响应时间（毫秒） |

### prompt_templates 表结构 | Table Structure

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| name | VARCHAR(100) | 模板名称 |
| language | VARCHAR(2) | 语言（zh/en） |
| template_type | VARCHAR(50) | 类型（base/night/special） |
| template_content | TEXT | 模板内容 |
| version | INTEGER | 版本号 |
| is_active | BOOLEAN | 是否激活 |
| created_at | TIMESTAMP | 创建时间 |

---

## 🛠️ 维护命令 | Maintenance Commands

### 启动/停止服务 | Start/Stop Services

```bash
# 启动所有服务
docker-compose up -d

# 启动特定服务
docker-compose up -d db redis

# 停止所有服务
docker-compose down

# 停止并删除数据卷（注意：会删除数据！）
docker-compose down -v
```

### 查看日志 | View Logs

```bash
# 查看数据库日志
docker logs destiny-db-1

# 查看Redis日志
docker logs destiny-redis-1

# 实时查看日志
docker logs -f destiny-db-1
```

### 备份数据 | Backup Data

```bash
# 备份PostgreSQL数据库
docker exec destiny-db-1 pg_dump -U destiny destiny > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i destiny-db-1 psql -U destiny destiny < backup_20260113.sql
```

---

## 🔒 安全注意事项 | Security Notes

⚠️ **生产环境部署时请注意：** | **For Production Deployment:**

1. **修改默认密码**
   - 修改数据库密码（当前：destiny/destiny）
   - 为Redis添加密码保护
   
2. **环境变量安全**
   - 不要将 `.env` 文件提交到git
   - 使用强密码和随机生成的密钥
   
3. **网络安全**
   - 不要将数据库端口暴露到公网
   - 使用防火墙限制访问
   
4. **数据备份**
   - 定期备份数据库
   - 测试恢复流程

---

## 📈 监控和性能 | Monitoring & Performance

### 数据库性能监控 | Database Performance

```sql
-- 查看活动连接
SELECT count(*) FROM pg_stat_activity;

-- 查看慢查询
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 查看表大小
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

### Redis监控 | Redis Monitoring

```bash
# 查看Redis信息
docker exec destiny-redis-1 redis-cli INFO

# 查看内存使用
docker exec destiny-redis-1 redis-cli INFO memory

# 查看统计信息
docker exec destiny-redis-1 redis-cli INFO stats
```

---

## 🐛 故障排查 | Troubleshooting

### 常见问题 | Common Issues

#### 1. 数据库连接失败
```bash
# 检查容器是否运行
docker ps | grep destiny

# 检查数据库日志
docker logs destiny-db-1

# 测试连接
docker exec destiny-db-1 pg_isready -U destiny
```

#### 2. Redis连接失败
```bash
# 测试Redis
docker exec destiny-redis-1 redis-cli ping

# 检查Redis日志
docker logs destiny-redis-1
```

#### 3. 端口冲突
```bash
# 查看端口占用
lsof -i :5432
lsof -i :6379

# 修改docker-compose.yml中的端口映射
```

---

## 📞 支持 | Support

如有问题，请查看：
- 项目文档：`/docs/README.md`
- 系统架构：`/docs/system-architecture.md`
- 产品规划：`/docs/product-planning.md`

---

**部署完成时间**: 2026-01-13  
**文档版本**: 1.0  
**最后更新**: 2026-01-13

✅ 数据库部署成功！准备启动应用服务。  
✅ Database deployed successfully! Ready to start application services.
