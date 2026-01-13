#!/bin/bash

# ======================================================================
# 《算一卦/Destiny》快速启动脚本
# Quick Start Script for Destiny Project
# ======================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 显示帮助信息
show_help() {
    cat << EOF
使用方法 | Usage:
    ./quick_start.sh [选项]

选项 | Options:
    -y, --yes, --force    自动终止占用端口的进程，无需确认
    -h, --help            显示此帮助信息

示例 | Examples:
    ./quick_start.sh              # 交互式启动（遇到端口占用会询问）
    ./quick_start.sh -y           # 自动启动（自动终止占用端口的进程）
    ./quick_start.sh --force      # 同上
EOF
    exit 0
}

# 解析命令行参数
FORCE_KILL=false
for arg in "$@"; do
    case $arg in
        -y|--yes|--force)
            FORCE_KILL=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "未知选项: $arg"
            echo "使用 './quick_start.sh --help' 查看帮助"
            exit 1
            ;;
    esac
done

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# 打印Banner
print_banner() {
    cat << "EOF"
    
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           《算一卦》/ Destiny - Quick Start              ║
    ║                                                           ║
    ║        不安慰你，只给结果的算卦器                           ║
    ║     An oracle that doesn't comfort, just results         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
EOF
    
    if [ "$FORCE_KILL" = true ]; then
        log_info "运行模式: 自动终止占用端口的进程 (--force)"
    else
        log_info "提示: 使用 './quick_start.sh -y' 可以自动终止占用端口的进程"
    fi
}

# 检查命令是否存在
check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "$1 已安装: $(command -v $1)"
        return 0
    else
        log_error "$1 未安装"
        return 1
    fi
}

# 检查Python版本
check_python_version() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
            log_success "Python 版本: $PYTHON_VERSION (符合要求 >= 3.9)"
            return 0
        else
            log_error "Python 版本: $PYTHON_VERSION (需要 >= 3.9)"
            return 1
        fi
    else
        log_error "Python 3 未安装"
        return 1
    fi
}

# 检查Node.js版本
check_node_version() {
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version | sed 's/v//')
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
        
        if [ "$NODE_MAJOR" -ge 18 ]; then
            log_success "Node.js 版本: $NODE_VERSION (符合要求 >= 18)"
            return 0
        else
            log_error "Node.js 版本: $NODE_VERSION (需要 >= 18)"
            return 1
        fi
    else
        log_error "Node.js 未安装"
        return 1
    fi
}

# 环境检查
check_environment() {
    log_step "步骤 1: 环境检查"
    
    local all_ok=true
    
    # 检查Python
    if ! check_python_version; then
        all_ok=false
        log_warning "请安装 Python 3.9 或更高版本: https://www.python.org/downloads/"
    fi
    
    # 检查Node.js
    if ! check_node_version; then
        all_ok=false
        log_warning "请安装 Node.js 18 或更高版本: https://nodejs.org/"
    fi
    
    # 检查npm
    if ! check_command "npm"; then
        all_ok=false
        log_warning "npm 通常随 Node.js 一起安装"
    fi
    
    # 检查Docker（可选）
    if check_command "docker"; then
        log_info "Docker 可用，可以使用 docker-compose 启动"
    else
        log_warning "Docker 未安装（可选），如需使用请访问: https://www.docker.com/"
    fi
    
    # 检查Docker Compose（可选）
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        log_info "Docker Compose 可用"
    else
        log_warning "Docker Compose 未安装（可选）"
    fi
    
    if [ "$all_ok" = false ]; then
        log_error "环境检查未通过，请先安装必需的依赖"
        exit 1
    fi
    
    log_success "环境检查通过！"
}

# 创建Python虚拟环境
setup_python_venv() {
    log_step "步骤 2: 创建 Python 虚拟环境"
    
    cd "$PROJECT_ROOT"
    
    if [ -d "venv" ]; then
        log_info "虚拟环境已存在"
    else
        log_info "创建 Python 虚拟环境..."
        python3 -m venv venv
        log_success "虚拟环境创建成功"
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    log_info "升级 pip..."
    pip install --upgrade pip -q
    
    log_success "Python 虚拟环境就绪"
}

# 安装后端依赖
install_backend_dependencies() {
    log_step "步骤 3: 安装后端依赖"
    
    cd "$PROJECT_ROOT/backend_python"
    source "$PROJECT_ROOT/venv/bin/activate"
    
    log_info "安装 Python 依赖包..."
    pip install -r requirements.txt -q
    
    log_success "后端依赖安装完成"
}

# 安装前端依赖
install_frontend_dependencies() {
    log_step "步骤 4: 安装前端依赖"
    
    cd "$PROJECT_ROOT/frontend"
    
    if [ -d "node_modules" ]; then
        log_info "前端依赖已安装"
    else
        log_info "安装 Node.js 依赖包..."
        npm install
        log_success "前端依赖安装完成"
    fi
}

