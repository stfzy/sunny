#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sunny - 高性能网络验证+高强度一键加密对接验证的程序
High-performance network verification and encryption program
"""

import argparse
import sys
from src.encryption import EncryptionManager
from src.verification import VerificationManager
from src.integration import IntegrationManager


def main():
    """主程序入口 / Main program entry point"""
    parser = argparse.ArgumentParser(
        description='Sunny - 网络验证和加密工具 / Network Verification and Encryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例 / Usage Examples:
  # 一键加密文件 / One-click file encryption
  python sunny.py encrypt --file myfile.txt
  
  # 一键解密文件 / One-click file decryption
  python sunny.py decrypt --file myfile.txt.enc
  
  # 生成验证令牌 / Generate verification token
  python sunny.py verify --generate
  
  # 验证令牌 / Verify token
  python sunny.py verify --token YOUR_TOKEN
  
  # 一键对接配置 / One-click integration setup
  python sunny.py integrate --setup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令 / Available commands')
    
    # 加密命令 / Encryption command
    encrypt_parser = subparsers.add_parser('encrypt', help='加密文件或文本 / Encrypt file or text')
    encrypt_parser.add_argument('--file', type=str, help='要加密的文件路径 / File to encrypt')
    encrypt_parser.add_argument('--text', type=str, help='要加密的文本 / Text to encrypt')
    encrypt_parser.add_argument('--output', type=str, help='输出文件路径 / Output file path')
    encrypt_parser.add_argument('--key', type=str, help='加密密钥（可选）/ Encryption key (optional)')
    
    # 解密命令 / Decryption command
    decrypt_parser = subparsers.add_parser('decrypt', help='解密文件或文本 / Decrypt file or text')
    decrypt_parser.add_argument('--file', type=str, help='要解密的文件路径 / File to decrypt')
    decrypt_parser.add_argument('--text', type=str, help='要解密的文本 / Text to decrypt')
    decrypt_parser.add_argument('--output', type=str, help='输出文件路径 / Output file path')
    decrypt_parser.add_argument('--key', type=str, required=True, help='解密密钥 / Decryption key')
    
    # 网络验证命令 / Network verification command
    verify_parser = subparsers.add_parser('verify', help='网络验证 / Network verification')
    verify_parser.add_argument('--generate', action='store_true', help='生成验证令牌 / Generate verification token')
    verify_parser.add_argument('--token', type=str, help='验证令牌 / Token to verify')
    verify_parser.add_argument('--app-id', type=str, help='应用ID / Application ID')
    verify_parser.add_argument('--expires', type=int, default=3600, help='令牌过期时间（秒）/ Token expiration time (seconds)')
    
    # 一键对接命令 / One-click integration command
    integrate_parser = subparsers.add_parser('integrate', help='一键对接配置 / One-click integration')
    integrate_parser.add_argument('--setup', action='store_true', help='设置对接配置 / Setup integration')
    integrate_parser.add_argument('--test', action='store_true', help='测试对接连接 / Test integration connection')
    integrate_parser.add_argument('--config', type=str, help='配置文件路径 / Config file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'encrypt':
            encryption_manager = EncryptionManager()
            result = encryption_manager.encrypt(
                file_path=args.file,
                text=args.text,
                output_path=args.output,
                key=args.key
            )
            print(f"✓ 加密成功 / Encryption successful")
            print(f"密钥 / Key: {result['key']}")
            if result.get('output_path'):
                print(f"输出文件 / Output file: {result['output_path']}")
            if result.get('encrypted_text'):
                print(f"加密文本 / Encrypted text: {result['encrypted_text']}")
        
        elif args.command == 'decrypt':
            encryption_manager = EncryptionManager()
            result = encryption_manager.decrypt(
                file_path=args.file,
                text=args.text,
                output_path=args.output,
                key=args.key
            )
            print(f"✓ 解密成功 / Decryption successful")
            if result.get('output_path'):
                print(f"输出文件 / Output file: {result['output_path']}")
            if result.get('decrypted_text'):
                print(f"解密文本 / Decrypted text: {result['decrypted_text']}")
        
        elif args.command == 'verify':
            verification_manager = VerificationManager()
            if args.generate:
                result = verification_manager.generate_token(
                    app_id=args.app_id,
                    expires_in=args.expires
                )
                print(f"✓ 令牌生成成功 / Token generated successfully")
                print(f"应用ID / App ID: {result['app_id']}")
                print(f"令牌 / Token: {result['token']}")
                print(f"过期时间 / Expires: {result['expires_at']}")
            elif args.token:
                result = verification_manager.verify_token(args.token)
                if result['valid']:
                    print(f"✓ 令牌验证成功 / Token verified successfully")
                    print(f"应用ID / App ID: {result['app_id']}")
                    print(f"过期时间 / Expires at: {result['expires_at']}")
                else:
                    print(f"✗ 令牌验证失败 / Token verification failed: {result['error']}")
                    return 1
            else:
                verify_parser.print_help()
        
        elif args.command == 'integrate':
            integration_manager = IntegrationManager()
            if args.setup:
                result = integration_manager.setup(config_path=args.config)
                print(f"✓ 对接配置完成 / Integration setup completed")
                print(f"配置文件 / Config file: {result['config_path']}")
                print(f"API密钥 / API Key: {result['api_key']}")
            elif args.test:
                result = integration_manager.test_connection(config_path=args.config)
                if result['success']:
                    print(f"✓ 连接测试成功 / Connection test successful")
                    print(f"响应时间 / Response time: {result['response_time']}ms")
                else:
                    print(f"✗ 连接测试失败 / Connection test failed: {result['error']}")
                    return 1
            else:
                integrate_parser.print_help()
        
        return 0
    
    except Exception as e:
        print(f"✗ 错误 / Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
