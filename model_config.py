"""
AWS Bedrock Translation Web Application - Model Configuration

This file contains the configuration for AWS Bedrock models and inference profiles.
It provides a central place to define model IDs and inference profile ARNs.
"""

# 注意: 请根据您的AWS账户中可用的模型和推理配置文件修改以下配置
# Note: Please modify the following configuration based on the models and inference profiles available in your AWS account

# 只能通过Inference Profile调用的模型ID列表
PROFILE_ONLY_MODELS = [
    # Nova系列模型
    'amazon.nova-premier-v1:0',
    'amazon.nova-lite-v1:0',
    'amazon.nova-pro-v1:0',
    'amazon.nova-micro-v1:0',
    'us.amazon.nova-premier-v1:0',
    'us.amazon.nova-lite-v1:0',
    'us.amazon.nova-pro-v1:0',
    'us.amazon.nova-micro-v1:0',
    
    # Claude 3.5, 3.7, 4系列
    'anthropic.claude-3-5-sonnet-20240620-v1:0',
    'anthropic.claude-3-7-sonnet-20250219-v1:0',
    'us.anthropic.claude-3-5-sonnet-20240620-v1:0',
    'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
    
    # DeepSeek系列
    'deepseek.r1-v1:0',
    'us.deepseek.r1-v1:0'
]

# Foundation Models (可直接调用的模型)
FOUNDATION_MODELS = {
    # Claude 3 Models (可直接调用)
    'claude3_sonnet': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'claude3_haiku': 'anthropic.claude-3-haiku-20240307-v1:0',
    'claude3_opus': 'anthropic.claude-3-opus-20240229-v1:0',
}

# Inference Profiles - 请替换为您自己的推理配置文件ARN
# Inference Profiles - Please replace with your own inference profile ARNs
INFERENCE_PROFILES = {
    # Claude系列
    'claude3_sonnet_profile': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-sonnet-20240229-v1:0',
    'claude3_opus_profile': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-opus-20240229-v1:0',
    'claude3_haiku_profile': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0',
    'claude3_5_sonnet': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0',
    'claude3_5_sonnet_v2': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0',
    'claude3_5_haiku': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0',
    'claude3_7_sonnet': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0',
    'claude4_opus': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-opus-4-20250514-v1:0',
    'claude4_sonnet': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0',
    
    # Nova系列
    'nova_premier': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-premier-v1:0',
    'nova_lite': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-lite-v1:0',
    'nova_pro': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-pro-v1:0',
    'nova_micro': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-micro-v1:0',
    
    # Meta Llama系列
    'llama3_1_8b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-1-8b-instruct-v1:0',
    'llama3_1_70b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-1-70b-instruct-v1:0',
    'llama3_2_1b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-1b-instruct-v1:0',
    'llama3_2_3b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-3b-instruct-v1:0',
    'llama3_2_11b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-11b-instruct-v1:0',
    'llama3_2_90b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-90b-instruct-v1:0',
    'llama3_3_70b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-3-70b-instruct-v1:0',
    'llama4_scout_17b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0',
    'llama4_maverick_17b': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama4-maverick-17b-instruct-v1:0',
    
    # 其他模型
    'deepseek_r1': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.deepseek.r1-v1:0',
    'mistral_pixtral_large': 'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.mistral.pixtral-large-2502-v1:0',
}

