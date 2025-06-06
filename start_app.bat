@echo off
REM 翻译应用启动脚本
REM 作者：AWS Q
REM 版本：1.0

echo ===== AWS Bedrock 翻译应用启动脚本 =====
echo 正在启动应用...

REM 设置端口（默认5001）
set PORT=5001
if not "%~1"=="" (
    echo %~1 | findstr /r "^[0-9]*$" >nul
    if not errorlevel 1 (
        set PORT=%~1
        shift
    )
)

REM 检查是否存在虚拟环境
if exist venv\ (
    echo 检测到虚拟环境，正在激活...
    call venv\Scripts\activate.bat
    
    REM 检查是否需要安装或更新依赖
    if "%~1"=="--install" (
        echo 安装/更新依赖...
        pip install -r requirements.txt
    ) else if "%~1"=="-i" (
        echo 安装/更新依赖...
        pip install -r requirements.txt
    )
    
    REM 检查boto3版本
    python -c "import boto3; print(boto3.__version__)" >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=*" %%i in ('python -c "import boto3; print(boto3.__version__)"') do set BOTO3_VERSION=%%i
        echo 使用 boto3 版本: %BOTO3_VERSION%
        
        REM 检查版本是否满足要求
        set REQUIRED_VERSION=1.34.0
        python -c "from packaging import version; import boto3; exit(0 if version.parse(boto3.__version__) >= version.parse('%REQUIRED_VERSION%') else 1)" >nul 2>&1
        if not errorlevel 1 (
            echo boto3 版本满足要求
        ) else (
            echo 警告: boto3 版本低于 %REQUIRED_VERSION%，可能不支持 Converse API
            echo 正在更新 boto3...
            pip install --upgrade boto3
        )
    ) else (
        echo 未检测到 boto3，正在安装...
        pip install boto3
    )
    
    REM 启动应用
    echo 启动应用，端口: %PORT%...
    python app.py --port %PORT%
    
    REM 退出虚拟环境
    call deactivate
) else (
    echo 未检测到虚拟环境，正在创建...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo 安装依赖...
    pip install -r requirements.txt
    
    echo 启动应用，端口: %PORT%...
    python app.py --port %PORT%
    
    REM 退出虚拟环境
    call deactivate
)

echo 应用已关闭。
pause
