# 更新日志 | Changelog

本文档记录了《算一卦/Destiny》项目的所有重要变更。

*All notable changes to the "Calculate a Fortune/Destiny" project will be documented in this file.*

版本格式遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)  
*The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).*

---

## [0.1.0] - 2026-01-13

### 🎉 首个版本发布 | Initial Release

这是《算一卦/Destiny》的首个功能版本，实现了核心的算命功能和基础架构。  
*This is the first functional release of "Calculate a Fortune/Destiny", implementing core fortune-telling features and basic architecture.*

### ✨ 新增功能 | Added

#### 前端 | Frontend
- ✅ **React 18 + TypeScript** 现代化前端框架
- ✅ **Tailwind CSS** 原子化CSS，实现极简UI设计
- ✅ **Framer Motion** 流畅的动画效果
- ✅ **双语支持** 完整的中英文界面切换
- ✅ **响应式设计** 支持移动端和桌面端
- ✅ **算卦交互** 用户提问、获取卦象和卦词的完整流程

#### 后端 | Backend
- ✅ **FastAPI** 现代化Python Web框架
- ✅ **LiteLLM** 统一的LLM接入层，支持多个AI提供商：
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude-3)
  - Azure OpenAI
  - Google PaLM/Gemini
  - Cohere
  - Hugging Face
- ✅ **命运判决引擎** (`fortune_agent.py`) 核心算命逻辑
- ✅ **提示词服务** 精心设计的prompt系统
- ✅ **数据库支持** PostgreSQL 用户数据存储
- ✅ **缓存支持** Redis 性能优化
- ✅ **API接口**：
  - `/api/divine` - 算卦接口
  - `/api/stats` - 统计接口
  - `/health` - 健康检查

#### 基础设施 | Infrastructure
- ✅ **Docker 支持** 完整的容器化部署方案
- ✅ **Docker Compose** 一键启动所有服务
- ✅ **快速启动脚本**：
  - `quick_start.sh` - 本地开发环境一键启动
  - `docker_quick_start.sh` - Docker容器化一键启动
  - `stop.sh` - 服务停止脚本
- ✅ **自动化测试** 集成测试脚本
- ✅ **环境配置** 完整的环境变量管理

#### 文档 | Documentation
- ✅ **产品规划文档** (`docs/product-planning.md`)
- ✅ **系统架构文档** (`docs/system-architecture.md`)
- ✅ **用户体验文档** (`docs/user-experience.md`)
- ✅ **快速开始指南** (`docs/quick-start-guide.md`)
- ✅ **Cursor 开发规范** (`.cursorrules`)
- ✅ **API 文档** 集成 Swagger UI
- ✅ **部署指南** (`DEPLOYMENT.md`)

### 🎯 核心特性 | Core Features

#### 产品理念 | Product Philosophy
- **不安慰，只给结果** - 直接、有态度的卦词
- **有后果** - 每个判决都暗示后果
- **有针对性** - 基于用户问题的个性化回答
- **"像真话"** - 保持真实感和冲击力

#### 技术特点 | Technical Highlights
- **多LLM支持** - 通过LiteLLM无缝切换AI提供商
- **高性能** - Redis缓存 + 异步处理
- **可扩展** - 模块化架构，易于扩展
- **开发友好** - 完善的开发工具和文档

### 🔧 技术栈 | Tech Stack

#### 前端 | Frontend
- React 18.x
- TypeScript 5.x
- Tailwind CSS 4.x
- Vite 7.x
- Framer Motion 12.x
- Axios 1.x

#### 后端 | Backend
- Python 3.9+
- FastAPI 0.128.0+
- LiteLLM 1.80.0+
- Uvicorn (ASGI Server)
- Pydantic 2.x

#### 数据库与缓存 | Database & Cache
- PostgreSQL 15+
- Redis 7.0+

#### 部署 | Deployment
- Docker 24+
- Docker Compose 2.x
- Nginx (前端代理)

### 📦 项目结构 | Project Structure

```
Destiny/
├── frontend/              # React前端
├── backend_python/        # Python后端
├── docs/                  # 项目文档
├── scripts/               # 工具脚本
├── docker-compose.yml     # Docker编排
├── quick_start.sh         # 快速启动脚本
└── README.md             # 项目说明
```

### 🚀 快速开始 | Quick Start

```bash
# 克隆项目
git clone <repository-url>
cd Destiny

# 方式1: 本地开发
./quick_start.sh

# 方式2: Docker部署
./docker_quick_start.sh
```

### 📝 已知限制 | Known Limitations

- 当前版本仅支持文本交互，暂不支持图片
- 卦象展示为文本形式，后续版本将增强视觉效果
- 用户数据存储功能已实现但需进一步优化
- 分享功能框架已搭建，需要补充社交媒体集成

### 🔜 后续规划 | Future Plans

详见 `docs/product-planning.md` 中的后续版本规划：
- v0.2.x: 增强用户体验和视觉效果
- v0.3.x: 社交分享功能完善
- v0.4.x: 个性化推荐系统
- v1.0.0: 正式版本发布

---

## 版本规范说明 | Version Format

本项目遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)：

- **主版本号(MAJOR)**: 不兼容的 API 修改
- **次版本号(MINOR)**: 向下兼容的功能性新增
- **修订号(PATCH)**: 向下兼容的问题修正

### 变更类型 | Change Types

- **Added** 新增功能
- **Changed** 功能变更
- **Deprecated** 即将废弃的功能
- **Removed** 已移除的功能
- **Fixed** 问题修复
- **Security** 安全相关修复

---

## [Unreleased]

### 计划中 | Planned
- 增强卦象的视觉呈现
- 添加用户历史记录查询
- 完善分享功能的社交媒体集成
- 性能监控和日志系统优化

---

*最后更新时间 | Last Updated: 2026-01-13*
