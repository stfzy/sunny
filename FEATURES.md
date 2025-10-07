# Sunny 功能特性详解 / Feature Details

## 🎯 核心功能 / Core Features

### 1. 一键加密 (One-Click Encryption)

#### 特点 / Features
- ✅ **AES-256-CBC 加密** - 工业标准的高强度加密算法
- ✅ **自动密钥生成** - 使用加密安全的随机数生成器
- ✅ **文件加密** - 支持任意大小的文件加密
- ✅ **文本加密** - 直接加密文本内容
- ✅ **自动 IV 生成** - 每次加密使用不同的初始化向量

#### 使用场景 / Use Cases
- 🔒 保护敏感配置文件
- 🔒 加密数据库备份
- 🔒 保护个人文件
- 🔒 传输前加密数据

#### 命令示例 / Command Examples
```bash
# 加密文件
python sunny.py encrypt --file config.json

# 加密文本
python sunny.py encrypt --text "敏感信息"

# 使用自定义密钥
python sunny.py encrypt --file data.txt --key YOUR_KEY

# 指定输出路径
python sunny.py encrypt --file data.txt --output encrypted.bin
```

#### 技术规格 / Technical Specs
- **算法**: AES-256-CBC
- **密钥长度**: 256 bits (32 bytes)
- **IV 长度**: 128 bits (16 bytes)
- **填充**: PKCS7
- **编码**: Base64 (用于文本输出)

---

### 2. 网络验证 (Network Verification)

#### 特点 / Features
- ✅ **令牌生成** - 生成带签名的 JSON Web Token
- ✅ **HMAC-SHA256 签名** - 防止令牌篡改
- ✅ **过期控制** - 可配置的令牌有效期
- ✅ **防重放攻击** - 每个令牌包含唯一 nonce
- ✅ **应用标识** - 支持多应用隔离

#### 使用场景 / Use Cases
- 🎫 API 身份验证
- 🎫 单点登录 (SSO)
- 🎫 临时访问授权
- 🎫 分布式系统认证

#### 命令示例 / Command Examples
```bash
# 生成令牌
python sunny.py verify --generate --app-id myapp

# 生成长效令牌（24小时）
python sunny.py verify --generate --app-id myapp --expires 86400

# 验证令牌
python sunny.py verify --token "eyJkYXRhIjogeyJhcH..."
```

#### 令牌结构 / Token Structure
```json
{
  "data": {
    "app_id": "myapp",
    "issued_at": 1759843301,
    "expires_at": 1759846901,
    "nonce": "24571cf00d000ca8b49e046a603b9049"
  },
  "signature": "0c0329b6d3f37ae1249cccb52a0cd0bffe400f485ca644a41f6f6590b90d119d"
}
```

#### 安全特性 / Security Features
- ✅ 签名验证防篡改
- ✅ 时间戳防过期使用
- ✅ Nonce 防重放攻击
- ✅ 密钥隔离（每个实例独立密钥）

---

### 3. 一键对接 (One-Click Integration)

#### 特点 / Features
- ✅ **自动配置生成** - 一键生成完整配置文件
- ✅ **API 密钥管理** - 自动生成安全的 API 密钥
- ✅ **连接测试** - 验证配置正确性
- ✅ **多语言支持** - 提供多种语言的集成示例

#### 使用场景 / Use Cases
- 🔌 快速接入现有系统
- 🔌 微服务认证集成
- 🔌 第三方应用对接
- 🔌 API 网关配置

#### 命令示例 / Command Examples
```bash
# 设置配置
python sunny.py integrate --setup

# 自定义配置路径
python sunny.py integrate --setup --config /path/to/config.json

# 测试连接
python sunny.py integrate --test --config config.json
```

#### 配置文件结构 / Config File Structure
```json
{
  "version": "1.0.0",
  "app_id": "app_6efe5f59ed970f75",
  "api_key": "sk_wmWNVHE6lVlO0mnXE...",
  "secret_key": "AR-b0rk1h-O9Y0GzTa7jVL...",
  "created_at": "2025-10-07T13:22:35",
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

---

## 🔥 高级特性 / Advanced Features

### 模块化设计 / Modular Design
```
sunny/
├── src/
│   ├── encryption.py      # 独立的加密模块
│   ├── verification.py    # 独立的验证模块
│   └── integration.py     # 独立的集成模块
```

每个模块都可以单独导入使用：

```python
from src.encryption import EncryptionManager
from src.verification import VerificationManager
from src.integration import IntegrationManager
```

### 可编程接口 / Programmatic API

#### 加密 API
```python
em = EncryptionManager()

