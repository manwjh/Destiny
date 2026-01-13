# 《算一卦/Destiny》 | Calculate a Fortune/Destiny

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

一个好玩的算命软件 - 不安慰你，只给结果的算卦器
*A fun fortune-telling software - An oracle that doesn't comfort you, just gives results*
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/295ca87d-59f9-4ad6-abf7-5ba2c1eb91eb" />

ooh shit!!

**当前版本 | Current Version: v0.1.0** | [📋 更新日志 | Changelog](./CHANGELOG.md)

## 🏗️ 技术架构 | Tech Stack

### 前端 | Frontend
- **React 18 + TypeScript**
- **Tailwind CSS** - 原子化CSS框架
- **Vite** - 现代化构建工具
- **Framer Motion** - 动画库

### 后端 | Backend
- **FastAPI** - 现代化Python Web框架
- **LiteLLM** - 统一LLM API接入层，支持多个提供商
- **Uvicorn** - ASGI服务器
- **Redis** - 缓存服务
- **PostgreSQL** - 数据库

### LLM支持 | LLM Providers (via LiteLLM)
- ✅ **OpenAI** (GPT-4, GPT-3.5)
- ✅ **Anthropic** (Claude-3)
- ✅ **Azure OpenAI**
- ✅ **Google PaLM/Gemini**
- ✅ **Cohere**
- ✅ **Hugging Face**
- 更多...

## 🚀 快速开始 | Quick Start

### 环境要求 | Requirements
- Python 3.9+
- Node.js 18+
- Redis (可选) | Optional
- Docker & Docker Compose (推荐) | Recommended

### ⚡ 一键启动（推荐）| One-Click Start (Recommended)

#### 方式 1: 本地开发环境

```bash
# 克隆项目 | Clone project
git clone https://github.com/manwjh/Destiny.git
cd Destiny

# 一键启动所有服务 | Start all services with one command
./quick_start.sh

# 停止服务 | Stop services
./stop.sh
```

**脚本会自动完成以下操作：**
- ✅ 检查环境依赖（Python, Node.js, Redis, PostgreSQL）
- ✅ 创建虚拟环境并安装所有依赖
- ✅ 配置环境变量（会提示你添加 API Key）
- ✅ 启动后端服务（FastAPI + LiteLLM）
- ✅ 启动前端服务（React + Vite）
- ✅ 运行系统测试验证

#### 方式 2: Docker 容器化部署

```bash
# 克隆项目 | Clone project
git clone https://github.com/manwjh/Destiny.git
cd Destiny

# 使用 Docker 一键启动 | Start with Docker
./docker_quick_start.sh

# 停止服务 | Stop services
docker compose down
```

**Docker 方式的优势：**
- ✅ 无需手动安装依赖
- ✅ 环境完全隔离
- ✅ 包含数据库和缓存服务
- ✅ 一键部署到生产环境

### 手动安装 | Manual Installation

#### 1. 后端安装 | Backend Setup

```bash
cd backend_python

# 创建虚拟环境 | Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 | or
venv\Scripts\activate     # Windows

# 安装依赖 | Install dependencies
pip install -r requirements.txt

# 配置环境变量 | Configure environment
# 创建 .env 文件，参考 .env.example

# 启动服务 | Start server
uvicorn app.main:app --reload
```

#### 2. 前端安装 | Frontend Setup

```bash
cd frontend

# 安装依赖 | Install dependencies
npm install

# 启动开发服务器 | Start dev server
npm run dev
```

## 📚 重要文档 | Key Documentation

- **[📋 产品规划书](docs/product-planning.md)** - 完整的项目规划和执行蓝图
- **[🏗️ 系统架构](docs/system-architecture.md)** - 详细的系统架构设计
- **[🎨 用户体验](docs/user-experience.md)** - 完整的用户交互流程
- **[📝 更新日志](CHANGELOG.md)** - 版本更新历史和变更记录
- **[🎯 Cursor 规则](.cursorrules)** - Cursor IDE 专用开发规范
- **[🐍 后端文档](backend_python/README.md)** - Python后端详细文档
- **[📖 文档索引](docs/README.md)** - 完整文档目录

## 🎯 核心理念 | Core Philosophy

- **不解释** | No explanations
- **不负责** | No responsibility
- **不温柔** | Not gentle
- **但"像真话"** | But "feels real"

*"不是现在不行，是你已经不想要了"* - 《算一卦》

## ✨ 核心功能 | Core Features

### 前端功能 | Frontend Features
- ✅ **算卦功能** - 基于LLM的智能命运判决
- ✅ **多语言支持** - 简体中文、繁体中文、English
- ✅ **用户统计** - 个人使用数据可视化
- ✅ **历史记录** - 查看最近的算卦记录
- ✅ **分享功能** - 一键分享算卦结果
- ✅ **夜间模式** - 自动检测并调整提示词风格
- ✅ **响应式设计** - 完美支持移动端和桌面端

### 后端功能 | Backend Features
- ✅ **用户追踪** - 基于IP的匿名用户识别
- ✅ **数据记录** - 自动记录所有交互数据
- ✅ **统计分析** - 多维度数据统计和分析
- ✅ **隐私保护** - IP哈希处理，符合GDPR
- ✅ **多LLM支持** - OpenAI、Anthropic、Azure等
- ✅ **智能Agent** - 基于问题类型选择算命工具

## 🔧 配置LLM提供商 | Configure LLM Providers

### OpenAI (默认)

```bash
OPENAI_API_KEY=sk-...
DEFAULT_LLM_MODEL=gpt-4
```

### Anthropic Claude

```bash
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_MODEL=claude-3-sonnet-20240229
```

### Azure OpenAI

```bash
AZURE_API_KEY=your_azure_key
AZURE_API_BASE=https://your-resource.openai.azure.com
DEFAULT_LLM_MODEL=azure/gpt-4
```

LiteLLM 会自动处理不同提供商的API调用，无需修改代码！

## 📦 项目结构 | Project Structure

```
Destiny/
├── frontend/              # React前端
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── backend_python/        # Python后端 (使用LiteLLM)
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── services/     # 业务服务
│   │   │   ├── llm_service.py    # LLM服务
│   │   │   └── prompt_service.py # 提示词服务
│   │   ├── config/       # 配置
│   │   └── main.py       # 主应用
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                  # 文档
├── docker-compose.yml     # Docker编排
└── README.md             # 本文档
```

## 🚢 部署 | Deployment

### Docker Compose (推荐)

```bash
# 生产环境部署 | Production deployment
docker-compose up -d

# 查看日志 | View logs
docker-compose logs -f

# 停止服务 | Stop services
docker-compose down
```

### 单独部署 | Individual Deployment

查看各服务的README文档：
- [后端部署指南](backend_python/README.md)
- 前端部署：构建后部署到静态服务器或CDN

## 📞 联系方式 | Contact

- **GitHub**: [https://github.com/manwjh/Destiny](https://github.com/manwjh/Destiny)
- **Issues**: [创建 Issue](https://github.com/manwjh/Destiny/issues)
- **Pull Requests**: [提交 PR](https://github.com/manwjh/Destiny/pulls)

## 📄 许可证 | License

MIT License
