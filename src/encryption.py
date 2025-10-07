#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密模块 / Encryption Module
提供AES-256高强度加密功能 / Provides AES-256 high-strength encryption
"""

import os
import base64
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class EncryptionManager:
    """加密管理器 / Encryption Manager"""
    
    def __init__(self):
        self.backend = default_backend()
        self.block_size = 128  # AES block size in bits
    
    def generate_key(self):
        """生成随机加密密钥 / Generate random encryption key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
    
    def _pad_data(self, data):
        """填充数据到块大小 / Pad data to block size"""
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data
    
    def _unpad_data(self, padded_data):
        """移除填充 / Remove padding"""
        unpadder = padding.PKCS7(self.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data
    
    def _encrypt_bytes(self, data, key):
        """加密字节数据 / Encrypt bytes data"""
        # Decode the key
        key_bytes = base64.urlsafe_b64decode(key.encode('utf-8'))
        
        # Generate random IV
        iv = secrets.token_bytes(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=self.backend
        )
        
        # Encrypt data
        encryptor = cipher.encryptor()
        padded_data = self._pad_data(data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and encrypted data
        return iv + encrypted_data
    
    def _decrypt_bytes(self, encrypted_data, key):
        """解密字节数据 / Decrypt bytes data"""
        # Decode the key
        key_bytes = base64.urlsafe_b64decode(key.encode('utf-8'))
        
        # Extract IV and encrypted data
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=self.backend
        )
        
        # Decrypt data
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        data = self._unpad_data(padded_data)
        
        return data
    
    def encrypt(self, file_path=None, text=None, output_path=None, key=None):
        """
        一键加密 / One-click encryption
        
        Args:
            file_path: 文件路径 / File path
            text: 文本内容 / Text content
            output_path: 输出路径 / Output path
            key: 加密密钥（可选）/ Encryption key (optional)
        
        Returns:
            dict: 包含加密结果的字典 / Dictionary containing encryption results
        """
        if not file_path and not text:
            raise ValueError("必须提供文件路径或文本 / Must provide file path or text")
        
        # Generate key if not provided
        if not key:
            key = self.generate_key()
        
        result = {'key': key}
        
        if file_path:
            # Read file
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Encrypt
            encrypted_data = self._encrypt_bytes(data, key)
            
            # Write to output file
            if not output_path:
                output_path = f"{file_path}.enc"
            
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            result['output_path'] = output_path
        
        elif text:
            # Encrypt text
            data = text.encode('utf-8')
            encrypted_data = self._encrypt_bytes(data, key)
            encrypted_text = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            result['encrypted_text'] = encrypted_text
        
        return result
    
    def decrypt(self, file_path=None, text=None, output_path=None, key=None):
        """
        一键解密 / One-click decryption
        
        Args:
            file_path: 文件路径 / File path
            text: 加密文本 / Encrypted text
            output_path: 输出路径 / Output path
            key: 解密密钥 / Decryption key
        
        Returns:
            dict: 包含解密结果的字典 / Dictionary containing decryption results
        """
        if not file_path and not text:
            raise ValueError("必须提供文件路径或文本 / Must provide file path or text")
        
        if not key:
            raise ValueError("必须提供解密密钥 / Must provide decryption key")
        
        result = {}
        
        if file_path:
            # Read encrypted file
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            data = self._decrypt_bytes(encrypted_data, key)
            
            # Write to output file
            if not output_path:
                if file_path.endswith('.enc'):
                    output_path = file_path[:-4]
                else:
                    output_path = f"{file_path}.dec"
            
            with open(output_path, 'wb') as f:
                f.write(data)
            
            result['output_path'] = output_path
        
        elif text:
            # Decrypt text
            encrypted_data = base64.urlsafe_b64decode(text.encode('utf-8'))
            data = self._decrypt_bytes(encrypted_data, key)
            decrypted_text = data.decode('utf-8')
            result['decrypted_text'] = decrypted_text
        
        return result