# 配置环境变量
setup_environment_variables() {
    log_step "步骤 5: 配置环境变量"
    
    cd "$PROJECT_ROOT/backend_python"
    
    if [ -f ".env" ]; then
        log_success "环境配置文件已存在"
        
        # 静默检查API Key，不显示警告（在最后统一提示）
        if grep -q "your_.*_api_key" .env 2>/dev/null || ! grep -q "LLM_API_KEY=" .env 2>/dev/null; then
            # 标记需要配置API Key，但不在这里显示警告
            export NEED_API_KEY_CONFIG=true
        fi
    else
        log_info "创建默认环境配置文件..."
        
        cat > .env << 'EOF'
# 应用配置
DEBUG=true
PORT=8000
HOST=127.0.0.1

# LLM 配置
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your_openai_api_key_here
LLM_BASE_URL=
LLM_MAX_CONTEXT_TOKENS=8000
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=300

# 向后兼容
DEFAULT_LLM_MODEL=gpt-4
FALLBACK_LLM_MODEL=gpt-3.5-turbo

# 可选配置
# ANTHROPIC_API_KEY=your_anthropic_api_key
# REDIS_URL=redis://localhost:6379
# DATABASE_URL=postgresql://user:pass@localhost:5432/destiny

# CORS配置
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# 日志配置
LOG_LEVEL=INFO

# 速率限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
EOF
        
        log_success "已创建默认配置文件"
        export NEED_API_KEY_CONFIG=true
        
        # 不再询问是否编辑，在最后统一提示
    fi
}

# 检查Docker中的可选服务
check_optional_services() {
    log_step "步骤 6: 检查可选服务（Docker）"
    
    if command -v docker &> /dev/null; then
        log_info "检查 Docker 容器状态..."
        
        # 检查Redis容器
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -q redis; then
            log_success "✓ Redis 容器正在运行"
        else
            log_info "  - Redis 容器未运行（可使用 docker compose 启动）"
        fi
        
        # 检查PostgreSQL容器
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -q -E '(postgres|db)'; then
            log_success "✓ PostgreSQL 容器正在运行"
        else
            log_info "  - PostgreSQL 容器未运行（可使用 docker compose 启动）"
        fi
        
        log_info "提示: 使用 'docker compose up -d db redis' 启动数据库服务"
    else
        log_info "Docker 未运行，跳过容器检查"
    fi
    
    log_success "可选服务检查完成"
}

# 构建前端
build_frontend() {
    log_step "步骤 8: 构建前端应用"
    
    cd "$PROJECT_ROOT/frontend"
    
    log_info "构建前端应用..."
    if npm run build; then
        log_success "前端构建成功"
    else
        log_error "前端构建失败"
        exit 1
    fi
}

# 启动后端服务
start_backend() {
    log_step "步骤 9: 启动后端服务"
    
    cd "$PROJECT_ROOT/backend_python"
    source "$PROJECT_ROOT/venv/bin/activate"
    
    # 检查端口是否被占用
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口 8000 已被占用"
        
        if [ "$FORCE_KILL" = true ]; then
            log_info "自动终止占用端口的进程..."
            lsof -ti:8000 | xargs kill -9 2>/dev/null || true
            sleep 2
        else
            read -p "是否终止现有进程？(y/n) " -t 10 -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                lsof -ti:8000 | xargs kill -9 2>/dev/null || true
                sleep 2
            else
                log_error "无法启动后端服务，端口被占用"
                log_info "提示：可以使用 './quick_start.sh -y' 自动终止占用端口的进程"
                exit 1
            fi
        fi
    fi
    
    log_info "启动 FastAPI 后端服务..."
    
    # 在后台启动服务
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$PROJECT_ROOT/logs/backend.log" 2>&1 &
    BACKEND_PID=$!
    
    # 等待服务启动
    log_info "等待后端服务启动..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            log_success "后端服务启动成功 (PID: $BACKEND_PID)"
            echo $BACKEND_PID > "$PROJECT_ROOT/logs/backend.pid"
            return 0
        fi
        sleep 1
    done
    
    log_error "后端服务启动失败，请查看日志: $PROJECT_ROOT/logs/backend.log"
    exit 1
}

