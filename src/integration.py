#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对接集成模块 / Integration Module
提供一键对接配置和测试功能 / Provides one-click integration setup and testing
"""

import os
import json
import time
import secrets
from pathlib import Path
from .verification import VerificationManager


class IntegrationManager:
    """对接集成管理器 / Integration Manager"""
    
    def __init__(self):
        self.default_config_path = os.path.join(os.getcwd(), 'sunny_config.json')
    
    def setup(self, config_path=None):
        """
        一键设置对接配置 / One-click setup integration configuration
        
        Args:
            config_path: 配置文件路径 / Config file path
        
        Returns:
            dict: 配置信息 / Configuration information
        """
        if not config_path:
            config_path = self.default_config_path
        
        # Generate API key
        verification_manager = VerificationManager()
        api_info = verification_manager.create_api_key(
            description='Sunny API密钥 / Sunny API Key'
        )
        
        # Create configuration
        config = {
            'version': '1.0.0',
            'app_id': api_info['app_id'],
            'api_key': api_info['api_key'],
            'secret_key': verification_manager.secret_key,
            'created_at': api_info['created_at'],
            'endpoints': {
                'verify': '/api/v1/verify',
                'encrypt': '/api/v1/encrypt',
                'decrypt': '/api/v1/decrypt'
            },
            'settings': {
                'token_expires_in': 3600,
                'max_retries': 3,
                'timeout': 30
            }
        }
        
        # Save configuration
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return {
            'config_path': config_path,
            'app_id': config['app_id'],
            'api_key': config['api_key']
        }
    
    def load_config(self, config_path=None):
        """
        加载配置 / Load configuration
        
        Args:
            config_path: 配置文件路径 / Config file path
        
        Returns:
            dict: 配置信息 / Configuration information
        """
        if not config_path:
            config_path = self.default_config_path
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在 / Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config
    
    def test_connection(self, config_path=None):
        """
        测试对接连接 / Test integration connection
        
        Args:
            config_path: 配置文件路径 / Config file path
        
        Returns:
            dict: 测试结果 / Test result
        """
        try:
            # Load configuration
            config = self.load_config(config_path)
            
            # Simulate connection test
            start_time = time.time()
            
            # Verify API key format
            if not config['api_key'].startswith('sk_'):
                return {
                    'success': False,
                    'error': 'API密钥格式无效 / Invalid API key format'
                }
            
            # Verify configuration completeness
            required_fields = ['app_id', 'api_key', 'secret_key', 'endpoints']
            for field in required_fields:
                if field not in config:
                    return {
                        'success': False,
                        'error': f'配置缺少必需字段 / Missing required field: {field}'
                    }
            
            # Test token generation
            verification_manager = VerificationManager(secret_key=config['secret_key'])
            token_result = verification_manager.generate_token(
                app_id=config['app_id'],
                expires_in=config['settings']['token_expires_in']
            )
            
            # Test token verification
            verify_result = verification_manager.verify_token(token_result['token'])
            
            if not verify_result['valid']:
                return {
                    'success': False,
                    'error': '令牌验证失败 / Token verification failed'
                }
            
            end_time = time.time()
            response_time = int((end_time - start_time) * 1000)
            
            return {
                'success': True,
                'response_time': response_time,
                'config_path': config_path or self.default_config_path,
                'app_id': config['app_id']
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_integration_example(self, language='python'):
        """
        获取集成示例代码 / Get integration example code
        
        Args:
            language: 编程语言 / Programming language
        
        Returns:
            str: 示例代码 / Example code
        """
        examples = {
            'python': '''
# Python集成示例 / Python Integration Example
import json
import requests

# 加载配置 / Load configuration
with open('sunny_config.json', 'r') as f:
    config = json.load(f)

# 生成验证令牌 / Generate verification token
def generate_token():
    from src.verification import VerificationManager
    vm = VerificationManager(secret_key=config['secret_key'])
    return vm.generate_token(app_id=config['app_id'])

# 加密数据 / Encrypt data
def encrypt_data(text):
    from src.encryption import EncryptionManager
    em = EncryptionManager()
    return em.encrypt(text=text)

# 使用示例 / Usage example
token = generate_token()
print(f"Token: {token['token']}")

encrypted = encrypt_data("Hello, Sunny!")
print(f"Encrypted: {encrypted['encrypted_text']}")
''',
            'javascript': '''
// JavaScript集成示例 / JavaScript Integration Example
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('sunny_config.json', 'utf8'));

// 使用API密钥进行请求 / Make request with API key
async function verifyToken(token) {
    const response = await fetch('https://your-api.com/api/v1/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.api_key}`
        },
        body: JSON.stringify({ token })
    });
    return await response.json();
}
''',
            'curl': '''
# cURL集成示例 / cURL Integration Example

# 加载配置中的API密钥 / Load API key from config
API_KEY=$(cat sunny_config.json | grep api_key | cut -d'"' -f4)

# 验证令牌 / Verify token
curl -X POST https://your-api.com/api/v1/verify \\
  -H "Authorization: Bearer $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"token": "YOUR_TOKEN_HERE"}'
'''
        }
        
        return examples.get(language, examples['python'])
