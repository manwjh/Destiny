# 🚀 快速启动指南 | Quick Start Guide

## 概述 | Overview

本指南提供两个自动化脚本，帮助你快速启动《算一卦/Destiny》系统：

1. **`quick_start.sh`** - 本地开发环境一键启动
2. **`docker_quick_start.sh`** - Docker容器化一键启动

---

## 方式 1: 本地开发环境启动

### 使用 `quick_start.sh` 脚本

```bash
# 进入项目目录
cd Destiny

# 运行快速启动脚本
./quick_start.sh
```

### 脚本功能说明

#### 步骤 1: 环境检查
- ✅ 检查 Python 3.9+ 是否安装
- ✅ 检查 Node.js 18+ 是否安装
- ✅ 检查 npm 是否可用
- ⚠️ 检查 Docker（可选）
- ⚠️ 检查 Docker Compose（可选）

#### 步骤 2: Python 虚拟环境
- 自动创建 `venv` 虚拟环境
- 升级 pip 到最新版本
- 激活虚拟环境

#### 步骤 3: 安装后端依赖
- 在虚拟环境中安装所有 Python 依赖
- 安装 FastAPI、LiteLLM、Uvicorn 等

#### 步骤 4: 安装前端依赖
- 检查 `node_modules` 是否存在
- 运行 `npm install` 安装所有依赖

#### 步骤 5: 配置环境变量
- 检查 `backend_python/.env` 文件
- 如不存在，自动创建默认配置文件
- 提示用户配置 LLM API Key
- 可选择立即编辑 .env 文件

#### 步骤 6: 检查 Redis（可选）
- 检查 Redis 是否安装
- 如已安装但未运行，尝试启动
- 如未安装，提供安装指引

#### 步骤 7: 检查 PostgreSQL（可选）
- 检查 PostgreSQL 是否安装
- 检查数据库是否运行
- 自动创建 `destiny` 数据库

#### 步骤 8: 构建前端（跳过）
- 开发环境跳过此步骤
- 生产环境会构建前端资源

#### 步骤 9: 启动后端服务
- 检查端口 8000 是否被占用
- 在后台启动 FastAPI 服务
- 等待服务健康检查通过
- 记录进程 PID 到 `backend.pid`

#### 步骤 10: 启动前端服务
- 检查端口 5173 是否被占用
- 在后台启动 Vite 开发服务器
- 等待服务启动
- 记录进程 PID 到 `frontend.pid`

#### 步骤 11: 系统测试
- 测试后端健康检查接口
- 测试算卦 API 接口
- 验证服务正常运行

### 启动后的信息

脚本成功后会显示：

```
╔═══════════════════════════════════════════════════════════╗
║                  服务已成功启动！                          ║
║                Service Started Successfully!              ║
╚═══════════════════════════════════════════════════════════╝

📍 访问地址 | Access URLs:
   
   前端 Frontend:     http://localhost:5173
   后端 Backend:      http://localhost:8000
   API文档 API Docs:  http://localhost:8000/docs
   健康检查 Health:    http://localhost:8000/health

📝 日志文件 | Log Files:
   后端日志: ./backend.log
   前端日志: ./frontend.log

🛠️  管理命令 | Management Commands:
   查看后端日志: tail -f backend.log
   查看前端日志: tail -f frontend.log
   停止服务: ./stop.sh
   重启服务: ./quick_start.sh
```

### 停止服务

脚本会自动创建 `stop.sh`：

```bash
# 停止所有服务
./stop.sh
```

`stop.sh` 会：
- 读取 PID 文件
- 终止后端和前端进程
- 清理 PID 文件
- 额外清理可能残留的进程

---

## 方式 2: Docker 容器化启动

### 使用 `docker_quick_start.sh` 脚本

```bash
# 进入项目目录
cd Destiny

# 运行 Docker 快速启动
./docker_quick_start.sh
```

### 脚本功能说明

#### 步骤 1: 检查 Docker 环境
- 检查 Docker 是否安装并运行
- 检查 Docker Compose 版本（V1 或 V2）
- 如环境不符合要求，提供安装指引

#### 步骤 2: 配置环境变量
- 检查或创建 `backend_python/.env`
- 配置数据库和 Redis 连接（使用容器内地址）
- 提示配置 LLM API Key

#### 步骤 3: 启动 Docker 服务
- 停止现有容器
- 拉取/构建镜像
- 启动所有服务：
  - PostgreSQL
  - Redis
  - Backend (FastAPI)
  - Frontend (Nginx)

#### 步骤 4: 等待服务就绪
- 等待后端服务健康检查通过（最多 60 秒）
- 等待前端服务可访问（最多 40 秒）

#### 步骤 5: 测试服务
- 测试算卦 API 接口
- 验证容器间通信

### 启动后的信息

