# Git 发布指南 | Git Release Guide

## 🎯 v0.1.0 首次发布步骤 | First Release Steps for v0.1.0

本指南将帮助你完成 v0.1.0 版本的 Git 提交和 GitHub 发布。  
*This guide will help you complete the Git commit and GitHub release for v0.1.0.*

---

## 📋 前置检查 | Pre-release Checklist

在发布之前，请确认以下事项：  
*Before releasing, please confirm the following:*

- [x] ✅ 所有版本文件已创建并正确配置
- [x] ✅ 版本验证脚本测试通过 (`./scripts/verify_version.sh`)
- [x] ✅ CHANGELOG.md 已完整记录 v0.1.0 变更
- [x] ✅ README.md 已更新版本信息和仓库链接
- [ ] ⏳ 本地测试通过（前端和后端）
- [ ] ⏳ 代码质量检查通过
- [ ] ⏳ 文档审查完成

---

## 🔧 步骤 1: 初始化 Git 仓库（如尚未初始化）

如果项目还没有初始化 Git，先执行：  
*If the project hasn't been initialized with Git yet, run:*

```bash
cd /Users/wangjunhui/playcode/Destiny

# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin https://github.com/manwjh/Destiny.git
```

---

## 📦 步骤 2: 提交版本管理相关文件

### 2.1 查看当前状态

```bash
# 查看所有变更文件
git status
```

### 2.2 添加版本管理文件

```bash
# 添加版本核心文件
git add VERSION
git add .version.json
git add CHANGELOG.md
git add VERSIONING.md
git add VERSION_MANAGEMENT_SUMMARY.md
git add GIT_RELEASE_GUIDE.md

# 添加前端版本文件
git add frontend/package.json
git add frontend/package-lock.json
git add frontend/src/version.ts

# 添加后端版本文件
git add backend_python/__version__.py
git add backend_python/app/config/settings.py
git add backend_python/app/main.py

# 添加版本验证脚本
git add scripts/verify_version.sh

# 添加更新的文档
git add README.md
git add docs/README.md

# 添加 GitHub 模板
git add .github/
```

### 2.3 提交版本管理系统

```bash
# 提交版本管理系统
git commit -m "chore: establish version management system v0.1.0

- Add VERSION file with semantic versioning
- Create comprehensive CHANGELOG.md
- Add .version.json with full version metadata
- Implement version modules for frontend (version.ts) and backend (__version__.py)
- Update package.json and settings.py with v0.1.0
- Add version API endpoint (/api/v1/version)
- Create VERSIONING.md guide document
- Add version verification script (verify_version.sh)
- Update README.md with version badges and GitHub links
- Add GitHub templates (PR, Issue)

Current version: v0.1.0
Release date: 2026-01-13"
```

---

## 🏷️ 步骤 3: 创建 Git 标签

```bash
# 创建带注释的标签
git tag -a v0.1.0 -m "Release v0.1.0 - Initial Release

🎉 首个功能版本发布 | First Functional Release

核心功能 | Core Features:
- ✅ 算命判决引擎 | Fortune telling engine
- ✅ 多LLM支持 (OpenAI, Claude, Azure等) | Multi-LLM support
- ✅ 双语界面 (中英文) | Bilingual interface (CN/EN)
- ✅ 用户追踪和统计 | User tracking and statistics
- ✅ 响应式设计 | Responsive design
- ✅ Docker部署支持 | Docker deployment support

技术栈 | Tech Stack:
- Frontend: React 18 + TypeScript + Tailwind CSS
- Backend: FastAPI + LiteLLM + Python 3.9+
- Database: PostgreSQL + Redis

详见 CHANGELOG.md | See CHANGELOG.md for details
"

# 查看标签
git tag -l
git show v0.1.0
```

---

## 🚀 步骤 4: 推送到 GitHub

### 4.1 推送代码

```bash
# 如果是首次推送，需要设置上游分支
git push -u origin main

# 或者，如果已经设置过
git push origin main
```

### 4.2 推送标签

```bash
# 推送特定标签
git push origin v0.1.0

# 或推送所有标签
git push origin --tags
```

---

## 📝 步骤 5: 在 GitHub 创建 Release

### 5.1 访问 Release 页面

打开浏览器，访问：  
*Open your browser and visit:*

```
https://github.com/manwjh/Destiny/releases/new
```

### 5.2 填写 Release 信息

#### 标签选择 | Choose Tag
- 选择: `v0.1.0`

#### 发布标题 | Release Title
```
v0.1.0 - Initial Release 🎉
```

#### 发布说明 | Release Description

复制以下内容到发布说明中（或从 CHANGELOG.md 复制）：  
*Copy the following content (or copy from CHANGELOG.md):*

