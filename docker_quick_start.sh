#!/bin/bash

# ======================================================================
# 《算一卦/Destiny》Docker 快速启动脚本
# Docker Quick Start Script for Destiny Project
# ======================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 显示帮助信息
show_help() {
    cat << EOF
使用方法 | Usage:
    ./docker_quick_start.sh [选项]

选项 | Options:
    -h, --help            显示此帮助信息
    --rebuild             强制重新构建镜像
    --clean               清理所有容器和数据卷后启动

示例 | Examples:
    ./docker_quick_start.sh              # 正常启动
    ./docker_quick_start.sh --rebuild    # 重新构建镜像后启动
    ./docker_quick_start.sh --clean      # 清理后重新启动
EOF
    exit 0
}

# 解析命令行参数
REBUILD=false
CLEAN=false
for arg in "$@"; do
    case $arg in
        -h|--help)
            show_help
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "未知选项: $arg"
            echo "使用 './docker_quick_start.sh --help' 查看帮助"
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
    ║      《算一卦》/ Destiny - Docker Quick Start            ║
    ║                                                           ║
    ║             使用 Docker 一键启动所有服务                   ║
    ║           One-click start with Docker                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
EOF
}

# 检查Docker
check_docker() {
    log_step "步骤 1: 检查 Docker 环境"
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装"
        log_info "请访问 https://www.docker.com/ 下载安装"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker 未运行"
        log_info "请启动 Docker Desktop 或 Docker 服务"
        exit 1
    fi
    
    log_success "Docker 已安装并运行"
    
    # 检查Docker Compose
    if docker compose version &> /dev/null; then
        log_success "Docker Compose V2 可用"
        DOCKER_COMPOSE="docker compose"
    elif command -v docker-compose &> /dev/null; then
        log_success "Docker Compose V1 可用"
        DOCKER_COMPOSE="docker-compose"
    else
        log_error "Docker Compose 未安装"
        exit 1
    fi
}

# 配置环境变量
setup_env() {
    log_step "步骤 2: 配置环境变量"
    
    cd "$PROJECT_ROOT/backend_python"
    
    if [ -f ".env" ]; then
        log_info ".env 文件已存在"
        
        if grep -q "your_.*_api_key" .env || ! grep -q "LLM_API_KEY=" .env; then
            log_warning "⚠️  请配置真实的 API Key"
        else
            log_success "环境变量已配置"
        fi
    else
        log_info "创建 .env 文件..."
        
        cat > .env << 'EOF'
# LLM 配置
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your_openai_api_key_here
LLM_BASE_URL=
LLM_MAX_CONTEXT_TOKENS=8000
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=300

# 应用配置
DEBUG=true
PORT=8000

# 数据库配置
DATABASE_URL=postgresql://destiny:destiny@db:5432/destiny

# Redis配置
REDIS_URL=redis://redis:6379

# CORS配置
CORS_ORIGINS=["http://localhost","http://localhost:3000","http://localhost:5173"]

# 日志配置
LOG_LEVEL=INFO
EOF
        
        log_success "已创建 .env 文件"
        log_warning "⚠️  请编辑 backend_python/.env 文件，添加你的 API Key"
        
        echo ""
        read -p "是否现在编辑 .env 文件？(y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    fi
}

# 启动Docker服务
start_docker_services() {
    log_step "步骤 3: 启动 Docker 服务"
    
    cd "$PROJECT_ROOT"
    
    if [ "$CLEAN" = true ]; then
        log_warning "清理所有容器和数据卷..."
        $DOCKER_COMPOSE down -v 2>/dev/null || true
        log_success "清理完成"
    else
        log_info "停止现有容器..."
        $DOCKER_COMPOSE down 2>/dev/null || true
    fi
    
    if [ "$REBUILD" = true ]; then
        log_info "强制重新构建镜像..."
        $DOCKER_COMPOSE build --no-cache
    else
        log_info "拉取/构建镜像..."
        $DOCKER_COMPOSE build
    fi
    
    log_info "启动所有服务..."
    $DOCKER_COMPOSE up -d
    
    log_success "Docker 服务已启动"
}

# 等待服务就绪
wait_for_services() {
    log_step "步骤 4: 等待服务就绪"
    
    log_info "等待后端服务启动..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            log_success "后端服务就绪"
            break
        fi
        sleep 2
        if [ $i -eq 30 ]; then
            log_warning "后端服务启动超时，请检查日志"
        fi
    done
    
    log_info "等待前端服务启动..."
    for i in {1..20}; do
        if curl -s http://localhost > /dev/null 2>&1; then
            log_success "前端服务就绪"
            break
        fi
        sleep 2
        if [ $i -eq 20 ]; then
            log_warning "前端服务启动超时，请检查日志"
        fi
    done
}

# 测试服务
test_services() {
    log_step "步骤 5: 测试服务"
    
    log_info "测试后端API..."
    if curl -s -X POST http://localhost:8000/api/v1/divine \
        -H "Content-Type: application/json" \
        -d '{"question":"Docker测试","language":"zh"}' | grep -q "success"; then
        log_success "后端API测试通过"
    else
        log_warning "后端API测试失败，可能需要配置API Key"
    fi
}

# 打印信息
print_info() {
    log_step "🎉 Docker 启动完成！"
    
    cat << EOF

${GREEN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              Docker 服务已成功启动！                       ║
║           Docker Services Started Successfully!           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝${NC}

${CYAN}📍 访问地址 | Access URLs:${NC}
   
   ${YELLOW}前端 Frontend:${NC}     http://localhost
   ${YELLOW}后端 Backend:${NC}      http://localhost:8000
   ${YELLOW}API文档 API Docs:${NC}  http://localhost:8000/docs
   ${YELLOW}Redis:${NC}             localhost:6379
   ${YELLOW}PostgreSQL:${NC}        localhost:5432

${CYAN}🐳 Docker 命令 | Docker Commands:${NC}

   查看日志: docker compose logs -f
   停止服务: docker compose down
   重启服务: docker compose restart
   查看状态: docker compose ps

${CYAN}🛠️  管理命令 | Management:${NC}

   查看后端日志: docker compose logs -f backend
   查看前端日志: docker compose logs -f frontend
   进入容器: docker compose exec backend bash

${CYAN}🔑 重要提示 | Important:${NC}

EOF

    if grep -q "your_.*_api_key" "$PROJECT_ROOT/backend_python/.env" 2>/dev/null; then
        echo -e "   ${RED}⚠️  请配置真实的 LLM API Key${NC}"
        echo -e "   ${YELLOW}编辑文件: backend_python/.env${NC}"
        echo -e "   ${YELLOW}然后重启: docker compose restart backend${NC}"
        echo ""
    fi
    
    cat << EOF
   ${GREEN}✓${NC} 所有服务运行在 Docker 容器中
   ${GREEN}✓${NC} 数据持久化在 Docker volumes 中
   ${GREEN}✓${NC} 支持一键启动和停止

${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}

${GREEN}开始使用《算一卦》吧！ Start using Destiny!${NC}

EOF
}

# 主函数
main() {
    print_banner
    
    log_info "开始 Docker 快速启动流程..."
    
    check_docker
    setup_env
    start_docker_services
    wait_for_services
    test_services
    print_info
}

# 运行主函数
main