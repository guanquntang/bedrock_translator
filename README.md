# AWS Bedrock Translation Application

A powerful translation web application based on AWS Bedrock, supporting text translation and batch file translation with a translation quality rating system.

![AWS Bedrock Translation](https://img.shields.io/badge/AWS-Bedrock-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)

## Features

- 🌐 Translation between multiple languages
- 📊 Translation quality rating system (1-5 stars)
- 📁 Batch translation of TXT, CSV, and XLSX files
- 🤖 Support for various AWS Bedrock models, including Claude 3 series
- ⚙️ Support for AWS Bedrock inference profiles
- 📈 Detailed translation quality statistics and analysis
- 🔧 Customizable system prompts

## Requirements

- Python 3.8+ (compatible with Python 3.13)
- AWS account with access to Bedrock service
- Valid AWS credentials with permissions to use Bedrock

## Installation and Startup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/aws-bedrock-translation-app.git
   cd aws-bedrock-translation-app
   ```

2. Run the startup script
   - macOS/Linux:
     ```bash
     ./start_app.sh
     ```
   - Windows:
     ```bash
     start_app.bat
     ```

The startup script will automatically:
- Create a virtual environment (if it doesn't exist)
- Install required dependencies
- Start the application

### Optional Parameters

The startup script supports the following parameters:
```bash
./start_app.sh [port_number] [--install/-i]
```

- `port_number`: Specify a custom port (default 5001)
- `--install` or `-i`: Update dependencies

## Module Description

### Core Modules

- **app.py**: Main application containing Flask routes and core functionality
- **model_config.py**: Model configuration management, defining available AWS Bedrock models and inference profiles
- **templates/index.html**: Main page template
- **static/**: Contains CSS and JavaScript files

### Functional Modules

1. **AWS Connection Module**
   - Supports direct input of AWS credentials or using AWS profiles
   - Automatically detects available Bedrock models and inference profiles

2. **Translation Module**
   - Supports single text translation
   - Supports batch file translation
   - Uses AWS Bedrock API for high-quality translation

3. **Rating System**
   - Allows users to rate translation quality (1-5 stars)
   - Stores rating data for analysis

4. **Statistical Analysis Module**
   - Rating trend analysis
   - Language pair rating comparison
   - Model performance comparison
   - Automatic insight generation

## Usage

### AWS Connection

1. Enter your AWS credentials:
   - Enter AWS Access Key and Secret Key
   - Enter AWS Region (default is us-east-1)
   - OR check "Use default AWS profile" to use your AWS CLI default profile
   - Click "Connect to Bedrock"

### Regular Translation

1. Select source and target languages
2. Choose a translation model or inference profile
3. Customize the system prompt if needed
4. Enter text in the input field
5. Click "Translate"
6. View the original and translated text side by side
7. Rate the translation quality (1-5 stars)

### Batch Translation

1. Select source and target languages
2. Choose a translation model or inference profile
3. Customize the system prompt if needed
4. Upload a TXT, CSV, or XLSX file
   - Each line in the file will be treated as a separate text to translate
5. Click "Translate File"
6. The translated file will be automatically downloaded as an HTML file with original and translated text side by side

## Customizing the System Prompt

The system prompt can be customized to control the translation style. The prompt supports two variables:
- `{sourceLanguage}`: Automatically replaced with the selected source language
- `{targetLanguage}`: Automatically replaced with the selected target language

Example prompt:
```
You are a professional translator. Translate the text from {sourceLanguage} to {targetLanguage}. Maintain the original meaning, tone, and style as much as possible.
```

## Model Configuration

The application uses a centralized configuration file (`model_config.py`) to manage model IDs and inference profile ARNs. This makes it easy to:

1. Add new models or inference profiles
2. Update model IDs when new versions are released
3. Customize display names for models
4. Easily reference models by name rather than ID in code

To add a new model or inference profile, simply update the appropriate dictionary in `model_config.py`.

## Important Note

Before using this application, you need to update the `model_config.py` file with your own AWS account information:

1. Replace `YOUR_ACCOUNT_ID` in all inference profile ARNs with your actual AWS account ID
2. Verify that the models and inference profiles listed are available in your AWS account
3. Add or remove models based on what's available to you

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

[MIT](LICENSE)
