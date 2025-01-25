# OSC Data Handler

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个用于处理和转发OSC（Open Sound Control）数据的Python应用程序。该程序可以接收、处理和转发OSC数据，支持多设备管理和数据本地存储。适用于需要实时处理和转发OSC数据的场景，如音频处理、传感器数据采集等。

## 目录
- [功能特点](#功能特点)
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [项目结构](#项目结构)
- [开发指南](#开发指南)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 功能特点

- 🚀 高性能OSC数据流接收与处理
- 📦 实时数据处理和转发
- 💾 数据本地持久化存储
- 🔄 多设备并行支持
- 🔒 线程安全的数据处理
- 📝 完善的错误处理和日志记录
- ⚙️ 灵活的配置系统

## 系统要求

### 环境要求
- Python 3.7+

## 快速开始

### 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
   cd osc-data-handler
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 基本使用

1. 配置设备：
   ```python
   # config.py 配置示例
   OUTPUT_DIR = "/path/to/output"
   DEVICE_HOST = "127.0.0.1"
   DEVICE_PORT = 8000
   ```

   或通过环境变量配置：
   ```bash
   export OSC_DEVICE_HOST="127.0.0.1"
   export OSC_DEVICE_PORT="8000"
   export OSC_OUTPUT_DIR="/custom/path/to/output"
   ```

2. 运行程序：
   ```bash
   python main.py
   ```

3. 退出程序：
   按 'q' 键优雅退出

## 详细配置

### 默认配置
| 配置项 | 说明 | 默认值 | 可选值 |
|--------|------|--------|--------|
| OSC服务器端口 | 监听端口 | 8000 | 1024-65535 |
| 设备地址 | OSC设备IP | 127.0.0.1 | 有效IP地址 |
| 数据保存路径 | 输出目录 | ~/Desktop/record | 有效路径 |

### 环境变量
| 环境变量 | 说明 | 默认值 | 必填 |
|----------|------|--------|------|
| OSC_DEVICE_HOST | OSC设备主机地址 | 127.0.0.1 | 否 |
| OSC_DEVICE_PORT | OSC设备端口 | 8000 | 否 |
| OSC_OUTPUT_DIR | 数据输出目录 | ~/Desktop/record | 否 |

## 项目结构

```
osc-data-handler/
├── main.py          # 程序入口
├── config.py        # 配置文件
├── Server.py        # OSC服务器实现
├── data_handler.py  # 数据处理模块
├── tests/           # 测试文件
│   ├── test_server.py
│   └── test_handler.py
├── docs/           # 文档
├── requirements.txt # 项目依赖
├── LICENSE         # 许可证
└── README.md       # 项目文档
```

## 开发指南

### 数据格式
保存的数据格式为文本文件，每行包含时间戳和数据：
```
Timestamp: 1234567890.123, Data: (value1, value2, ...)
```

### API文档
主要类和方法：

#### DataHandler
```python
class DataHandler:
    def __init__(self, data_buffer, clients, output_dir, exit_event):
        """初始化数据处理器
        
        Args:
            data_buffer: 数据缓冲区
            clients: OSC客户端字典
            output_dir: 输出目录
            exit_event: 退出事件
        """
```

## 常见问题

### 1. 端口被占用
- **症状**：启动时报错 "Address already in use"
- **解决方案**：
  - 检查8000端口是否被其他程序占用
  - 修改配置文件中的端口号
  - 使用 `netstat -ano` 查看端口占用

### 2. 权限问题
- **症状**：无法写入数据文件
- **解决方案**：
  - 确保程序对输出目录有写入权限
  - Windows用户可能需要以管理员身份运行
  - 检查防火墙设置

## 更新日志

### [1.0.0] - 2024-01-01
- 🎉 首次发布
- ✨ 基本功能实现
- 🐛 修复已知问题

## 贡献指南

欢迎提交 Pull Request 或 Issue。在提交之前，请确保：

1. 代码规范
   - 遵循 PEP 8 规范
   - 使用类型注解
   - 添加适当的注释

2. 测试要求
   - 添加单元测试
   - 确保所有测试通过
   - 测试覆盖率不低于 80%

3. 文档要求
   - 更新相关文档
   - 添加变更日志
   - 完善注释和类型提示

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 作者：[ZhuQinghui]
- 邮箱：[601625293@qq.com或者support@xmuse.cn]
- 项目主页：[https://github.com/AI-Xmuse/Xmuse-Coding.git]

---
如有问题或建议，欢迎提交 Issue 或通过邮件联系。
