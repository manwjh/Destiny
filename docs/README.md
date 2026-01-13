# 《算一卦/Destiny》 | Calculate a Fortune/Destiny

一个好玩的算命软件 - 不安慰你，只给结果的算卦器
A fun fortune-telling software - An oracle that doesn't comfort you, just gives results

## 📋 项目简介 | Project Introduction

这是一个中英文双语的 SaaS 算命服务，采用极简设计理念：
- **不解释** | No explanations
- **不负责** | No responsibility
- **不温柔** | Not gentle
- **但"像真话"** | But "feels real"

## 🚀 快速开始 | Quick Start

### 环境要求 | Requirements
- Python 3.8+
- Node.js 16+
- Cursor IDE (推荐) | Recommended

### 开发环境设置 | Development Setup
```bash
# 克隆项目 | Clone project
git clone <repository-url>
cd Destiny

# 创建虚拟环境 | Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 | or
venv\Scripts\activate     # Windows

# 安装依赖 | Install dependencies
pip install -r requirements.txt
```

## 📚 文档 | Documentation

### 核心文档 | Core Documents
- **[🚀 快速启动指南](quick-start-guide.md)** - 一键启动脚本使用指南
- **[📋 产品规划书](product-planning.md)** - 完整的项目规划和执行蓝图
- **[🏗️ 系统架构文档](system-architecture.md)** - 详细的系统架构设计和技术实现方案
- **[🎨 用户体验文档](user-experience.md)** - 完整的用户交互流程和界面设计规范
- **[🤖 Agent架构](AGENT_ARCHITECTURE.md)** - Fortune Agent 架构设计
- **[👤 用户追踪](USER_TRACKING.md)** - 用户追踪系统说明
- **[🔧 LLM配置](LLM_CONFIG.md)** - LLM服务配置指南
- **[🎯 Cursor 规则](../.cursorrules)** - Cursor IDE 专用开发规范

### 技术文档 | Technical Documentation
- **[🤖 Agent架构](AGENT_ARCHITECTURE.md)** - Fortune Agent 架构设计和实现
- **[👤 用户追踪](USER_TRACKING.md)** - 用户追踪系统设计和隐私保护
- **[🔧 LLM配置](LLM_CONFIG.md)** - LLM服务配置和提供商支持

### 版本管理 | Version Management
- **[📝 更新日志](../CHANGELOG.md)** - 版本更新历史和变更记录
- **[🔖 版本管理指南](../VERSIONING.md)** - 版本管理规范和操作指南
- **[📦 VERSION](../VERSION)** - 当前版本号

### 📖 文档目录 | Documentation
详细文档请查看 [docs/README.md](docs/README.md)

## 🏗️ 项目结构 | Project Structure

```
Destiny/
├── docs/                 # 项目文档 | Documentation
│   ├── product-planning.md
│   └── README.md
├── .cursorrules         # Cursor IDE 规则 | Cursor IDE Rules
├── README.md           # 项目说明 | Project Description
└── ...                 # 源代码目录 | Source Code
```

## 🎯 开发规范 | Development Standards

### 必须遵守的规则 | Must Follow Rules

1. **📖 阅读规则**: 开始开发前务必阅读所有规则文档
2. **🎯 Cursor 优先**: 推荐使用 Cursor IDE 进行开发
3. **🔧 规范遵循**: 严格遵循编程规则和最佳实践
4. **📋 规划执行**: 按照产品规划书执行开发任务

### 核心理念 | Core Philosophy
- **炸裂体验**: 让用户算完忍不住截图、转发、@朋友
- **极简设计**: 首页只有输入框、按钮、空白
- **真实反馈**: 给用户"像真话"的结果，而非安慰

## 🤝 贡献指南 | Contributing

### 开发流程 | Development Process
1. **Fork** 本仓库 | Fork this repository
2. **创建分支** | Create a feature branch
3. **遵守规则** | Follow all coding standards
4. **提交 PR** | Submit a Pull Request

### 代码审查 | Code Review
- 确保符合编程规则
- 保持代码质量标准
- 遵循产品设计理念

## 📈 项目进度 | Project Progress

### 已完成 | Completed ✅
- [x] 产品规划文档 | Product planning document
- [x] 系统架构文档 | System architecture document
- [x] Cursor IDE 规则 | Cursor IDE rules
- [x] 项目结构搭建 | Project structure setup

### 进行中 | In Progress 🚧
- [ ] 核心功能开发 | Core feature development
- [ ] 卦词库构建 | Fortune database construction
- [ ] 用户界面设计 | User interface design

### 计划中 | Planned 📋
- [ ] 双语系统实现 | Bilingual system implementation
- [ ] SaaS 架构搭建 | SaaS architecture setup
- [ ] 测试和部署 | Testing and deployment

## 📞 联系我们 | Contact

如有问题或建议，请通过以下方式联系：
For questions or suggestions, please contact us through:

- **GitHub**: [https://github.com/manwjh/Destiny](https://github.com/manwjh/Destiny)
- **Issues**: [创建 Issue](https://github.com/manwjh/Destiny/issues)
- **Discussions**: 项目讨论区
- **Email**: your-email@example.com

## 📄 许可证 | License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

*"不是现在不行，是你已经不想要了"* - 《算一卦》

*"It's not that it's not possible now, you just don't want it anymore"* - Calculate a Fortune