```
╔═══════════════════════════════════════════════════════════╗
║              Docker 服务已成功启动！                       ║
║           Docker Services Started Successfully!           ║
╚═══════════════════════════════════════════════════════════╝

📍 访问地址 | Access URLs:
   
   前端 Frontend:     http://localhost
   后端 Backend:      http://localhost:8000
   API文档 API Docs:  http://localhost:8000/docs
   Redis:             localhost:6379
   PostgreSQL:        localhost:5432

🐳 Docker 命令 | Docker Commands:
   查看日志: docker compose logs -f
   停止服务: docker compose down
   重启服务: docker compose restart
   查看状态: docker compose ps

🛠️  管理命令 | Management:
   查看后端日志: docker compose logs -f backend
   查看前端日志: docker compose logs -f frontend
   进入容器: docker compose exec backend bash
```

### 停止 Docker 服务

```bash
# 停止所有容器
docker compose down

# 停止并删除数据卷（⚠️ 会删除数据库数据）
docker compose down -v
```

---

## 环境变量配置

### 必需配置

在 `backend_python/.env` 中，必须配置：

```bash
# LLM 提供商
LLM_PROVIDER=openai

# LLM 模型
LLM_MODEL=gpt-4

# LLM API Key（必需！）
LLM_API_KEY=sk-your-actual-api-key-here
```

### 可选配置

```bash
# 数据库
DATABASE_URL=postgresql://destiny:destiny@localhost:5432/destiny

# Redis
REDIS_URL=redis://localhost:6379

# 日志级别
LOG_LEVEL=INFO

# 速率限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 获取 API Key

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/account/keys
- **Google**: https://makersuite.google.com/app/apikey
- **Azure**: https://portal.azure.com/
- **Cohere**: https://dashboard.cohere.com/api-keys

---

## 故障排查

### 问题 1: 端口被占用

```bash
# 查看端口占用
lsof -i :5173  # 前端
lsof -i :8000  # 后端
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# 终止占用进程
lsof -ti:8000 | xargs kill -9
```

### 问题 2: Python 版本不符合

```bash
# macOS 使用 Homebrew 安装
brew install python@3.11

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11

# 验证版本
python3 --version
```

### 问题 3: Node.js 版本不符合

```bash
# 使用 nvm 安装（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# 或使用 Homebrew (macOS)
brew install node@20

# 验证版本
node --version
```

### 问题 4: Docker 未运行

```bash
# macOS: 启动 Docker Desktop
open -a Docker

# Linux: 启动 Docker 服务
sudo systemctl start docker

# 验证 Docker
docker info
```

### 问题 5: 服务启动失败

```bash
# 查看日志
tail -f backend.log
tail -f frontend.log

# 或使用 Docker
docker compose logs backend
docker compose logs frontend

# 检查环境变量
cat backend_python/.env

# 手动测试后端
cd backend_python
source ../venv/bin/activate
uvicorn app.main:app --reload
```

### 问题 6: API 调用失败

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试算卦 API
curl -X POST http://localhost:8000/api/v1/divine \
  -H "Content-Type: application/json" \
  -d '{"question":"测试","language":"zh"}'

# 检查 API Key
grep LLM_API_KEY backend_python/.env

# 查看详细日志
tail -f backend.log | grep -i error
```

---

## 开发建议

### 本地开发环境

推荐使用 `quick_start.sh`：
- ✅ 可以直接修改代码并热重载
- ✅ 日志输出更直观
- ✅ 调试更方便
- ✅ 占用资源更少

### 生产环境部署

推荐使用 `docker_quick_start.sh`：
- ✅ 环境一致性
- ✅ 易于扩展
- ✅ 易于维护
- ✅ 包含完整依赖

### 混合使用

你也可以：
1. 使用 Docker 运行数据库和 Redis
2. 本地运行前后端进行开发

```bash
# 只启动数据库服务
docker compose up -d db redis

# 本地启动应用
./quick_start.sh
```

---

## 常用命令速查

### 本地开发

```bash
# 启动服务
./quick_start.sh

# 停止服务
./stop.sh

# 查看日志
tail -f backend.log
tail -f frontend.log

# 重启后端
pkill -f uvicorn
cd backend_python && source ../venv/bin/activate && uvicorn app.main:app &

# 重启前端
pkill -f vite
cd frontend && npm run dev &
```

### Docker 部署

```bash
# 启动服务
./docker_quick_start.sh

# 停止服务
docker compose down

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启单个服务
docker compose restart backend

# 进入容器
docker compose exec backend bash

# 清理所有数据
docker compose down -v
```

---

## 下一步

启动成功后，你可以：

1. 📖 查看 [产品规划](./product-planning.md)
2. 🏗️ 了解 [系统架构](./system-architecture.md)
3. 🎨 研究 [用户体验设计](./user-experience.md)
4. 🐍 阅读 [后端文档](../backend_python/README.md)
5. 🧪 进行系统测试和开发

---

## 反馈与支持

如遇到问题：
1. 查看本文档的故障排查章节
2. 检查日志文件
3. 查看项目 Issues
4. 提交新的 Issue

**祝你好运！Good Luck!** 🚀