# 启动前端服务
start_frontend() {
    log_step "步骤 10: 启动前端服务"
    
    cd "$PROJECT_ROOT/frontend"
    
    # 检查端口是否被占用
    if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "端口 5173 已被占用"
        
        if [ "$FORCE_KILL" = true ]; then
            log_info "自动终止占用端口的进程..."
            lsof -ti:5173 | xargs kill -9 2>/dev/null || true
            sleep 2
        else
            read -p "是否终止现有进程？(y/n) " -t 10 -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                lsof -ti:5173 | xargs kill -9 2>/dev/null || true
                sleep 2
            else
                log_error "无法启动前端服务，端口被占用"
                log_info "提示：可以使用 './quick_start.sh -y' 自动终止占用端口的进程"
                exit 1
            fi
        fi
    fi
    
    log_info "启动 Vite 开发服务器..."
    
    # 在后台启动服务
    nohup npm run dev > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    
    # 等待服务启动
    log_info "等待前端服务启动..."
    for i in {1..15}; do
        if curl -s http://localhost:5173 > /dev/null 2>&1; then
            log_success "前端服务启动成功 (PID: $FRONTEND_PID)"
            echo $FRONTEND_PID > "$PROJECT_ROOT/logs/frontend.pid"
            return 0
        fi
        sleep 1
    done
    
    log_warning "前端服务可能需要更长时间启动，请稍后访问"
    echo $FRONTEND_PID > "$PROJECT_ROOT/logs/frontend.pid"
}

# 测试系统
test_system() {
    log_step "步骤 11: 系统测试"
    
    log_info "测试后端健康检查..."
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        log_success "后端健康检查通过"
    else
        log_error "后端健康检查失败"
    fi
    
    log_info "测试算卦API..."
    if curl -s -X POST http://localhost:8000/api/v1/divine \
        -H "Content-Type: application/json" \
        -d '{"question":"测试","language":"zh"}' | grep -q "success"; then
        log_success "算卦API测试通过"
    else
        log_error "算卦API测试失败"
    fi
}

# 打印启动信息
print_startup_info() {
    clear
    
    cat << "EOF"

    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           《算一卦》 Destiny - 启动成功！                  ║
    ║                  🎉 All Services Running 🎉              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝

EOF

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}          👉 请在浏览器中打开以下地址 👈${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "   ${CYAN}🌐 前端应用 (Frontend):${NC}"
    echo -e "      ${YELLOW}➜  http://localhost:5173${NC}"
    echo ""
    echo -e "   ${CYAN}📡 后端API (Backend):${NC}"
    echo -e "      ➜  http://localhost:8000"
    echo ""
    echo -e "   ${CYAN}📚 API文档 (Docs):${NC}"
    echo -e "      ➜  http://localhost:8000/docs"
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # 自动打开浏览器（可选）
    if command -v open &> /dev/null; then
        echo -e "${CYAN}💡 提示: 正在自动打开浏览器...${NC}"
        sleep 1
        open http://localhost:5173 2>/dev/null || true
    elif command -v xdg-open &> /dev/null; then
        echo -e "${CYAN}💡 提示: 正在自动打开浏览器...${NC}"
        sleep 1
        xdg-open http://localhost:5173 2>/dev/null || true
    fi
    
    echo ""
    echo -e "${CYAN}📝 管理命令:${NC}"
    echo -e "   停止服务: ${YELLOW}./stop.sh${NC}"
    echo -e "   查看日志: ${YELLOW}tail -f logs/backend.log${NC}"
    echo ""
    
    # 检查Docker服务状态
    if command -v docker &> /dev/null; then
        if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -q -E '(redis|postgres|db)'; then
            echo -e "${CYAN}💡 可选: 启动数据库服务（Docker）${NC}"
            echo -e "   ${YELLOW}docker compose up -d db redis${NC}"
            echo -e "   （提供缓存和数据持久化功能）"
            echo ""
        fi
    fi
    
    # 检查API Key配置
    if grep -q "your_.*_api_key" "$PROJECT_ROOT/backend_python/.env" 2>/dev/null; then
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}⚠️  警告: 请配置真实的 LLM API Key！${NC}"
        echo -e "${YELLOW}   编辑: backend_python/.env${NC}"
        echo -e "${YELLOW}   然后重启: ./stop.sh && ./quick_start.sh${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
    fi
    
    echo -e "${PURPLE}按 Ctrl+C 可以停止查看此信息，服务将继续在后台运行${NC}"
    echo ""
}

# 创建停止脚本
create_stop_script() {
    cat > "$PROJECT_ROOT/stop.sh" << 'EOF'
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
EOF
    
    chmod +x "$PROJECT_ROOT/stop.sh"
    log_success "已创建停止脚本: stop.sh"
}

# 主函数
main() {
    print_banner
    
    log_info "开始《算一卦/Destiny》快速启动流程..."
    
    # 执行所有步骤
    check_environment
    setup_python_venv
    install_backend_dependencies
    install_frontend_dependencies
    setup_environment_variables
    check_optional_services
    # build_frontend  # 开发环境可以跳过构建，直接使用 npm run dev
    start_backend
    start_frontend
    
    sleep 3  # 等待服务稳定
    
    test_system
    create_stop_script
    print_startup_info
}

# 运行主函数
main