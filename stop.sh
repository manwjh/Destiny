#!/bin/bash

# ======================================================================
# 《算一卦/Destiny》服务停止脚本
# Service Stop Script
# ======================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 显示帮助
show_help() {
    cat << HELP
使用方法 | Usage:
    ./stop.sh [选项]

选项 | Options:
    -f, --force     强制终止所有相关进程
    -h, --help      显示此帮助信息

示例 | Examples:
    ./stop.sh              # 正常停止服务
    ./stop.sh -f           # 强制终止所有进程
HELP
    exit 0
}

# 解析参数
FORCE=false
for arg in "$@"; do
    case $arg in
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
    esac
done

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}停止《算一卦/Destiny》服务...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 停止后端
if [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
    BACKEND_PID=$(cat "$PROJECT_ROOT/logs/backend.pid")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        if [ "$FORCE" = true ]; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        else
            kill $BACKEND_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✓ 后端服务已停止 (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠ 后端服务未运行${NC}"
    fi
    rm "$PROJECT_ROOT/logs/backend.pid"
fi

# 停止前端
if [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat "$PROJECT_ROOT/logs/frontend.pid")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        if [ "$FORCE" = true ]; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        else
            kill $FRONTEND_PID 2>/dev/null || true
        fi
        echo -e "${GREEN}✓ 前端服务已停止 (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠ 前端服务未运行${NC}"
    fi
    rm "$PROJECT_ROOT/logs/frontend.pid"
fi

# 额外清理（以防PID文件不准确或用户选择强制模式）
if [ "$FORCE" = true ]; then
    echo ""
    echo -e "${YELLOW}强制清理所有相关进程...${NC}"
    pkill -9 -f "uvicorn app.main:app" 2>/dev/null && echo -e "${GREEN}✓ 清理 uvicorn 进程${NC}" || true
    pkill -9 -f "vite" 2>/dev/null && echo -e "${GREEN}✓ 清理 vite 进程${NC}" || true
    
    # 清理可能占用的端口
    lsof -ti:8000 | xargs kill -9 2>/dev/null && echo -e "${GREEN}✓ 清理端口 8000${NC}" || true
    lsof -ti:5173 | xargs kill -9 2>/dev/null && echo -e "${GREEN}✓ 清理端口 5173${NC}" || true
else
    # 温和清理
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}所有服务已停止！All services stopped!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
