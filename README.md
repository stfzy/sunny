# Sunny - 网络验证和加密工具

一款高性能网络验证+高强度一键加密对接验证的程序

## 功能特性 / Features

- 🔐 **一键加密** - 基于AES-256的高强度加密，支持文件和文本加密
- 🔑 **网络验证** - 基于令牌的网络验证系统，安全可靠
- 🚀 **一键对接** - 快速配置和集成，支持多种编程语言
- ⚡ **高性能** - 优化的加密和验证算法，响应迅速

## 安装 / Installation

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/stfzy/sunny.git
cd sunny

# 安装依赖 / Install dependencies
pip install -r requirements.txt
```

## 快速开始 / Quick Start

### 1. 一键加密文件 / One-click File Encryption

```bash
# 加密文件 / Encrypt file
python sunny.py encrypt --file myfile.txt

# 输出示例 / Output example:
# ✓ 加密成功 / Encryption successful
# 密钥 / Key: xxxxx
# 输出文件 / Output file: myfile.txt.enc
```

### 2. 一键解密文件 / One-click File Decryption

```bash
# 解密文件 / Decrypt file
python sunny.py decrypt --file myfile.txt.enc --key YOUR_KEY
```

### 3. 加密文本 / Encrypt Text

```bash
# 加密文本 / Encrypt text
python sunny.py encrypt --text "Hello, World!"
```

### 4. 生成验证令牌 / Generate Verification Token

```bash
# 生成令牌 / Generate token
python sunny.py verify --generate --app-id myapp

# 输出示例 / Output example:
# ✓ 令牌生成成功 / Token generated successfully
# 应用ID / App ID: myapp
# 令牌 / Token: xxxxx
# 过期时间 / Expires: 2025-01-01T12:00:00
```

### 5. 验证令牌 / Verify Token

```bash
# 验证令牌 / Verify token
python sunny.py verify --token YOUR_TOKEN
```

### 6. 一键对接配置 / One-click Integration Setup

```bash
# 设置对接配置 / Setup integration
python sunny.py integrate --setup

# 输出示例 / Output example:
# ✓ 对接配置完成 / Integration setup completed
# 配置文件 / Config file: sunny_config.json
# API密钥 / API Key: sk_xxxxx
```

### 7. 测试对接连接 / Test Integration Connection

```bash
# 测试连接 / Test connection
python sunny.py integrate --test
```

## 使用示例 / Usage Examples

### Python集成示例 / Python Integration Example

```python
from src.encryption import EncryptionManager
from src.verification import VerificationManager

# 加密管理 / Encryption management
em = EncryptionManager()
result = em.encrypt(text="Hello, Sunny!")
print(f"Encrypted: {result['encrypted_text']}")
print(f"Key: {result['key']}")

# 解密 / Decryption
decrypted = em.decrypt(text=result['encrypted_text'], key=result['key'])
print(f"Decrypted: {decrypted['decrypted_text']}")

# 网络验证 / Network verification
vm = VerificationManager()
token_info = vm.generate_token(app_id="myapp")
print(f"Token: {token_info['token']}")

# 验证令牌 / Verify token
verify_result = vm.verify_token(token_info['token'])
print(f"Valid: {verify_result['valid']}")
```

## 命令行参数 / Command Line Arguments

### 加密命令 / Encrypt Command

```bash
python sunny.py encrypt [选项 / options]
  --file FILE       要加密的文件路径 / File to encrypt
  --text TEXT       要加密的文本 / Text to encrypt
  --output OUTPUT   输出文件路径 / Output file path
  --key KEY         加密密钥（可选）/ Encryption key (optional)
```

### 解密命令 / Decrypt Command

```bash
python sunny.py decrypt [选项 / options]
  --file FILE       要解密的文件路径 / File to decrypt
  --text TEXT       要解密的文本 / Text to decrypt
  --output OUTPUT   输出文件路径 / Output file path
  --key KEY         解密密钥（必需）/ Decryption key (required)
```

### 验证命令 / Verify Command

```bash
python sunny.py verify [选项 / options]
  --generate        生成验证令牌 / Generate verification token
  --token TOKEN     验证令牌 / Token to verify
  --app-id APP_ID   应用ID / Application ID
  --expires EXPIRES 令牌过期时间（秒）/ Token expiration time (seconds)
```

### 对接命令 / Integration Command

```bash
python sunny.py integrate [选项 / options]
  --setup           设置对接配置 / Setup integration
  --test            测试对接连接 / Test integration connection
  --config CONFIG   配置文件路径 / Config file path
```

## 配置文件 / Configuration File

使用 `python sunny.py integrate --setup` 命令会生成 `sunny_config.json` 配置文件：

```json
{
  "version": "1.0.0",
  "app_id": "app_xxxxxxxx",
  "api_key": "sk_xxxxxxxxxxxxxxxx",
  "secret_key": "xxxxxxxxxxxxxxxx",
  "endpoints": {
    "verify": "/api/v1/verify",
    "encrypt": "/api/v1/encrypt",
    "decrypt": "/api/v1/decrypt"
  },
  "settings": {
    "token_expires_in": 3600,
    "max_retries": 3,
    "timeout": 30
  }
}
```

## 安全说明 / Security Notes

- 🔒 使用AES-256加密算法，行业标准级安全
- 🔑 密钥采用安全随机生成器生成
- ⏰ 令牌支持过期时间设置，默认1小时
- ✍️ 令牌使用HMAC-SHA256签名验证

## 技术栈 / Tech Stack

- Python 3.7+
- cryptography - 加密库
- HMAC-SHA256 - 令牌签名
- AES-256-CBC - 数据加密

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

## 联系方式 / Contact

如有问题或建议，请提交 Issue。
