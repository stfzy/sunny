# Sunny 快速入门指南 / Quick Start Guide

## 安装 / Installation

```bash
# 1. 克隆仓库 / Clone repository
git clone https://github.com/stfzy/sunny.git
cd sunny

# 2. 安装依赖 / Install dependencies
pip install -r requirements.txt
```

## 5分钟快速上手 / 5-Minute Quick Start

### 场景1: 文件加密 / Scenario 1: File Encryption

```bash
# 创建一个测试文件 / Create a test file
echo "机密数据" > secret.txt

# 一键加密 / One-click encrypt
python sunny.py encrypt --file secret.txt

# 输出 / Output:
# ✓ 加密成功 / Encryption successful
# 密钥 / Key: YOUR_ENCRYPTION_KEY
# 输出文件 / Output file: secret.txt.enc

# 保存密钥，然后解密 / Save the key, then decrypt
python sunny.py decrypt --file secret.txt.enc --key YOUR_ENCRYPTION_KEY

# 验证文件内容 / Verify file content
cat secret.txt
```

### 场景2: 网络验证 / Scenario 2: Network Verification

```bash
# 生成应用验证令牌 / Generate app verification token
python sunny.py verify --generate --app-id myapp --expires 7200

# 输出 / Output:
# ✓ 令牌生成成功 / Token generated successfully
# 应用ID / App ID: myapp
# 令牌 / Token: YOUR_TOKEN
# 过期时间 / Expires: 2025-XX-XX XX:XX:XX

# 验证令牌 / Verify token
python sunny.py verify --token YOUR_TOKEN
```

### 场景3: 应用对接 / Scenario 3: Application Integration

```bash
# 一键设置对接配置 / One-click setup integration
python sunny.py integrate --setup

# 输出 / Output:
# ✓ 对接配置完成 / Integration setup completed
# 配置文件 / Config file: sunny_config.json
# API密钥 / API Key: sk_xxxxx

# 测试对接连接 / Test integration
python sunny.py integrate --test

# 输出 / Output:
# ✓ 连接测试成功 / Connection test successful
# 响应时间 / Response time: 0ms
```

## 实际应用案例 / Real-World Use Cases

### 案例1: 保护配置文件 / Use Case 1: Protect Configuration Files

```bash
# 加密数据库配置 / Encrypt database config
python sunny.py encrypt --file database.config

# 在应用中解密使用 / Decrypt and use in application
python sunny.py decrypt --file database.config.enc --key YOUR_KEY
```

### 案例2: API安全验证 / Use Case 2: API Security Verification

```python
# server.py - 服务器端 / Server side
from src.verification import VerificationManager

vm = VerificationManager()

# 生成令牌给客户端 / Generate token for client
token_info = vm.generate_token(app_id="client_app", expires_in=3600)
print(f"Token: {token_info['token']}")

# 验证客户端请求 / Verify client request
def verify_request(token):
    result = vm.verify_token(token)
    if result['valid']:
        print(f"Authorized: {result['app_id']}")
        return True
    else:
        print(f"Unauthorized: {result['error']}")
        return False
```

### 案例3: 数据传输加密 / Use Case 3: Data Transmission Encryption

```python
# sender.py - 发送方 / Sender
from src.encryption import EncryptionManager

em = EncryptionManager()
result = em.encrypt(text="敏感数据")
# 发送: result['encrypted_text'] 和 result['key']
# Send: result['encrypted_text'] and result['key']

# receiver.py - 接收方 / Receiver
decrypted = em.decrypt(text=encrypted_text, key=key)
print(decrypted['decrypted_text'])
```

## 高级功能 / Advanced Features

### 自定义加密密钥 / Custom Encryption Key

```bash
# 使用自定义密钥加密 / Encrypt with custom key
python sunny.py encrypt --file data.txt --key YOUR_CUSTOM_KEY
```

### 自定义令牌过期时间 / Custom Token Expiration

```bash
# 生成24小时有效的令牌 / Generate token valid for 24 hours
python sunny.py verify --generate --expires 86400
```

### 自定义配置文件路径 / Custom Config File Path

```bash
# 使用自定义配置文件 / Use custom config file
python sunny.py integrate --setup --config /path/to/my_config.json
python sunny.py integrate --test --config /path/to/my_config.json
```

## 集成到项目 / Integrate into Project

### Python项目 / Python Project

```python
import sys
sys.path.append('/path/to/sunny')

from src.encryption import EncryptionManager
from src.verification import VerificationManager
from src.integration import IntegrationManager

# 使用加密功能 / Use encryption
em = EncryptionManager()
encrypted = em.encrypt(text="secret data")

# 使用验证功能 / Use verification
vm = VerificationManager()
token = vm.generate_token(app_id="myapp")
```

### 作为子模块 / As Submodule

```bash
# 添加为Git子模块 / Add as Git submodule
git submodule add https://github.com/stfzy/sunny.git libs/sunny
git submodule update --init --recursive

# 在代码中使用 / Use in code
from libs.sunny.src.encryption import EncryptionManager
```

## 常见问题 / FAQ

### Q1: 忘记了加密密钥怎么办？
A1: 密钥丢失后无法恢复加密数据。请务必妥善保管密钥！

### Q2: 令牌过期了怎么办？
A2: 重新生成新的令牌即可。使用 `--expires` 参数设置更长的过期时间。

### Q3: 如何在生产环境中使用？
A3: 
1. 使用 `integrate --setup` 生成配置文件
2. 妥善保管 API 密钥和密钥
3. 定期更新令牌
4. 使用 HTTPS 传输加密数据

### Q4: 支持哪些加密算法？
A4: 目前使用 AES-256-CBC 加密算法，这是行业标准的高强度加密算法。

### Q5: 如何批量加密多个文件？
A5: 使用 shell 脚本循环处理：
```bash
for file in *.txt; do
    python sunny.py encrypt --file "$file"
done
```

## 性能指标 / Performance Metrics

- 加密速度 / Encryption speed: ~100MB/s
- 令牌生成 / Token generation: <1ms
- 令牌验证 / Token verification: <1ms
- 配置生成 / Config generation: <10ms

## 安全建议 / Security Best Practices

1. ✅ 使用强随机密钥（已自动生成）
2. ✅ 定期更换 API 密钥
3. ✅ 不要在代码中硬编码密钥
4. ✅ 使用环境变量存储密钥
5. ✅ 加密传输敏感数据
6. ✅ 设置合理的令牌过期时间

## 下一步 / Next Steps

- 查看完整文档: [README.md](README.md)
- 运行示例代码: `python examples/example_usage.py`
- 查看源代码: [src/](src/)
- 提交问题: [GitHub Issues](https://github.com/stfzy/sunny/issues)

## 更新日志 / Changelog

### v1.0.0 (2025-10-07)
- ✅ 初始版本发布
- ✅ 实现 AES-256 加密
- ✅ 实现令牌验证系统
- ✅ 实现一键对接配置
- ✅ 完整的 CLI 界面