# Display Names for Models and Profiles
MODEL_DISPLAY_NAMES = {
    # Foundation Models
    'anthropic.claude-3-sonnet-20240229-v1:0': 'Claude 3 Sonnet',
    'anthropic.claude-3-haiku-20240307-v1:0': 'Claude 3 Haiku',
    'anthropic.claude-3-opus-20240229-v1:0': 'Claude 3 Opus',
    
    # Inference Profiles - Claude系列
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-sonnet-20240229-v1:0': 'Claude 3 Sonnet (Inference Profile)',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-opus-20240229-v1:0': 'Claude 3 Opus (Inference Profile)',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0': 'Claude 3 Haiku (Inference Profile)',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0': 'Claude 3.5 Sonnet',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0': 'Claude 3.5 Sonnet v2',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0': 'Claude 3.5 Haiku',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0': 'Claude 3.7 Sonnet',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-opus-4-20250514-v1:0': 'Claude 4 Opus',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0': 'Claude 4 Sonnet',
    
    # Inference Profiles - Nova系列
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-premier-v1:0': 'Nova Premier',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-lite-v1:0': 'Nova Lite',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-pro-v1:0': 'Nova Pro',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.amazon.nova-micro-v1:0': 'Nova Micro',
    
    # Inference Profiles - Meta Llama系列
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-1-8b-instruct-v1:0': 'Llama 3.1 8B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-1-70b-instruct-v1:0': 'Llama 3.1 70B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-1b-instruct-v1:0': 'Llama 3.2 1B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-3b-instruct-v1:0': 'Llama 3.2 3B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-11b-instruct-v1:0': 'Llama 3.2 11B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-2-90b-instruct-v1:0': 'Llama 3.2 90B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama3-3-70b-instruct-v1:0': 'Llama 3.3 70B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0': 'Llama 4 Scout 17B',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.meta.llama4-maverick-17b-instruct-v1:0': 'Llama 4 Maverick 17B',
    
    # Inference Profiles - 其他模型
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.deepseek.r1-v1:0': 'DeepSeek-R1',
    'arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:inference-profile/us.mistral.pixtral-large-2502-v1:0': 'Mistral Pixtral Large',
    
    # 只能通过Inference Profile调用的模型 (用于显示警告)
    'anthropic.claude-3-7-sonnet-20250219-v1:0': 'Claude 3.7 Sonnet (需要Inference Profile)',
    'anthropic.claude-3-5-sonnet-20240620-v1:0': 'Claude 3.5 Sonnet (需要Inference Profile)',
    'amazon.nova-premier-v1:0': 'Nova Premier (需要Inference Profile)',
    'amazon.nova-lite-v1:0': 'Nova Lite (需要Inference Profile)',
    'amazon.nova-pro-v1:0': 'Nova Pro (需要Inference Profile)',
    'amazon.nova-micro-v1:0': 'Nova Micro (需要Inference Profile)',
    'deepseek.r1-v1:0': 'DeepSeek-R1 (需要Inference Profile)',
}
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama3-2-1b-instruct-v1:0': 'Llama 3.2 1B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama3-2-3b-instruct-v1:0': 'Llama 3.2 3B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama3-2-11b-instruct-v1:0': 'Llama 3.2 11B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama3-2-90b-instruct-v1:0': 'Llama 3.2 90B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama3-3-70b-instruct-v1:0': 'Llama 3.3 70B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0': 'Llama 4 Scout 17B',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.meta.llama4-maverick-17b-instruct-v1:0': 'Llama 4 Maverick 17B',
    
    # Inference Profiles - 其他模型
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.deepseek.r1-v1:0': 'DeepSeek-R1',
    'arn:aws:bedrock:us-east-1:770042106018:inference-profile/us.mistral.pixtral-large-2502-v1:0': 'Mistral Pixtral Large',
    
    # 只能通过Inference Profile调用的模型 (用于显示警告)
    'anthropic.claude-3-7-sonnet-20250219-v1:0': 'Claude 3.7 Sonnet (需要Inference Profile)',
    'anthropic.claude-3-5-sonnet-20240620-v1:0': 'Claude 3.5 Sonnet (需要Inference Profile)',
    'amazon.nova-premier-v1:0': 'Nova Premier (需要Inference Profile)',
    'amazon.nova-lite-v1:0': 'Nova Lite (需要Inference Profile)',
    'amazon.nova-pro-v1:0': 'Nova Pro (需要Inference Profile)',
    'amazon.nova-micro-v1:0': 'Nova Micro (需要Inference Profile)',
    'deepseek.r1-v1:0': 'DeepSeek-R1 (需要Inference Profile)',
}

