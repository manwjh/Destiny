#!/bin/bash

###############################################################################
# 版本验证脚本 | Version Verification Script
# 《算一卦/Destiny》
# 
# 功能：验证所有版本文件中的版本号是否一致
# Usage: ./scripts/verify_version.sh
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}版本验证 | Version Verification${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 读取各个文件中的版本号
echo -e "${YELLOW}📋 读取版本信息...${NC}"

# 1. VERSION 文件
if [ -f "$PROJECT_ROOT/VERSION" ]; then
    VERSION_FILE=$(cat "$PROJECT_ROOT/VERSION" | tr -d '[:space:]')
    echo -e "  VERSION 文件: ${GREEN}$VERSION_FILE${NC}"
else
    echo -e "  ${RED}❌ VERSION 文件不存在${NC}"
    VERSION_FILE=""
fi

# 2. .version.json 文件
if [ -f "$PROJECT_ROOT/.version.json" ]; then
    VERSION_JSON=$(grep -m 1 '"version"' "$PROJECT_ROOT/.version.json" | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    echo -e "  .version.json: ${GREEN}$VERSION_JSON${NC}"
else
    echo -e "  ${RED}❌ .version.json 文件不存在${NC}"
    VERSION_JSON=""
fi

# 3. frontend/package.json
if [ -f "$PROJECT_ROOT/frontend/package.json" ]; then
    VERSION_FRONTEND=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PROJECT_ROOT/frontend/package.json" | head -1 | cut -d'"' -f4)
    echo -e "  frontend/package.json: ${GREEN}$VERSION_FRONTEND${NC}"
else
    echo -e "  ${RED}❌ frontend/package.json 文件不存在${NC}"
    VERSION_FRONTEND=""
fi

# 4. frontend/src/version.ts
if [ -f "$PROJECT_ROOT/frontend/src/version.ts" ]; then
    VERSION_TS=$(grep "^export const VERSION = " "$PROJECT_ROOT/frontend/src/version.ts" | head -1 | sed "s/.*= '\([^']*\)'.*/\1/")
    echo -e "  frontend/src/version.ts: ${GREEN}$VERSION_TS${NC}"
else
    echo -e "  ${RED}❌ frontend/src/version.ts 文件不存在${NC}"
    VERSION_TS=""
fi

# 5. backend_python/__version__.py
if [ -f "$PROJECT_ROOT/backend_python/__version__.py" ]; then
    VERSION_BACKEND=$(grep "__version__" "$PROJECT_ROOT/backend_python/__version__.py" | head -1 | cut -d'"' -f2)
    echo -e "  backend_python/__version__.py: ${GREEN}$VERSION_BACKEND${NC}"
else
    echo -e "  ${RED}❌ backend_python/__version__.py 文件不存在${NC}"
    VERSION_BACKEND=""
fi

echo ""

# 验证版本一致性
echo -e "${YELLOW}🔍 验证版本一致性...${NC}"
echo ""

VERSIONS=("$VERSION_FILE" "$VERSION_JSON" "$VERSION_FRONTEND" "$VERSION_TS" "$VERSION_BACKEND")
INCONSISTENT=false

# 获取第一个非空版本作为基准
BASE_VERSION=""
for v in "${VERSIONS[@]}"; do
    if [ -n "$v" ]; then
        BASE_VERSION="$v"
        break
    fi
done

if [ -z "$BASE_VERSION" ]; then
    echo -e "${RED}❌ 错误: 未找到任何版本信息${NC}"
    exit 1
fi

echo -e "  基准版本: ${BLUE}$BASE_VERSION${NC}"
echo ""

# 检查所有版本
[ -n "$VERSION_FILE" ] && [ "$VERSION_FILE" != "$BASE_VERSION" ] && echo -e "  ${RED}❌ VERSION 文件版本不一致: $VERSION_FILE${NC}" && INCONSISTENT=true
[ -n "$VERSION_JSON" ] && [ "$VERSION_JSON" != "$BASE_VERSION" ] && echo -e "  ${RED}❌ .version.json 版本不一致: $VERSION_JSON${NC}" && INCONSISTENT=true
[ -n "$VERSION_FRONTEND" ] && [ "$VERSION_FRONTEND" != "$BASE_VERSION" ] && echo -e "  ${RED}❌ frontend/package.json 版本不一致: $VERSION_FRONTEND${NC}" && INCONSISTENT=true
[ -n "$VERSION_TS" ] && [ "$VERSION_TS" != "$BASE_VERSION" ] && echo -e "  ${RED}❌ frontend/src/version.ts 版本不一致: $VERSION_TS${NC}" && INCONSISTENT=true
[ -n "$VERSION_BACKEND" ] && [ "$VERSION_BACKEND" != "$BASE_VERSION" ] && echo -e "  ${RED}❌ backend_python/__version__.py 版本不一致: $VERSION_BACKEND${NC}" && INCONSISTENT=true

if [ "$INCONSISTENT" = true ]; then
    echo ""
    echo -e "${RED}================================${NC}"
    echo -e "${RED}❌ 版本验证失败！${NC}"
    echo -e "${RED}Version verification failed!${NC}"
    echo -e "${RED}================================${NC}"
    echo ""
    echo -e "请确保所有版本文件中的版本号一致。"
    echo -e "Please ensure all version files have consistent version numbers."
    echo ""
    echo -e "参考文档: ${BLUE}VERSIONING.md${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 所有版本文件一致！${NC}"
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✅ 版本验证成功！${NC}"
    echo -e "${GREEN}Version verification passed!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo -e "当前版本: ${BLUE}v$BASE_VERSION${NC}"
    exit 0
fi
