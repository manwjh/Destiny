#!/bin/bash

# 《算一卦/Destiny》项目设置脚本
# Setup script for Destiny project

set -e

echo "🎯 《算一卦/Destiny》项目设置"
echo "================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.9+"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 18+"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"

# 创建Python虚拟环境
echo ""
echo "📦 创建Python虚拟环境..."
cd "$(dirname "$0")/.."
python3 -m venv venv
echo "✅ 虚拟环境创建成功"

# 激活虚拟环境并安装依赖
echo ""
echo "📦 安装Python依赖..."
source venv/bin/activate
cd backend_python
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python依赖安装成功"

# 安装前端依赖
echo ""
echo "📦 安装前端依赖..."
cd ../frontend
npm install
echo "✅ 前端依赖安装成功"

# 创建环境变量文件
echo ""
echo "📝 配置环境变量..."
cd ../backend_python
if [ ! -f .env ]; then
    cat > .env << EOF
# 应用配置
DEBUG=true
PORT=8000

# LLM配置
DEFAULT_LLM_MODEL=gpt-4
FALLBACK_LLM_MODEL=gpt-3.5-turbo

# OpenAI API Key (必填)
OPENAI_API_KEY=your_openai_api_key_here

# 可选配置
# ANTHROPIC_API_KEY=your_anthropic_api_key
# REDIS_URL=redis://localhost:6379

# 日志配置
LOG_LEVEL=INFO
EOF
    echo "✅ 创建了 .env 文件，请编辑添加你的 API Key"
else
    echo "⚠️  .env 文件已存在，跳过创建"
fi

echo ""
echo "🎉 设置完成！"
echo ""
echo "📝 下一步："
echo "1. 编辑 backend_python/.env 文件，添加你的 OpenAI API Key"
echo "2. 启动后端: cd backend_python && source ../venv/bin/activate && uvicorn app.main:app --reload"
echo "3. 启动前端: cd frontend && npm run dev"
echo ""
echo "或者使用Docker:"
echo "docker-compose up -d"
echo ""
echo "访问: http://localhost:5173 (前端) 或 http://localhost:8000/docs (API文档)"