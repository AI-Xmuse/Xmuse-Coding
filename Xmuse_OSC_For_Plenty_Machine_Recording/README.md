# OSC 数据接收器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/your-username/osc-data-receiver/workflows/CI/badge.svg)](https://github.com/your-username/osc-data-receiver/actions)
[![Documentation Status](https://readthedocs.org/projects/osc-data-receiver/badge/?version=latest)](https://osc-data-receiver.readthedocs.io/)

一个基于 Python 的多端口 OSC (Open Sound Control) 数据接收和处理工具，专门用于实时采集、过滤和存储多通道生理信号数据。支持多端口并发、信号过滤、实时数据存储等功能。

## 主要特性

- 🚀 **多端口并发**: 
  - 支持同时监听多个 OSC 端口
  - 高效的数据流处理机制
  - 自动负载均衡
  - 端口状态实时监控

- 🎯 **信号过滤**: 
  - 灵活的信号类型选择
  - 支持多种信号格式
  - 实时信号质量检测
  - 自定义信号过滤规则

- 💾 **实时存储**: 
  - CSV 格式数据存储
  - 批量写入优化
  - 自动文件管理
  - 数据完整性保证

- 📊 **性能监控**: 
  - 实时数据接收率统计
  - 丢包率监控
  - 系统资源使用监控
  - 性能瓶颈分析

- 🛡️ **异常恢复**: 
  - 数据缓冲机制
  - 自动错误恢复
  - 断点续传支持
  - 异常日志记录

- 🎨 **交互界面**: 
  - 友好的命令行界面
  - 实时状态显示
  - 交互式信号选择
  - 彩色日志输出

## 快速开始

### 系统要求

- 操作系统：Windows/Linux/MacOS
- Python 版本：3.7+
- 内存：至少 4GB
- 存储空间：根据数据量决定，建议 10GB+

### 安装

1. 克隆仓库：

```bash
git clone https://github.com/your-username/osc-data-receiver.git
cd osc-data-receiver
```

2. 创建虚拟环境（推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

### 使用方法

#### 基本用法

启动默认配置的接收器：

```bash
python run.py
```

#### 高级选项

自定义端口和保存目录：

```bash
python run.py --ports 8001 8002 --save-dir data --debug
```

多端口配置示例：

```bash
python run.py --ports 8001 8002 8003 --save-dir data/session1 --all-signals
```

### 命令行参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--ports` | OSC 服务器端口列表 | 8001 8002 | `--ports 8001 8002 8003` |
| `--save-dir` | 数据保存目录 | data | `--save-dir data/session1` |
| `--all-signals` | 接收所有信号 | False | `--all-signals` |
| `--debug` | 启用调试模式 | False | `--debug` |
| `--buffer-size` | 缓冲区大小 | 1000 | `--buffer-size 2000` |
| `--batch-size` | 批量写入大小 | 100 | `--batch-size 200` |

## 支持的信号类型

### EEG 信号
- `/eeg`: 脑电信号数据
  - 采样率：256Hz
  - 数据格式：(channel1, channel2, ..., channelN)
- `elements/is_good`: 信号质量指标
  - 范围：0-100
  - 更新频率：1Hz

### 生理信号
- `/ppg`: 光电容积信号
  - 采样率：100Hz
  - 数据格式：(red, infrared)
- `/batt`: 电池电量信息
  - 更新频率：0.2Hz
  - 数据格式：百分比(0-100)
- `/drlref`: 参考电极信号
  - 采样率：250Hz
  - 数据格式：float

### 运动数据
- `/acc`: 加速度数据
  - 采样率：50Hz
  - 数据格式：(x, y, z)
- `/gyro`: 陀螺仪数据
  - 采样率：50Hz
  - 数据格式：(pitch, roll, yaw)

## 数据格式

### CSV 文件格式

数据以 CSV 格式保存，包含以下字段：
- `Timestamp`: 数据采集时间戳（精确到毫秒）
- `Address`: 信号地址标识（包含端口信息）
- `Data`: 信号数据内容（元组格式）

示例：
```csv
Timestamp,Address,Data
2024-01-20 10:15:23.456,/8001/eeg,"(123.45, 234.56, 345.67)"
2024-01-20 10:15:23.458,/8001/ppg,"(98.76, 87.65)"
2024-01-20 10:15:23.460,/8001/acc,"(0.12, -0.34, 9.81)"
```

### 文件命名规则

```
osc_data_port_{端口号}_{时间戳}.csv
```

示例：`osc_data_port_8001_20240120_101523.csv`

## 项目结构

```
osc-data-receiver/
├── osc_receiver/          # 主要源代码
│   ├── core/             # 核心功能模块
│   │   ├── data_types.py    # 数据类型定义
│   │   ├── receiver.py      # OSC接收器实现
│   │   └── signal_manager.py # 信号管理器
│   ├── ui/              # 用户界面模块
│   │   └── signal_selector.py # 信号选择界面
│   └── main.py         # 主程序入口
├── tests/              # 测试文件
│   ├── test_receiver.py
│   └── test_signal_manager.py
├── data/              # 数据存储目录
├── docs/              # 文档
├── examples/          # 示例代码
├── run.py             # 程序启动脚本
├── requirements.txt    # 依赖列表
├── setup.py           # 安装配置
└── README.md          # 项目说明文档
```

## 性能特性

### 数据处理能力
- 每端口最大并发处理速率：10,000 样本/秒
- 支持同时监听最多 32 个端口
- 写入缓冲区大小：可配置，默认 1000 条记录
- 批量写入大小：可配置，默认 100 条记录

### 优化策略
- 使用缓冲区优化数据写入性能
- 批量处理减少 I/O 操作次数
- 动态休眠优化 CPU 使用率
- 线程池管理提高并发效率
- 实时性能监控和统计

### 资源消耗
- CPU：单核心负载 < 30%
- 内存：基础占用 < 100MB
- 磁盘写入：约 1MB/分钟（因数据量而异）

## 常见问题

### 1. 端口被占用
- 症状：启动时报错 "Address already in use"
- 解决方案：
  - 检查端口是否被其他程序占用
  - 使用 `--ports` 参数指定其他可用端口
  - 确保有足够的权限访问端口

### 2. 数据丢失
- 症状：数据文件不完整或丢失数据点
- 解决方案：
  - 检查磁盘剩余空间
  - 适当增加缓冲区大小
  - 确保写入权限正确
  - 检查网络连接状态

### 3. 性能问题
- 症状：CPU 使用率高或响应延迟
- 解决方案：
  - 减少同时监听的端口数量
  - 调整数据缓冲区大小
  - 使用更快的存储设备
  - 启用调试模式查看性能统计

## 开发说明

### 环境要求
- Python 3.7+
- python-osc >= 1.8.0
- pandas >= 1.3.0
- numpy >= 1.21.0

### 开发环境设置
1. 克隆开发分支
2. 安装开发依赖
3. 设置 pre-commit hooks
4. 运行测试套件

### 调试模式

启用调试模式可以查看详细的运行信息：
```bash
python run.py --debug
```

调试信息包括：
- 数据接收速率和延迟
- 缓冲区使用情况
- 信号处理状态
- 性能统计数据
- 系统资源使用情况

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

### 代码规范
- 遵循 PEP 8 规范
- 添加适当的注释和文档
- 确保通过所有测试
- 更新相关文档

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 更新日志

### v0.1.0 (2024-01)
- 初始版本发布
- 实现多端口数据接收
- 添加信号过滤功能
- 支持 CSV 格式数据存储
- 集成性能监控功能
- 优化数据处理流程
- 添加交互式信号选择界面

### 计划功能
- [ ] 数据可视化界面
- [ ] 实时数据分析
- [ ] 网络连接状态监控
- [ ] 数据加密存储
- [ ] 远程控制接口

## 联系方式

- 作者：[ZhuQinghui]
- 邮箱：[601625293@qq.com或者support@xmuse.cn]
- 项目主页：[https://github.com/AI-Xmuse/Xmuse-Coding.git]
- 项目链接: [https://github.com/AI-Xmuse/Xmuse-Coding.git](https://github.com/AI-Xmuse/Xmuse-Coding.git)

## 文档

- [API 文档](docs/API.md)
- [开发指南](docs/DEVELOPMENT.md)
- [贡献指南](docs/CONTRIBUTING.md)
