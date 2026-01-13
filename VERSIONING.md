# 版本管理指南 | Version Management Guide

## 📋 版本规范 | Version Format

本项目遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)（Semantic Versioning）

### 版本号格式 | Version Number Format

```
MAJOR.MINOR.PATCH
主版本号.次版本号.修订号
```

- **MAJOR (主版本号)**: 不兼容的API修改
- **MINOR (次版本号)**: 向下兼容的功能性新增
- **PATCH (修订号)**: 向下兼容的问题修正

### 版本示例 | Version Examples

- `0.1.0` - 首个功能版本
- `0.1.1` - Bug修复版本
- `0.2.0` - 新增功能版本
- `1.0.0` - 第一个稳定版本
- `2.0.0` - 重大API变更

---

## 📁 版本文件位置 | Version File Locations

项目中的版本信息分布在以下文件：

### 核心版本文件 | Core Version Files

1. **`VERSION`** - 项目根目录，纯版本号
   ```
   0.1.0
   ```

2. **`.version.json`** - 项目根目录，完整版本信息（JSON格式）
   ```json
   {
     "version": "0.1.0",
     "releaseDate": "2026-01-13",
     ...
   }
   ```

3. **`CHANGELOG.md`** - 版本变更日志，记录所有版本的变更内容

### 前端版本文件 | Frontend Version Files

4. **`frontend/package.json`** - NPM包配置
   ```json
   {
     "version": "0.1.0",
     ...
   }
   ```

5. **`frontend/src/version.ts`** - TypeScript版本配置
   ```typescript
   export const VERSION = '0.1.0';
   ```

### 后端版本文件 | Backend Version Files

6. **`backend_python/__version__.py`** - Python版本模块
   ```python
   __version__ = "0.1.0"
   ```

7. **`backend_python/app/config/settings.py`** - 应用配置（自动从__version__.py导入）

---

## 🔄 版本更新流程 | Version Update Process

### 1. 决定版本号 | Determine Version Number

根据变更类型选择版本号递增规则：

- **Bug修复** → 递增 PATCH (如 0.1.0 → 0.1.1)
- **新功能（向下兼容）** → 递增 MINOR (如 0.1.1 → 0.2.0)
- **破坏性变更** → 递增 MAJOR (如 0.2.0 → 1.0.0)

### 2. 更新版本文件 | Update Version Files

按以下顺序更新所有版本文件：

#### a. 更新核心版本文件

```bash
# 1. 更新 VERSION 文件
echo "0.2.0" > VERSION

# 2. 更新 .version.json
# 手动编辑或使用脚本更新
```

#### b. 更新前端版本

```bash
cd frontend
npm version 0.2.0 --no-git-tag-version
# 这会自动更新 package.json 和 package-lock.json

# 手动更新 src/version.ts
```

#### c. 更新后端版本

编辑 `backend_python/__version__.py`:
```python
__version__ = "0.2.0"
__version_info__ = (0, 2, 0)
VERSION_TAG = "v0.2.0"
RELEASE_DATE = "2026-XX-XX"  # 更新发布日期
```

### 3. 更新 CHANGELOG.md | Update Changelog

在 `CHANGELOG.md` 文件顶部添加新版本记录：

```markdown
## [0.2.0] - 2026-XX-XX

### Added
- 新增功能1
- 新增功能2

### Changed
- 变更内容1

### Fixed
- 修复问题1
```

### 4. 提交版本变更 | Commit Version Changes

```bash
git add VERSION .version.json CHANGELOG.md
git add frontend/package.json frontend/package-lock.json frontend/src/version.ts
git add backend_python/__version__.py
git commit -m "chore: bump version to v0.2.0"
```

### 5. 创建Git标签 | Create Git Tag

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

### 6. 发布 | Release

- 在GitHub上创建Release
- 附加CHANGELOG内容
- 上传构建产物（如需要）

---

## 🛠️ 版本管理工具 | Version Management Tools

### 快速版本更新脚本（计划中）

```bash
# 使用脚本自动更新所有版本文件
./scripts/bump_version.sh patch   # 0.1.0 → 0.1.1
./scripts/bump_version.sh minor   # 0.1.1 → 0.2.0
./scripts/bump_version.sh major   # 0.2.0 → 1.0.0
```

### 版本验证脚本（计划中）

```bash
# 验证所有版本文件是否一致
./scripts/verify_version.sh
```

---

## 📝 变更日志规范 | Changelog Standards

### 变更类型 | Change Types

使用以下标准类型标记变更：

- **Added** - 新增功能
- **Changed** - 功能变更
- **Deprecated** - 即将废弃的功能
- **Removed** - 已移除的功能
- **Fixed** - 问题修复
- **Security** - 安全相关修复

### Changelog 模板

```markdown
## [版本号] - 日期

### Added | 新增
- 新增功能描述（中文）
- New feature description (English)

### Changed | 变更
- 变更内容描述

### Fixed | 修复
- 修复问题描述

### Security | 安全
- 安全修复描述
```

---

## 🔍 版本信息查询 | Version Information Query

### 查看当前版本 | Check Current Version

```bash
# 方法1: 查看 VERSION 文件
cat VERSION

# 方法2: 查看前端版本
cd frontend && npm version

# 方法3: 查看后端版本
cd backend_python && python -c "from __version__ import __version__; print(__version__)"

# 方法4: 通过API查询（需要启动后端）
curl http://localhost:8000/api/v1/version
```

### 前端中使用版本 | Use Version in Frontend

```typescript
import { VERSION, getFullVersion } from './version';

console.log(`当前版本: ${VERSION}`);
const versionInfo = getFullVersion();
```

### 后端中使用版本 | Use Version in Backend

```python
from __version__ import __version__, get_full_version

print(f"当前版本: {__version__}")
version_info = get_full_version()
```

---

## 🎯 版本规划 | Version Planning

### 里程碑版本 | Milestone Versions

- **v0.1.0** ✅ - 首个功能版本（当前）
- **v0.2.0** 🚧 - 增强UI和用户体验
- **v0.3.0** 📋 - 社交分享功能
- **v0.4.0** 📋 - 用户系统和历史记录
- **v0.5.0** 📋 - 性能优化和监控
- **v1.0.0** 🎯 - 正式发布版

### 发布周期 | Release Cycle

- **PATCH版本**: 随时发布，修复紧急bug
- **MINOR版本**: 每2-4周发布，包含新功能
- **MAJOR版本**: 根据产品规划，重大版本更新

---

## ⚠️ 注意事项 | Important Notes

1. **版本一致性**: 确保所有版本文件中的版本号保持一致
2. **发布前测试**: 每次版本更新前必须进行完整测试
3. **文档更新**: 重大版本更新时同步更新相关文档
4. **向下兼容**: 在v1.0.0之前，MINOR版本可能包含破坏性变更
5. **Tag命名**: Git标签统一使用 `v{version}` 格式（如 v0.1.0）

---

## 📚 参考资料 | References

- [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)

---

*最后更新时间 | Last Updated: 2026-01-13*
