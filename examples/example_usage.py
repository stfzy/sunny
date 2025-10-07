#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sunny 使用示例 / Sunny Usage Examples
演示如何使用Sunny进行加密、验证和对接 / Demonstrates how to use Sunny for encryption, verification, and integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.encryption import EncryptionManager
from src.verification import VerificationManager
from src.integration import IntegrationManager


def example_encryption():
    """加密示例 / Encryption example"""
    print("=" * 60)
    print("加密示例 / Encryption Example")
    print("=" * 60)
    
    em = EncryptionManager()
    
    # 加密文本 / Encrypt text
    text = "Hello, Sunny! 你好，世界！"
    print(f"\n原始文本 / Original text: {text}")
    
    result = em.encrypt(text=text)
    print(f"加密文本 / Encrypted text: {result['encrypted_text'][:50]}...")
    print(f"密钥 / Key: {result['key']}")
    
    # 解密文本 / Decrypt text
    decrypted = em.decrypt(text=result['encrypted_text'], key=result['key'])
    print(f"解密文本 / Decrypted text: {decrypted['decrypted_text']}")
    print()


def example_verification():
    """验证示例 / Verification example"""
    print("=" * 60)
    print("网络验证示例 / Network Verification Example")
    print("=" * 60)
    
    vm = VerificationManager()
    
    # 生成令牌 / Generate token
    print("\n生成令牌 / Generating token...")
    token_info = vm.generate_token(app_id="example_app", expires_in=3600)
    print(f"应用ID / App ID: {token_info['app_id']}")
    print(f"令牌 / Token: {token_info['token'][:50]}...")
    print(f"过期时间 / Expires at: {token_info['expires_at']}")
    
    # 验证令牌 / Verify token
    print("\n验证令牌 / Verifying token...")
    verify_result = vm.verify_token(token_info['token'])
    print(f"验证结果 / Verification result: {verify_result['valid']}")
    if verify_result['valid']:
        print(f"应用ID / App ID: {verify_result['app_id']}")
        print(f"签发时间 / Issued at: {verify_result['issued_at']}")
        print(f"过期时间 / Expires at: {verify_result['expires_at']}")
    print()


def example_integration():
    """对接集成示例 / Integration example"""
    print("=" * 60)
    print("对接集成示例 / Integration Example")
    print("=" * 60)
    
    im = IntegrationManager()
    
    # 设置配置 / Setup configuration
    print("\n设置对接配置 / Setting up integration...")
    config_path = '/tmp/sunny_config_example.json'
    setup_result = im.setup(config_path=config_path)
    print(f"配置文件 / Config file: {setup_result['config_path']}")
    print(f"应用ID / App ID: {setup_result['app_id']}")
    print(f"API密钥 / API Key: {setup_result['api_key'][:20]}...")
    
    # 测试连接 / Test connection
    print("\n测试对接连接 / Testing integration connection...")
    test_result = im.test_connection(config_path=config_path)
    if test_result['success']:
        print(f"✓ 连接测试成功 / Connection test successful")
        print(f"响应时间 / Response time: {test_result['response_time']}ms")
    else:
        print(f"✗ 连接测试失败 / Connection test failed: {test_result['error']}")
    
    # 清理示例文件 / Clean up example file
    if os.path.exists(config_path):
        os.remove(config_path)
    print()


def example_file_encryption():
    """文件加密示例 / File encryption example"""
    print("=" * 60)
    print("文件加密示例 / File Encryption Example")
    print("=" * 60)
    
    em = EncryptionManager()
    
    # 创建测试文件 / Create test file
    test_file = '/tmp/sunny_test_file.txt'
    test_content = "这是一个测试文件\nThis is a test file\n包含多行内容\nWith multiple lines"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"\n创建测试文件 / Created test file: {test_file}")
    print(f"原始内容 / Original content:\n{test_content}")
    
    # 加密文件 / Encrypt file
    print("\n加密文件 / Encrypting file...")
    encrypt_result = em.encrypt(file_path=test_file)
    print(f"加密文件 / Encrypted file: {encrypt_result['output_path']}")
    print(f"密钥 / Key: {encrypt_result['key']}")
    
    # 解密文件 / Decrypt file
    print("\n解密文件 / Decrypting file...")
    decrypt_result = em.decrypt(file_path=encrypt_result['output_path'], key=encrypt_result['key'])
    print(f"解密文件 / Decrypted file: {decrypt_result['output_path']}")
    
    # 验证内容 / Verify content
    with open(decrypt_result['output_path'], 'r', encoding='utf-8') as f:
        decrypted_content = f.read()
    
    if decrypted_content == test_content:
        print("✓ 文件加密解密验证成功 / File encryption/decryption verification successful")
    else:
        print("✗ 文件加密解密验证失败 / File encryption/decryption verification failed")
    
    # 清理测试文件 / Clean up test files
    for filepath in [test_file, encrypt_result['output_path'], decrypt_result['output_path']]:
        if os.path.exists(filepath):
            os.remove(filepath)
    print()


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Sunny 使用示例 / Sunny Usage Examples" + " " * 11 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # 运行所有示例 / Run all examples
    example_encryption()
    example_verification()
    example_integration()
    example_file_encryption()
    
    print("=" * 60)
    print("所有示例运行完成 / All examples completed")
    print("=" * 60)
