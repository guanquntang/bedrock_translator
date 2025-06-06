#!/bin/bash

# 翻译应用启动脚本
# 作者：AWS Q
# 版本：1.0

echo "===== AWS Bedrock 翻译应用启动脚本 ====="
echo "正在启动应用..."

# 设置端口（默认5001）
PORT=5001
if [ ! -z "$1" ] && [[ "$1" =~ ^[0-9]+$ ]]; then
    PORT=$1
    shift
fi

# 检查是否存在虚拟环境
if [ -d "venv" ]; then
    echo "检测到虚拟环境，正在激活..."
    source venv/bin/activate
    
    # 检查是否需要安装或更新依赖
    if [ "$1" == "--install" ] || [ "$1" == "-i" ]; then
        echo "安装/更新依赖..."
        pip install -r requirements.txt
    fi
    
    # 检查boto3版本
    BOTO3_VERSION=$(python -c "import boto3; print(boto3.__version__)" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "使用 boto3 版本: $BOTO3_VERSION"
        # 检查版本是否满足要求
        REQUIRED_VERSION="1.34.0"
        if python -c "from packaging import version; import boto3; exit(0 if version.parse(boto3.__version__) >= version.parse('$REQUIRED_VERSION') else 1)" 2>/dev/null; then
            echo "boto3 版本满足要求"
        else
            echo "警告: boto3 版本低于 $REQUIRED_VERSION，可能不支持 Converse API"
            echo "正在更新 boto3..."
            pip install --upgrade boto3
        fi
    else
        echo "未检测到 boto3，正在安装..."
        pip install boto3
    fi
    
    # 启动应用
    echo "启动应用，端口: $PORT..."
    python app.py --port $PORT
    
    # 退出虚拟环境
    deactivate
else
    echo "未检测到虚拟环境，正在创建..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "安装依赖..."
    pip install -r requirements.txt
    
    echo "启动应用，端口: $PORT..."
    python app.py --port $PORT
    
    # 退出虚拟环境
    deactivate
fi

echo "应用已关闭。"