# Default fallback models list when API listing fails
DEFAULT_MODELS = [
    # 可直接调用的模型
    {'id': FOUNDATION_MODELS['claude3_sonnet'], 'name': MODEL_DISPLAY_NAMES[FOUNDATION_MODELS['claude3_sonnet']]},
    {'id': FOUNDATION_MODELS['claude3_haiku'], 'name': MODEL_DISPLAY_NAMES[FOUNDATION_MODELS['claude3_haiku']]},
    {'id': FOUNDATION_MODELS['claude3_opus'], 'name': MODEL_DISPLAY_NAMES[FOUNDATION_MODELS['claude3_opus']]},
    
    # 注意: 以下是示例推理配置文件，请根据您的AWS账户中可用的配置文件进行修改
    # Note: The following are example inference profiles, please modify according to the profiles available in your AWS account
    
    # Inference Profiles - Claude系列
    {'id': INFERENCE_PROFILES['claude3_sonnet_profile'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_sonnet_profile']]},
    {'id': INFERENCE_PROFILES['claude3_opus_profile'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_opus_profile']]},
    {'id': INFERENCE_PROFILES['claude3_haiku_profile'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_haiku_profile']]},
    {'id': INFERENCE_PROFILES['claude3_5_sonnet'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_5_sonnet']]},
    {'id': INFERENCE_PROFILES['claude3_5_sonnet_v2'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_5_sonnet_v2']]},
    {'id': INFERENCE_PROFILES['claude3_5_haiku'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_5_haiku']]},
    {'id': INFERENCE_PROFILES['claude3_7_sonnet'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude3_7_sonnet']]},
    {'id': INFERENCE_PROFILES['claude4_opus'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude4_opus']]},
    {'id': INFERENCE_PROFILES['claude4_sonnet'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['claude4_sonnet']]},
    
    # Inference Profiles - Nova系列
    {'id': INFERENCE_PROFILES['nova_premier'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['nova_premier']]},
    {'id': INFERENCE_PROFILES['nova_lite'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['nova_lite']]},
    {'id': INFERENCE_PROFILES['nova_pro'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['nova_pro']]},
    {'id': INFERENCE_PROFILES['nova_micro'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['nova_micro']]},
    
    # 其他模型
    {'id': INFERENCE_PROFILES['deepseek_r1'], 'name': MODEL_DISPLAY_NAMES[INFERENCE_PROFILES['deepseek_r1']]},
]

def is_inference_profile(model_id):
    """Check if a model ID is an inference profile ARN"""
    return model_id.startswith('arn:aws:bedrock:')

def requires_inference_profile(model_id):
    """Check if a model requires an inference profile to be used"""
    # 检查模型ID是否在只能通过Inference Profile调用的列表中
    for profile_only_model in PROFILE_ONLY_MODELS:
        if profile_only_model in model_id:
            return True
    return False

def get_model_display_name(model_id):
    """Get the display name for a model ID or inference profile ARN"""
    return MODEL_DISPLAY_NAMES.get(model_id, model_id)

def get_corresponding_profile(model_id):
    """尝试获取与模型对应的inference profile ARN"""
    # 这里简单实现，实际应用中可能需要更复杂的映射逻辑
    for profile_name, profile_arn in INFERENCE_PROFILES.items():
        if model_id in profile_arn:
            return profile_arn
    return None

# 模型分组配置，用于在UI中组织模型
MODEL_GROUPS = {
    "Claude 3 系列": [
        FOUNDATION_MODELS['claude3_sonnet'],
        FOUNDATION_MODELS['claude3_haiku'],
        FOUNDATION_MODELS['claude3_opus'],
        INFERENCE_PROFILES['claude3_sonnet_profile'],
        INFERENCE_PROFILES['claude3_opus_profile'],
        INFERENCE_PROFILES['claude3_haiku_profile'],
    ],
    "Claude 3.5/3.7 系列": [
        INFERENCE_PROFILES['claude3_5_sonnet'],
        INFERENCE_PROFILES['claude3_5_sonnet_v2'],
        INFERENCE_PROFILES['claude3_5_haiku'],
        INFERENCE_PROFILES['claude3_7_sonnet'],
    ],
    "Claude 4 系列": [
        INFERENCE_PROFILES['claude4_opus'],
        INFERENCE_PROFILES['claude4_sonnet'],
    ],
    "Amazon Nova 系列": [
        INFERENCE_PROFILES['nova_premier'],
        INFERENCE_PROFILES['nova_lite'],
        INFERENCE_PROFILES['nova_pro'],
        INFERENCE_PROFILES['nova_micro'],
    ],
    "Meta Llama 系列": [
        INFERENCE_PROFILES['llama3_1_8b'],
        INFERENCE_PROFILES['llama3_1_70b'],
        INFERENCE_PROFILES['llama3_2_1b'],
        INFERENCE_PROFILES['llama3_2_3b'],
        INFERENCE_PROFILES['llama3_2_11b'],
        INFERENCE_PROFILES['llama3_2_90b'],
        INFERENCE_PROFILES['llama3_3_70b'],
        INFERENCE_PROFILES['llama4_scout_17b'],
        INFERENCE_PROFILES['llama4_maverick_17b'],
    ],
    "其他模型": [
        INFERENCE_PROFILES['deepseek_r1'],
        INFERENCE_PROFILES['mistral_pixtral_large'],
    ]
}

def is_inference_profile(model_id):
    """Check if a model ID is an inference profile ARN"""
    return model_id.startswith('arn:aws:bedrock:')

def requires_inference_profile(model_id):
    """Check if a model requires an inference profile to be used"""
    # 检查模型ID是否在只能通过Inference Profile调用的列表中
    for profile_only_model in PROFILE_ONLY_MODELS:
        if profile_only_model in model_id:
            return True
    return False

def get_model_display_name(model_id):
    """Get the display name for a model ID or inference profile ARN"""
    return MODEL_DISPLAY_NAMES.get(model_id, model_id)

def get_corresponding_profile(model_id):
    """尝试获取与模型对应的inference profile ARN"""
    # 这里简单实现，实际应用中可能需要更复杂的映射逻辑
    for profile_name, profile_arn in INFERENCE_PROFILES.items():
        if model_id in profile_arn:
            return profile_arn
    return None
    "Meta Llama 系列": [
        INFERENCE_PROFILES['llama3_1_8b'],
        INFERENCE_PROFILES['llama3_1_70b'],
        INFERENCE_PROFILES['llama3_2_1b'],
        INFERENCE_PROFILES['llama3_2_3b'],
        INFERENCE_PROFILES['llama3_2_11b'],
        INFERENCE_PROFILES['llama3_2_90b'],
        INFERENCE_PROFILES['llama3_3_70b'],
        INFERENCE_PROFILES['llama4_scout_17b'],
        INFERENCE_PROFILES['llama4_maverick_17b'],
    ],
    "其他模型": [
        INFERENCE_PROFILES['deepseek_r1'],
        INFERENCE_PROFILES['mistral_pixtral_large'],
    ]
}
