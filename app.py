#!/usr/bin/env python3
"""
AWS Bedrock Translation Web Application
A Flask-based web application for translating text using AWS Bedrock service.
"""

import os
import json
import boto3
import pandas as pd
import sqlite3
import time
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional, Tuple
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import tempfile
from io import BytesIO

# Import model configuration
from model_config import (
    FOUNDATION_MODELS, 
    INFERENCE_PROFILES, 
    MODEL_DISPLAY_NAMES, 
    DEFAULT_MODELS,
    PROFILE_ONLY_MODELS,
    MODEL_GROUPS,
    is_inference_profile,
    requires_inference_profile,
    get_model_display_name,
    get_corresponding_profile
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("translation_app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("BedrockTranslationApp")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}

# Global variables
bedrock_client = None
available_models = []

# Global variable to track translation progress
translation_progress = {
    'total': 0,
    'completed': 0,
    'percent': 0
}

# Initialize database for ratings
def init_db():
    """Initialize the SQLite database for storing translation ratings"""
    conn = sqlite3.connect('translation_ratings.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_text TEXT,
        translated_text TEXT,
        source_language TEXT,
        target_language TEXT,
        model_id TEXT,
        rating INTEGER,
        timestamp DATETIME
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("Initialized ratings database")

# Initialize database on startup
init_db()

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    # 将模型按组分类
    grouped_models = {}
    
    if bedrock_client is not None:
        # 按MODEL_GROUPS中的分组组织模型
        for group_name, model_ids in MODEL_GROUPS.items():
            group_models = []
            for model_id in model_ids:
                # 检查模型是否在available_models中
                model_info = next((m for m in available_models if m['id'] == model_id), None)
                if model_info:
                    group_models.append(model_info)
            
            if group_models:  # 只添加非空组
                grouped_models[group_name] = group_models
    
    return render_template('index.html', 
                          connected=(bedrock_client is not None),
                          models=available_models,
                          grouped_models=grouped_models)

@app.route('/connect', methods=['POST'])
def connect():
    """Connect to AWS Bedrock service"""
    global bedrock_client, available_models
    
    # Get credentials from form
    use_profile = 'use_profile' in request.form
    
    try:
        if use_profile:
            # Use default profile
            logger.info("Using default AWS profile")
            session = boto3.Session()
            region = session.region_name or 'us-east-1'
        else:
            # Use explicit credentials
            access_key = request.form.get('access_key', '').strip()
            secret_key = request.form.get('secret_key', '').strip()
            region = request.form.get('region', 'us-east-1').strip()
            
            if not access_key or not secret_key:
                flash('Please enter AWS credentials', 'danger')
                return redirect(url_for('index'))
            
            # 注意: 在生产环境中，应该使用更安全的方式处理凭证
            # Note: In production, you should use a more secure way to handle credentials
            logger.info(f"Using explicit credentials with region {region}")
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
        
        # Create Bedrock client
        bedrock_client = session.client('bedrock-runtime')
        
        # 初始化可用模型列表
        available_models = []
        
        # 直接使用FOUNDATION_MODELS和INFERENCE_PROFILES中定义的模型
        # 1. 添加基础模型
        for model_key, model_id in FOUNDATION_MODELS.items():
            # 跳过需要inference profile的模型
            if not requires_inference_profile(model_id):
                available_models.append({
                    'id': model_id,
                    'name': MODEL_DISPLAY_NAMES.get(model_id, model_id)
                })
        
        # 2. 添加inference profiles
        for profile_key, profile_arn in INFERENCE_PROFILES.items():
            available_models.append({
                'id': profile_arn,
                'name': MODEL_DISPLAY_NAMES.get(profile_arn, profile_arn)
            })
        
        logger.info(f"Added {len(available_models)} models from configuration")
        
        flash('Successfully connected to AWS Bedrock', 'success')
        logger.info("Successfully connected to AWS Bedrock")
        
    except Exception as e:
        error_msg = str(e)
        flash(f'Connection failed: {error_msg}', 'danger')
        logger.error(f"Error connecting to Bedrock: {error_msg}", exc_info=True)
    
    return redirect(url_for('index'))

@app.route('/translate', methods=['POST'])
def translate():
    """Translate text using AWS Bedrock"""
    if not bedrock_client:
        flash('Not connected to AWS Bedrock', 'danger')
        return redirect(url_for('index'))
    
    input_text = request.form.get('input_text', '').strip()
    model_id = request.form.get('model_id', '')
    source_lang = request.form.get('source_language', 'English')
    target_lang = request.form.get('target_language', 'Chinese')
    system_prompt = request.form.get('system_prompt', '')
    
    if not input_text:
        flash('Please enter text to translate', 'warning')
        return redirect(url_for('index'))
    
    if not model_id:
        flash('Please select a model', 'warning')
        return redirect(url_for('index'))
    
    # 检查是否是需要inference profile的模型
    if not is_inference_profile(model_id) and requires_inference_profile(model_id):
        # 尝试找到对应的inference profile
        profile_arn = get_corresponding_profile(model_id)
        if profile_arn:
            flash(f'模型 {model_id} 只能通过inference profile调用。已自动切换到对应的profile。', 'warning')
            model_id = profile_arn
        else:
            flash(f'错误: 模型 {model_id} 只能通过inference profile调用，但找不到对应的profile。请选择带有(Inference Profile)标记的模型。', 'danger')
            return redirect(url_for('index'))
    
    # Save user selections in session
    session['selected_model'] = model_id
    session['source_language'] = source_lang
    session['target_language'] = target_lang
    session['system_prompt'] = system_prompt
    
    # Replace placeholders in system prompt
    system_prompt = system_prompt.replace('{sourceLanguage}', source_lang)
    system_prompt = system_prompt.replace('{targetLanguage}', target_lang)
    
    logger.info(f"Starting translation from {source_lang} to {target_lang} using model {model_id}")
    
    try:
        # Call Bedrock API for translation
        translated_text = call_bedrock_api(model_id, system_prompt, input_text)
        
        # Store results in session for display
        session['original_text'] = input_text
        session['translated_text'] = translated_text
        
        flash('Translation completed successfully', 'success')
        logger.info("Translation completed successfully")
        
    except Exception as e:
        error_msg = str(e)
        flash(f'Translation error: {error_msg}', 'danger')
        logger.error(f"Translation error: {error_msg}", exc_info=True)
    
    return redirect(url_for('index'))

@app.route('/api/translate', methods=['POST'])
def api_translate():
    """API endpoint for translation with AJAX"""
    if not bedrock_client:
        return jsonify({'error': 'Not connected to AWS Bedrock'}), 400
    
    data = request.json or request.form
    input_text = data.get('input_text', '').strip()
    model_id = data.get('model_id', '')
    source_lang = data.get('source_language', 'English')
    target_lang = data.get('target_language', 'Chinese')
    system_prompt = data.get('system_prompt', '')
    
    if not input_text:
        return jsonify({'error': 'Please enter text to translate'}), 400
    
    if not model_id:
        return jsonify({'error': 'Please select a model'}), 400
    
    # 检查是否是需要inference profile的模型
    if not is_inference_profile(model_id) and requires_inference_profile(model_id):
        # 尝试找到对应的inference profile
        profile_arn = get_corresponding_profile(model_id)
        if profile_arn:
            logger.warning(f'模型 {model_id} 只能通过inference profile调用。已自动切换到对应的profile: {profile_arn}')
            model_id = profile_arn
        else:
            error_msg = f'错误: 模型 {model_id} 只能通过inference profile调用，但找不到对应的profile。请选择带有(Inference Profile)标记的模型。'
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
    
    # Replace placeholders in system prompt
    system_prompt = system_prompt.replace('{sourceLanguage}', source_lang)
    system_prompt = system_prompt.replace('{targetLanguage}', target_lang)
    
    logger.info(f"API: Starting translation from {source_lang} to {target_lang} using model {model_id}")
    
    try:
        # Call Bedrock API for translation
        translated_text = call_bedrock_api(model_id, system_prompt, input_text)
        
        return jsonify({
            'original_text': input_text,
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'model_id': model_id
        })
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"API Translation error: {error_msg}", exc_info=True)
        return jsonify({'error': error_msg}), 500

@app.route('/translate_file', methods=['POST'])
def translate_file():
    """Translate a file using AWS Bedrock"""
    global translation_progress
    
    if not bedrock_client:
        flash('Not connected to AWS Bedrock', 'danger')
        return redirect(url_for('index'))
    
    # Reset progress tracking
    translation_progress = {
        'total': 0,
        'completed': 0,
        'percent': 0
    }
    
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a TXT, CSV, or XLSX file', 'warning')
        return redirect(url_for('index'))
    
    model_id = request.form.get('model_id', '')
    source_lang = request.form.get('source_language', 'English')
    target_lang = request.form.get('target_language', 'Chinese')
    system_prompt = request.form.get('system_prompt', '')
    
    if not model_id:
        flash('Please select a model', 'warning')
        return redirect(url_for('index'))
    
    # 检查是否是需要inference profile的模型
    if not is_inference_profile(model_id) and requires_inference_profile(model_id):
        # 尝试找到对应的inference profile
        profile_arn = get_corresponding_profile(model_id)
        if profile_arn:
            flash(f'模型 {model_id} 只能通过inference profile调用。已自动切换到对应的profile。', 'warning')
            model_id = profile_arn
        else:
            flash(f'错误: 模型 {model_id} 只能通过inference profile调用，但找不到对应的profile。请选择带有(Inference Profile)标记的模型。', 'danger')
            return redirect(url_for('index'))
    
    # Save user selections in session
    session['selected_model'] = model_id
    session['source_language'] = source_lang
    session['target_language'] = target_lang
    session['system_prompt'] = system_prompt
    
    # Replace placeholders in system prompt
    system_prompt = system_prompt.replace('{sourceLanguage}', source_lang)
    system_prompt = system_prompt.replace('{targetLanguage}', target_lang)
    
    # Save the file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    logger.info(f"Starting batch translation of {filename} from {source_lang} to {target_lang} using model {model_id}")
    
    try:
        # Process file based on extension
        file_extension = os.path.splitext(filename)[1].lower()
        lines = []
        
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            logger.info(f"Read {len(lines)} lines from text file")
        elif file_extension == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            logger.info(f"Read {len(lines)} lines from CSV file")
        elif file_extension == '.xlsx':
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                line = ' '.join(str(cell) for cell in row if str(cell) != 'nan')
                if line.strip():
                    lines.append(line)
            logger.info(f"Read {len(lines)} lines from Excel file")
        
        # 设置总数
        total_lines = len(lines)
        translation_progress['total'] = total_lines
        logger.info(f"设置批量翻译总数: {total_lines}")
        
        # Translate each line
        translations = []
        failed_lines = []
        
        for i, line in enumerate(lines):
            if line:
                try:
                    # 添加延迟，避免API调用过于频繁
                    if i > 0:
                        time.sleep(0.5)  # 每次调用之间添加0.5秒延迟
                    
                    # 记录详细的调用参数
                    logger.info(f"Batch translation line {i+1}: model_id={model_id}, text_length={len(line)}")
                    
                    # 直接使用model_id进行翻译，与常规翻译保持一致
                    translated_text = call_bedrock_api(model_id, system_prompt, line)
                    translations.append({'original': line, 'translated': translated_text})
                    logger.info(f"Translated line {i+1}/{len(lines)}")
                except Exception as line_error:
                    # 记录失败的行，但继续处理其他行
                    error_msg = str(line_error)
                    logger.error(f"Failed to translate line {i+1}: {error_msg}")
                    translations.append({'original': line, 'translated': f"[翻译失败: {error_msg}]"})
                    failed_lines.append(i+1)
                
                # 更新进度
                translation_progress['completed'] = i + 1
                translation_progress['percent'] = int((i + 1) / total_lines * 100)
                logger.info(f"更新批量翻译进度: {i+1}/{total_lines} ({translation_progress['percent']}%)")
        
        # Generate HTML output
        html_content = generate_translation_html(translations, source_lang, target_lang)
        
        # Create a temporary file to serve
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{os.path.splitext(filename)[0]}_translated_{timestamp}.html"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 显示翻译结果摘要
        if failed_lines:
            flash(f'批量翻译完成，但有 {len(failed_lines)} 行翻译失败。失败的行号: {", ".join(map(str, failed_lines))}', 'warning')
        else:
            flash(f'批量翻译成功完成，共翻译 {len(translations)} 行文本。', 'success')
        
        logger.info(f"Batch translation completed, saved to {output_filename}")
        
        # Return the file for download
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/html'
        )
        
    except Exception as e:
        error_msg = str(e)
        flash(f'批量翻译错误: {error_msg}', 'danger')
        logger.error(f"Batch translation error: {error_msg}", exc_info=True)
        return redirect(url_for('index'))
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/progress')
def get_progress():
    """Get the current progress of batch translation"""
    global translation_progress
    logger.info(f"获取进度: {translation_progress}")
    return jsonify(translation_progress)

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    """Submit a rating for a translation"""
    data = request.json
    
    source_text = data.get('source_text')
    translated_text = data.get('translated_text')
    source_language = data.get('source_language')
    target_language = data.get('target_language')
    model_id = data.get('model_id')
    rating = data.get('rating')
    
    # Validate rating
    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid rating value'}), 400
    
    # Store rating in database
    try:
        conn = sqlite3.connect('translation_ratings.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO ratings (source_text, translated_text, source_language, target_language, model_id, rating, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (source_text, translated_text, source_language, target_language, model_id, rating, datetime.now()))
        conn.commit()
        conn.close()
        
        logger.info(f"Rating submitted: {rating}/5 for translation from {source_language} to {target_language}")
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error submitting rating: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/rating_stats', methods=['GET'])
def rating_stats():
    """Get rating statistics"""
    granularity = request.args.get('granularity', 'day')  # 'hour' or 'day'
    
    # Calculate one week ago
    one_week_ago = datetime.now() - timedelta(days=7)
    
    try:
        conn = sqlite3.connect('translation_ratings.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # 检查是否有评分数据
        c.execute('SELECT COUNT(*) as count FROM ratings')
        count = c.fetchone()['count']
        
        if count == 0:
            # 如果没有数据，返回空结果
            logger.warning("No rating data found in database")
            return jsonify({
                'time_series': [],
                'rating_distribution': [],
                'language_pairs': [],
                'models': [],
                'insights': ["暂无评分数据，请先进行一些翻译并评分"]
            })
        
        if granularity == 'hour':
            # By hour
            c.execute('''
            SELECT 
                strftime('%Y-%m-%d %H:00:00', timestamp) as time_period,
                AVG(rating) as avg_rating,
                COUNT(*) as count
            FROM ratings
            WHERE timestamp >= ?
            GROUP BY time_period
            ORDER BY time_period
            ''', (one_week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        else:
            # By day
            c.execute('''
            SELECT 
                strftime('%Y-%m-%d', timestamp) as time_period,
                AVG(rating) as avg_rating,
                COUNT(*) as count
            FROM ratings
            WHERE timestamp >= ?
            GROUP BY time_period
            ORDER BY time_period
            ''', (one_week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        
        time_series = [dict(row) for row in c.fetchall()]
        logger.info(f"Found {len(time_series)} time periods with ratings")
        
        # Get rating distribution
        c.execute('''
        SELECT 
            rating,
            COUNT(*) as count
        FROM ratings
        WHERE timestamp >= ?
        GROUP BY rating
        ORDER BY rating
        ''', (one_week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        
        rating_distribution = [dict(row) for row in c.fetchall()]
        logger.info(f"Found {len(rating_distribution)} different rating values")
        
        # Get language pair stats
        c.execute('''
        SELECT 
            source_language || ' -> ' || target_language as language_pair,
            AVG(rating) as avg_rating,
            COUNT(*) as count
        FROM ratings
        WHERE timestamp >= ?
        GROUP BY language_pair
        ORDER BY avg_rating DESC
        ''', (one_week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        
        language_pairs = [dict(row) for row in c.fetchall()]
        logger.info(f"Found {len(language_pairs)} language pairs with ratings")
        
        # Get model stats
        c.execute('''
        SELECT 
            model_id,
            AVG(rating) as avg_rating,
            COUNT(*) as count
        FROM ratings
        WHERE timestamp >= ?
        GROUP BY model_id
        ORDER BY avg_rating DESC
        ''', (one_week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        
        models = [dict(row) for row in c.fetchall()]
        logger.info(f"Found {len(models)} models with ratings")
        
        conn.close()
        
        # Generate insights
        insights = generate_insights(time_series, rating_distribution, language_pairs, models)
        
        # 记录返回的数据大小
        response_data = {
            'time_series': time_series,
            'rating_distribution': rating_distribution,
            'language_pairs': language_pairs,
            'models': models,
            'insights': insights
        }
        logger.info(f"Returning rating stats with {len(time_series)} time periods, {len(rating_distribution)} rating values, {len(language_pairs)} language pairs, {len(models)} models")
        
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"Error getting rating stats: {str(e)}", exc_info=True)
        return jsonify({
            'error': str(e),
            'time_series': [],
            'rating_distribution': [],
            'language_pairs': [],
            'models': [],
            'insights': [f"获取统计数据时出错: {str(e)}"]
        }), 500

def generate_insights(time_series, rating_distribution, language_pairs, models):
    """Generate insights from rating data"""
    insights = []
    
    # 如果没有数据，返回提示信息
    if not rating_distribution:
        return ["暂无评分数据，请先进行一些翻译并评分"]
    
    # Calculate overall average rating
    total_ratings = sum(int(item['count']) for item in rating_distribution) if rating_distribution else 0
    if total_ratings > 0:
        weighted_sum = sum(int(item['rating']) * int(item['count']) for item in rating_distribution)
        avg_rating = weighted_sum / total_ratings
        insights.append(f"总体平均评分: {avg_rating:.2f}/5.0")
        insights.append(f"总评分数量: {total_ratings}个")
    
    # Rating trend analysis
    if len(time_series) >= 2:
        try:
            first_rating = float(time_series[0]['avg_rating'])
            last_rating = float(time_series[-1]['avg_rating'])
            if last_rating > first_rating:
                insights.append(f"评分趋势: 上升 (+{last_rating - first_rating:.2f})")
            elif last_rating < first_rating:
                insights.append(f"评分趋势: 下降 ({last_rating - first_rating:.2f})")
            else:
                insights.append("评分趋势: 稳定")
        except (ValueError, TypeError) as e:
            logger.warning(f"Error calculating rating trend: {e}")
    
    # Best language pair
    if language_pairs:
        try:
            best_pair = language_pairs[0]
            insights.append(f"最佳语言对: {best_pair['language_pair']} (平均评分: {float(best_pair['avg_rating']):.2f})")
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"Error calculating best language pair: {e}")
    
    # Best model
    if models:
        try:
            best_model = models[0]
            model_name = get_model_display_name(best_model['model_id'])
            insights.append(f"最佳模型: {model_name} (平均评分: {float(best_model['avg_rating']):.2f})")
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"Error calculating best model: {e}")
    
    return insights
    
    return insights

def call_bedrock_api(model_id: str, system_prompt: str, input_text: str) -> str:
    """Call AWS Bedrock API for translation"""
    global bedrock_client
    
    logger.debug(f"Calling Bedrock API with model/profile {model_id}")
    
    # 使用model_config中的函数检查是否是inference profile
    is_profile = is_inference_profile(model_id)
    
    # 如果是推理配置文件，尝试提取基础模型ID
    base_model_id = None
    if is_profile:
        # 从ARN中提取模型ID部分
        model_parts = model_id.split('/')
        if len(model_parts) > 1:
            base_model_id = model_parts[-1]
            logger.info(f"Extracted base model ID from profile: {base_model_id}")
    
    # 特殊处理DeepSeek模型
    if 'deepseek' in model_id.lower():
        try:
            logger.info(f"Using DeepSeek-specific format for {model_id}")
            
            # DeepSeek模型使用特定的提示格式
            body = json.dumps({
                "prompt": f"<|system|>\n{system_prompt}\n<|user|>\n{input_text}\n<|assistant|>",
                "max_tokens": 2000,
                "temperature": 0.5,
                "top_p": 0.9,
                "stop": ["<|user|>"]  # 防止模型继续生成用户输入
            })
            
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body.get('generation', '').strip()
        except Exception as e:
            error_msg = str(e)
            logger.error(f"DeepSeek API error: {error_msg}", exc_info=True)
            # 继续尝试其他方法
    
    # 特殊处理Mistral模型
    if 'mistral' in model_id.lower() or 'pixtral' in model_id.lower():
        try:
            logger.info(f"Using Mistral-specific format for {model_id}")
            
            # Mistral模型使用特定的提示格式
            body = json.dumps({
                "prompt": f"<s>[INST] {system_prompt}\n\n{input_text} [/INST]",
                "max_tokens": 2000,
                "temperature": 0.5,
                "top_p": 0.9
            })
            
            # 如果是推理配置文件，尝试使用基础模型ID
            if is_profile and base_model_id:
                try:
                    logger.info(f"Trying Mistral with base model ID: {base_model_id}")
                    response = bedrock_client.invoke_model(
                        modelId=base_model_id,
                        body=body
                    )
                    
                    response_body = json.loads(response['body'].read())
                    return response_body.get('outputs', [{}])[0].get('text', '').strip()
                except Exception as base_error:
                    logger.error(f"Mistral base model error: {str(base_error)}", exc_info=True)
            
            # 尝试使用原始模型ID
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body.get('outputs', [{}])[0].get('text', '').strip()
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Mistral API error: {error_msg}", exc_info=True)
            # 继续尝试其他方法
    
    # 对于所有其他模型，首先尝试使用invoke_model API
    try:
        logger.info(f"Using invoke_model API with {'inference profile' if is_profile else 'model'}: {model_id}")
        
        # Format request based on model type
        if 'claude' in model_id.lower():
            # Claude-style request
            if 'claude-3' in model_id.lower() or 'claude-3-5' in model_id.lower() or 'claude-3-7' in model_id.lower() or 'claude-4' in model_id.lower():
                # Claude 3/3.5/3.7/4 format
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{system_prompt}\n\n{input_text}"
                        }
                    ],
                    "temperature": 0.5
                })
            else:
                # Claude 2 and earlier format
                body = json.dumps({
                    "prompt": f"\n\nHuman: {system_prompt}\n\n{input_text}\n\nAssistant:",
                    "max_tokens_to_sample": 2000,
                    "temperature": 0.5
                })
        elif 'nova' in model_id.lower():
            # Nova-style request
            body = json.dumps({
                "inputText": f"{system_prompt}\n\n{input_text}",
                "textGenerationConfig": {
                    "maxTokenCount": 2000,
                    "temperature": 0.5,
                    "topP": 0.9,
                    "stopSequences": []
                }
            })
        elif 'titan' in model_id.lower():
            # Titan-style request
            body = json.dumps({
                "inputText": f"{system_prompt}\n\n{input_text}",
                "textGenerationConfig": {
                    "maxTokenCount": 2000,
                    "temperature": 0.5,
                    "topP": 0.9
                }
            })
        elif 'llama' in model_id.lower() or 'meta' in model_id.lower():
            # Llama/Meta-style request
            body = json.dumps({
                "prompt": f"<s>[INST] {system_prompt}\n\n{input_text} [/INST]",
                "max_gen_len": 2000,
                "temperature": 0.5,
                "top_p": 0.9
            })
        else:
            # 通用回退方法
            body = json.dumps({
                "prompt": f"{system_prompt}\n\nOriginal: {input_text}\nTranslation:",
                "max_tokens": 2000,
                "temperature": 0.5
            })
        
        # 调用API
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body
        )
        
        # 解析响应
        response_body = json.loads(response['body'].read())
        
        # 根据模型类型提取结果
        if 'claude' in model_id.lower() and ('claude-3' in model_id.lower() or 'claude-3-5' in model_id.lower() or 'claude-3-7' in model_id.lower() or 'claude-4' in model_id.lower()):
            return response_body.get('content', [{}])[0].get('text', '').strip()
        elif 'claude' in model_id.lower():
            return response_body.get('completion', '').strip()
        elif 'nova' in model_id.lower() or 'titan' in model_id.lower():
            return response_body.get('results', [{}])[0].get('outputText', '').strip()
        elif 'llama' in model_id.lower() or 'meta' in model_id.lower():
            return response_body.get('generation', '').strip()
        else:
            # 通用提取方法
            if 'completion' in response_body:
                return response_body.get('completion', '').strip()
            elif 'generated_text' in response_body:
                return response_body.get('generated_text', '').strip()
            else:
                return str(response_body)  # Fallback
                
    except Exception as e:
        error_msg = str(e)
        logger.error(f"invoke_model API error: {error_msg}", exc_info=True)
        
        # 尝试使用不同的方法
        
        # 1. 尝试使用converse API
        try:
            logger.info(f"Trying converse API for {model_id}")
            
            # 使用converse API
            response = bedrock_client.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": f"{system_prompt}\n\n{input_text}"}]
                    }
                ],
                inferenceConfig={
                    "temperature": 0.5,
                    "maxTokens": 2000
                }
            )
            
            # Extract the translated text from the response
            if 'output' in response and 'message' in response['output']:
                output_message = response['output']['message']
                if 'content' in output_message:
                    for content_item in output_message['content']:
                        if 'text' in content_item:
                            return content_item['text'].strip()
            
            # Fallback if the expected structure is not found
            logger.warning(f"Unexpected converse API response structure: {response}")
            return str(response)
            
        except Exception as converse_error:
            logger.error(f"Converse API error: {str(converse_error)}", exc_info=True)
            
            # 2. 如果有基础模型ID，尝试使用基础模型ID
            if base_model_id:
                try:
                    logger.info(f"Trying with base model ID: {base_model_id}")
                    
                    # 递归调用，但使用基础模型ID
                    # 注意：这里不会导致无限递归，因为base_model_id不是inference profile
                    return call_bedrock_api(base_model_id, system_prompt, input_text)
                    
                except Exception as base_model_error:
                    logger.error(f"Base model API error: {str(base_model_error)}", exc_info=True)
            
            # 3. 尝试在INFERENCE_PROFILES中查找替代的profile
            for profile_name, profile_arn in INFERENCE_PROFILES.items():
                if profile_arn != model_id and (
                    ('claude-3-5' in model_id.lower() and 'claude-3-5' in profile_arn.lower()) or
                    ('claude-3-7' in model_id.lower() and 'claude-3-7' in profile_arn.lower()) or
                    ('claude-4' in model_id.lower() and 'claude-4' in profile_arn.lower()) or
                    ('nova' in model_id.lower() and 'nova' in profile_arn.lower()) or
                    ('deepseek' in model_id.lower() and 'deepseek' in profile_arn.lower()) or
                    ('mistral' in model_id.lower() and 'mistral' in profile_arn.lower()) or
                    ('pixtral' in model_id.lower() and 'pixtral' in profile_arn.lower())
                ):
                    try:
                        logger.info(f"Trying alternative profile: {profile_arn}")
                        return call_bedrock_api(profile_arn, system_prompt, input_text)
                    except Exception as alt_profile_error:
                        logger.error(f"Alternative profile error: {str(alt_profile_error)}", exc_info=True)
                        continue
            
            # 如果所有尝试都失败，抛出异常
            raise Exception(f"Translation failed: All API methods failed. Original error: {error_msg}")

def generate_translation_html(translations: List[Dict[str, str]], 
                             source_language: str, target_language: str) -> str:
    """Generate HTML for translation results"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Translation Results: {source_language} to {target_language}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }}
            h1 {{
                color: #333;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }}
            .translation-container {{
                display: flex;
                margin-bottom: 20px;
                border-bottom: 1px solid #eee;
                padding-bottom: 15px;
            }}
            .original, .translated {{
                flex: 1;
                padding: 10px;
            }}
            .original {{
                border-right: 1px solid #eee;
            }}
            .header {{
                font-weight: bold;
                margin-bottom: 10px;
                color: #555;
            }}
            .timestamp {{
                color: #888;
                font-size: 0.8em;
                text-align: right;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Translation Results: {source_language} to {target_language}</h1>
    """
    
    for item in translations:
        html_content += f"""
        <div class="translation-container">
            <div class="original">
                <div class="header">{source_language}</div>
                <div>{item['original']}</div>
            </div>
            <div class="translated">
                <div class="header">{target_language}</div>
                <div>{item['translated']}</div>
            </div>
        </div>
        """
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content += f"""
        <div class="timestamp">Generated on {timestamp}</div>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AWS Bedrock Translation Web Application')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the application on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the application on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    app.run(host=args.host, port=args.port, debug=args.debug)