```markdown
# v0.1.0 - 首个功能版本 | Initial Functional Release

🎉 欢迎使用《算一卦/Destiny》的首个正式版本！  
*Welcome to the first official release of "Calculate a Fortune/Destiny"!*

## ✨ 核心功能 | Core Features

### 产品特性 | Product Features
- 🎯 **命运判决引擎** - 基于大语言模型的智能算命系统
- 💬 **双语支持** - 完整的中英文界面切换
- 📊 **用户统计** - 匿名用户追踪和数据可视化
- 📜 **历史记录** - 查看最近的算卦记录
- 🔗 **分享功能** - 一键分享算卦结果
- 🎨 **响应式设计** - 完美适配移动端和桌面端

### 技术特性 | Technical Features
- 🤖 **多LLM支持** - 支持 OpenAI、Anthropic、Azure 等多个AI提供商
- 🔌 **统一接入** - 通过 LiteLLM 实现无缝切换
- 🎭 **智能Agent** - 基于问题类型智能选择算命工具
- 🔒 **隐私保护** - IP哈希处理，符合GDPR标准
- 📦 **容器化部署** - 完整的 Docker 和 Docker Compose 支持
- 🚀 **快速启动** - 一键启动脚本，开箱即用

## 🏗️ 技术栈 | Tech Stack

### 前端 | Frontend
- React 18.x
- TypeScript 5.x
- Tailwind CSS 4.x
- Vite 7.x
- Framer Motion 12.x

### 后端 | Backend
- Python 3.9+
- FastAPI 0.128.0+
- LiteLLM 1.80.0+
- PostgreSQL 15+
- Redis 7.0+

## 🚀 快速开始 | Quick Start

### 方式 1: 本地开发
\`\`\`bash
git clone https://github.com/manwjh/Destiny.git
cd Destiny
./quick_start.sh
\`\`\`

### 方式 2: Docker 部署
\`\`\`bash
git clone https://github.com/manwjh/Destiny.git
cd Destiny
./docker_quick_start.sh
\`\`\`

## 📚 文档 | Documentation

- 📋 [产品规划](docs/product-planning.md)
- 🏗️ [系统架构](docs/system-architecture.md)
- 🎨 [用户体验](docs/user-experience.md)
- 📝 [更新日志](CHANGELOG.md)
- 🔧 [版本管理](VERSIONING.md)

## 📝 已知限制 | Known Limitations

- 当前版本仅支持文本交互
- 卦象展示为文本形式
- 用户数据存储需进一步优化
- 分享功能需补充社交媒体集成

## 🔜 后续计划 | Roadmap

- v0.2.0: 增强用户体验和视觉效果
- v0.3.0: 社交分享功能完善
- v0.4.0: 个性化推荐系统
- v1.0.0: 正式版本发布

## 🙏 致谢 | Acknowledgments

感谢所有为这个项目做出贡献的开发者和用户！  
*Thanks to all developers and users who contributed to this project!*

---

**完整变更日志**: [CHANGELOG.md](https://github.com/manwjh/Destiny/blob/main/CHANGELOG.md)

*"不是现在不行，是你已经不想要了"* - 《算一卦》
```

### 5.3 发布设置

- [ ] ✅ 勾选 "Set as the latest release"（设置为最新版本）
- [ ] 如需预发布，勾选 "This is a pre-release"

### 5.4 点击发布

点击 **"Publish release"** 按钮完成发布。

---

## ✅ 步骤 6: 验证发布

### 6.1 检查 GitHub

访问以下链接确认发布成功：  
*Visit the following links to confirm successful release:*

- **Releases**: https://github.com/manwjh/Destiny/releases
- **Tags**: https://github.com/manwjh/Destiny/tags
- **Latest Release**: https://github.com/manwjh/Destiny/releases/latest

### 6.2 本地验证

```bash
# 验证标签
git tag -l

# 查看标签详情
git show v0.1.0

# 验证远程仓库
git remote -v

# 检查远程分支和标签
git ls-remote --tags origin
```

---

## 🎯 后续版本发布流程 | Future Release Process

当需要发布新版本时（如 v0.2.0），按照以下简化流程：

### 1. 更新版本号

```bash
# 更新所有版本文件（见 VERSIONING.md）
# 验证版本一致性
./scripts/verify_version.sh
```

### 2. 更新 CHANGELOG

在 `CHANGELOG.md` 顶部添加新版本记录

### 3. 提交和标签

```bash
# 提交变更
git add .
git commit -m "chore: bump version to v0.2.0"

# 创建标签
git tag -a v0.2.0 -m "Release v0.2.0 - [版本描述]"

# 推送
git push origin main --tags
```

### 4. GitHub Release

按照步骤 5 在 GitHub 创建新的 Release

---

## 🆘 常见问题 | Troubleshooting

### 问题 1: 推送被拒绝

```bash
# 如果远程有更新，先拉取
git pull origin main --rebase

# 解决冲突后再推送
git push origin main
```

### 问题 2: 标签已存在

```bash
# 删除本地标签
git tag -d v0.1.0

# 删除远程标签
git push origin :refs/tags/v0.1.0

# 重新创建标签
git tag -a v0.1.0 -m "..."
git push origin v0.1.0
```

### 问题 3: 版本不一致

```bash
# 运行验证脚本
./scripts/verify_version.sh

# 根据提示修复版本文件
# 修复后重新验证
```

---

## 📚 参考资料 | References

- [GitHub Release 文档](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Git 标签文档](https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/)

---

## ✨ 发布清单 | Release Checklist

最后，请确认以下所有事项都已完成：

- [ ] 版本验证脚本测试通过
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md 已完善
- [ ] 代码已提交到 Git
- [ ] Git 标签已创建
- [ ] 代码和标签已推送到 GitHub
- [ ] GitHub Release 已创建
- [ ] Release 页面显示正常
- [ ] README 徽章显示正确版本

---

**🎊 完成！现在你可以向世界展示《算一卦/Destiny》v0.1.0 了！**  
**🎊 Done! Now you can share "Calculate a Fortune/Destiny" v0.1.0 with the world!**

*创建时间 | Created: 2026-01-13*