# 加密
result = em.encrypt(text="data")
# Returns: {'key': '...', 'encrypted_text': '...'}

# 解密
decrypted = em.decrypt(text=encrypted, key=key)
# Returns: {'decrypted_text': '...'}
```

#### 验证 API
```python
vm = VerificationManager()

# 生成令牌
token_info = vm.generate_token(app_id="app", expires_in=3600)
# Returns: {'app_id': '...', 'token': '...', 'expires_at': '...'}

# 验证令牌
result = vm.verify_token(token)
# Returns: {'valid': True/False, 'app_id': '...', ...}
```

#### 集成 API
```python
im = IntegrationManager()

# 设置配置
config = im.setup(config_path="config.json")
# Returns: {'config_path': '...', 'app_id': '...', 'api_key': '...'}

# 测试连接
result = im.test_connection(config_path="config.json")
# Returns: {'success': True/False, 'response_time': ..., ...}
```

---

## 📊 性能指标 / Performance Metrics

| 操作 / Operation | 速度 / Speed | 说明 / Notes |
|-----------------|-------------|-------------|
| 文本加密 | < 1ms | 小于 1KB 文本 |
| 文件加密 | ~100MB/s | 依赖硬件性能 |
| 令牌生成 | < 1ms | 包括签名 |
| 令牌验证 | < 1ms | 包括签名验证 |
| 配置生成 | < 10ms | 包括密钥生成 |

---

## 🔒 安全性 / Security

### 加密安全 / Encryption Security
- ✅ AES-256 - NIST 认证标准
- ✅ CBC 模式 - 安全的加密模式
- ✅ 随机 IV - 每次加密不同
- ✅ PKCS7 填充 - 标准填充方案

### 验证安全 / Verification Security
- ✅ HMAC-SHA256 - 强签名算法
- ✅ 时间验证 - 防止过期令牌
- ✅ Nonce - 防止重放攻击
- ✅ 密钥隔离 - 独立密钥管理

### 密钥管理 / Key Management
- ✅ 加密安全随机数生成器
- ✅ Base64 URL-safe 编码
- ✅ 256 位密钥强度
- ✅ 不在日志中记录密钥

---

## 🌍 国际化 / Internationalization

所有输出信息都提供中英文双语：
- ✅ 命令行帮助信息
- ✅ 错误提示信息
- ✅ 成功提示信息
- ✅ 文档注释

---

## 📦 包管理 / Package Management

### 使用 pip 安装 / Install with pip
```bash
pip install -r requirements.txt
```

### 使用 setup.py 安装 / Install with setup.py
```bash
python setup.py install
```

### 依赖项 / Dependencies
- `cryptography >= 41.0.0` - 加密库

---

## 🧪 测试覆盖 / Test Coverage

### 功能测试 / Functional Tests
- ✅ 文本加密/解密
- ✅ 文件加密/解密
- ✅ 令牌生成/验证
- ✅ 配置生成/测试
- ✅ 多语言内容（中英文）

### 边界测试 / Edge Case Tests
- ✅ 空文件处理
- ✅ 大文件处理
- ✅ 过期令牌
- ✅ 无效签名
- ✅ 错误密钥

---

## 🚀 部署建议 / Deployment Recommendations

### 开发环境 / Development
```bash
git clone https://github.com/stfzy/sunny.git
cd sunny
pip install -r requirements.txt
python sunny.py --help
```

### 生产环境 / Production
```bash
# 1. 设置配置
python sunny.py integrate --setup --config /etc/sunny/config.json

# 2. 设置权限
chmod 600 /etc/sunny/config.json

# 3. 使用环境变量
export SUNNY_CONFIG=/etc/sunny/config.json

# 4. 集成到应用
from src.encryption import EncryptionManager
from src.verification import VerificationManager
```

---

## 📞 支持 / Support

- 📖 完整文档: [README.md](README.md)
- 🚀 快速入门: [QUICKSTART.md](QUICKSTART.md)
- 💡 示例代码: [examples/example_usage.py](examples/example_usage.py)
- 🐛 问题报告: [GitHub Issues](https://github.com/stfzy/sunny/issues)

---

## 📝 版本历史 / Version History

### v1.0.0 (2025-10-07)
- 🎉 首次发布
- ✅ 完整的加密功能
- ✅ 完整的验证功能
- ✅ 完整的集成功能
- ✅ CLI 工具
- ✅ 中英文文档

---

## 📄 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件
