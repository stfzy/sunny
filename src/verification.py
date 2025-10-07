#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络验证模块 / Network Verification Module
提供基于令牌的网络验证功能 / Provides token-based network verification
"""

import time
import hmac
import hashlib
import secrets
import json
import base64
from datetime import datetime, timedelta


class VerificationManager:
    """网络验证管理器 / Network Verification Manager"""
    
    def __init__(self, secret_key=None):
        """
        初始化验证管理器 / Initialize verification manager
        
        Args:
            secret_key: 密钥，用于签名令牌 / Secret key for signing tokens
        """
        self.secret_key = secret_key or self._generate_secret_key()
    
    def _generate_secret_key(self):
        """生成密钥 / Generate secret key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
    
    def _generate_token_data(self, app_id, expires_in):
        """
        生成令牌数据 / Generate token data
        
        Args:
            app_id: 应用ID / Application ID
            expires_in: 过期时间（秒）/ Expiration time in seconds
        
        Returns:
            dict: 令牌数据 / Token data
        """
        now = datetime.now()
        expires_at = now + timedelta(seconds=expires_in)
        
        return {
            'app_id': app_id,
            'issued_at': int(now.timestamp()),
            'expires_at': int(expires_at.timestamp()),
            'nonce': secrets.token_hex(16)
        }
    
    def _sign_token(self, token_data):
        """
        签名令牌 / Sign token
        
        Args:
            token_data: 令牌数据 / Token data
        
        Returns:
            str: 签名 / Signature
        """
        message = json.dumps(token_data, sort_keys=True).encode('utf-8')
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _verify_signature(self, token_data, signature):
        """
        验证签名 / Verify signature
        
        Args:
            token_data: 令牌数据 / Token data
            signature: 签名 / Signature
        
        Returns:
            bool: 签名是否有效 / Whether signature is valid
        """
        expected_signature = self._sign_token(token_data)
        return hmac.compare_digest(signature, expected_signature)
    
    def generate_token(self, app_id=None, expires_in=3600):
        """
        一键生成验证令牌 / One-click generate verification token
        
        Args:
            app_id: 应用ID / Application ID
            expires_in: 过期时间（秒）/ Expiration time in seconds
        
        Returns:
            dict: 包含令牌信息的字典 / Dictionary containing token information
        """
        if not app_id:
            app_id = f"app_{secrets.token_hex(8)}"
        
        # Generate token data
        token_data = self._generate_token_data(app_id, expires_in)
        
        # Sign token
        signature = self._sign_token(token_data)
        
        # Combine token data and signature
        token_payload = {
            'data': token_data,
            'signature': signature
        }
        
        # Encode token
        token = base64.urlsafe_b64encode(
            json.dumps(token_payload).encode('utf-8')
        ).decode('utf-8')
        
        return {
            'app_id': app_id,
            'token': token,
            'expires_at': datetime.fromtimestamp(token_data['expires_at']).isoformat(),
            'secret_key': self.secret_key
        }
    
    def verify_token(self, token):
        """
        一键验证令牌 / One-click verify token
        
        Args:
            token: 令牌字符串 / Token string
        
        Returns:
            dict: 验证结果 / Verification result
        """
        try:
            # Decode token
            token_json = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            token_payload = json.loads(token_json)
            
            token_data = token_payload['data']
            signature = token_payload['signature']
            
            # Verify signature
            if not self._verify_signature(token_data, signature):
                return {
                    'valid': False,
                    'error': '签名验证失败 / Signature verification failed'
                }
            
            # Check expiration
            now = int(time.time())
            if now > token_data['expires_at']:
                return {
                    'valid': False,
                    'error': '令牌已过期 / Token expired'
                }
            
            return {
                'valid': True,
                'app_id': token_data['app_id'],
                'issued_at': datetime.fromtimestamp(token_data['issued_at']).isoformat(),
                'expires_at': datetime.fromtimestamp(token_data['expires_at']).isoformat()
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': f'令牌解析失败 / Token parsing failed: {str(e)}'
            }
    
    def create_api_key(self, app_id=None, description=None):
        """
        创建API密钥 / Create API key
        
        Args:
            app_id: 应用ID / Application ID
            description: 描述 / Description
        
        Returns:
            dict: API密钥信息 / API key information
        """
        if not app_id:
            app_id = f"app_{secrets.token_hex(8)}"
        
        api_key = f"sk_{secrets.token_urlsafe(32)}"
        
        return {
            'app_id': app_id,
            'api_key': api_key,
            'description': description or 'API密钥 / API Key',
            'created_at': datetime.now().isoformat()
        }
