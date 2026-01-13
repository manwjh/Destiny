#!/usr/bin/env python3
"""
测试环境变量配置
"""
import os
from pathlib import Path

# 加载.env文件
env_file = Path(__file__).parent / '.env'

print("=" * 60)
print("环境变量配置测试")
print("=" * 60)

if env_file.exists():
    print(f"✅ .env 文件存在: {env_file}")
    print("\n读取配置内容:\n")
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if 'API_KEY' in line:
                    # 隐藏API密钥
                    key, value = line.split('=', 1)
                    print(f"  {key}={value[:20]}..." if len(value) > 20 else f"  {line}")
                else:
                    print(f"  {line}")
    
    print("\n" + "=" * 60)
    print("配置说明:")
    print("=" * 60)
    print("""
1. LLM配置已保存在 .env 文件中
2. 应用启动时会自动加载这些环境变量
3. 使用 pydantic-settings 管理配置
4. LiteLLM 会使用这些配置调用自定义API

启动应用命令:
  cd backend_python
  pip install -r requirements.txt  # 首次运行需要安装依赖
  python -m app.main               # 或 uvicorn app.main:app --reload
    """)
else:
    print(f"❌ .env 文件不存在: {env_file}")

print("=" * 60)
