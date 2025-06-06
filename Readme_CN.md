# AWS Bedrock 翻译应用

一个基于AWS Bedrock的强大翻译Web应用，支持文本翻译和批量文件翻译，并提供翻译质量评分系统。

![AWS Bedrock Translation](https://img.shields.io/badge/AWS-Bedrock-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)

## 功能特点

- 🌐 支持多种语言之间的翻译
- 📊 翻译质量评分系统（1-5星）
- 📁 批量翻译TXT、CSV和XLSX文件
- 🤖 支持多种AWS Bedrock模型，包括Claude 3系列
- ⚙️ 支持AWS Bedrock推理配置文件
- 📈 详细的翻译质量统计和分析
- 🔧 可自定义系统提示词

## 系统要求

- Python 3.8+（兼容Python 3.13）
- AWS账户，并开通Bedrock服务
- 有效的AWS凭证，具有使用Bedrock的权限

## 安装和启动

1. 克隆仓库
   bash
  git clone https://github.com/yourusername/aws-bedrock-translation-app.git
  cd aws-bedrock-translation-app
  

2. 运行启动脚本
   - macOS/Linux:
     bash
    ./start_app.sh
    
   - Windows:
     bash
    start_app.bat
    

启动脚本将自动：
- 创建虚拟环境（如果不存在）
- 安装所需依赖
- 启动应用程序

### 可选参数

启动脚本支持以下参数：
bash
./start_app.sh [端口号] [--install/-i]

- `端口号`: 指定自定义端口（默认5001）
- `--install` 或 `-i`: 更新依赖

## 模块说明

### 核心模块

- **app.py**: 主应用程序，包含Flask路由和核心功能
- **model_config.py**: 模型配置管理，定义可用的AWS Bedrock模型和推理配置文件
- **templates/index.html**: 主页面模板
- **static/**: 包含CSS和JavaScript文件

### 功能模块

1. **AWS连接模块**
   - 支持直接输入AWS凭证或使用AWS配置文件
   - 自动检测可用的Bedrock模型和推理配置文件

2. **翻译模块**
   - 支持单文本翻译
   - 支持批量文件翻译
   - 使用AWS Bedrock API进行高质量翻译

3. **评分系统**
   - 允许用户对翻译质量进行评分（1-5星）
   - 存储评分数据用于分析

4. **统计分析模块**
   - 评分趋势分析
   - 语言对评分比较
   - 模型性能比较
   - 自动生成洞察分析

## 使用方法

### AWS连接

1. 输入您的AWS凭证：
   - 输入AWS访问密钥和秘密密钥
   - 输入AWS区域（默认为us-east-1）
   - 或勾选"使用默认AWS配置文件"以使用AWS CLI默认配置文件
   - 点击"连接到Bedrock"

### 常规翻译

1. 选择源语言和目标语言
2. 选择翻译模型或推理配置文件
3. 根据需要自定义系统提示词
4. 在输入框中输入文本
5. 点击"翻译"
6. 并排查看原文和译文
7. 为翻译质量评分（1-5星）

### 批量翻译

1. 选择源语言和目标语言
2. 选择翻译模型或推理配置文件
3. 根据需要自定义系统提示词
4. 上传TXT、CSV或XLSX文件
   - 文件中的每一行将被视为单独的文本进行翻译
5. 点击"翻译文件"
6. 翻译后的文件将自动下载为HTML文件，其中包含原文和译文

## 自定义系统提示词

系统提示词可以自定义以控制翻译风格。提示词支持两个变量：
- `{sourceLanguage}`：自动替换为所选源语言
- `{targetLanguage}`：自动替换为所选目标语言

示例提示词：

您是一位专业翻译。请将文本从{sourceLanguage}翻译成{targetLanguage}。尽可能保持原意、语气和风格。

## 模型配置

应用程序使用集中式配置文件（`model_config.py`）管理模型ID和推理配置文件ARN。这使得以下操作变得容易：

1. 添加新模型或推理配置文件
2. 在发布新版本时更新模型ID
3. 自定义模型的显示名称
4. 在代码中通过名称而不是ID轻松引用模型

要添加新模型或推理配置文件，只需更新`model_config.py`中的相应字典。

## 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 许可证

[MIT](LICENSE)
