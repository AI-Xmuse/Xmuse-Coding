# LSL 数据流处理工具

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

这是一个用于处理 LSL（Lab Streaming Layer）数据流的 Python 工具。它提供了一个简单而强大的接口，用于接收、显示和保存来自各种 LSL 数据源的数据流。

## 目录

- [功能特点](#功能特点)
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细使用说明](#详细使用说明)
- [项目结构](#项目结构)
- [数据格式](#数据格式)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [更新日志](#更新日志)
- [许可证](#许可证)

## 功能特点

- **自动发现数据流**
  - 自动查找和连接可用的 LSL 数据流
  - 支持多种数据类型（EEG、PPG、Gory 等）
  - 智能处理连接中断和重连

- **实时数据处理**
  - 实时显示数据流信息和采样数据
  - 支持高采样率数据的稳定接收
  - 自动检测和处理异常数据

- **多格式数据保存**
  - CSV 格式：适合通用数据分析和导入其他工具
  - JSON 格式：包含完整的元数据信息
  - HDF5 格式：适合大规模数据的高效存储和访问
  - 支持数据分段保存，防止数据丢失

- **性能监控**
  - 实时显示数据统计信息
  - 自动记录运行日志

## 系统要求

- **操作系统**
  - Windows 10 或更高版本
  - macOS 10.14 或更高版本
  - Linux (Ubuntu 18.04+, CentOS 7+)

- **Python 环境**
  - Python 3.7 或更高版本
  - pip 包管理器


## 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
   cd Pylsl
   ```

2. **创建虚拟环境** (推荐)
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python main.py
   ```

## 详细使用说明

### 基本用法

1. **启动程序**
   - 运行 `main.py`
   - 程序会自动搜索可用的 LSL 数据流
   - 显示找到的数据流信息

2. **数据显示**
   - 实时显示接收到的数据
   - 每个通道的数据都会被格式化显示
   - 支持自定义显示格式

3. **数据保存**
   - 数据自动保存在 `data` 目录下
   - 使用时间戳命名的子目录
   - 支持多种文件格式

4. **程序退出**
   - 按 `Ctrl+C` 安全停止程序
   - 自动保存所有未保存的数据
   - 生成会话摘要报告

### 配置选项

可以通过修改以下参数自定义程序行为：

- `max_segment_size`: 单个数据段的最大样本数
- `stream_type`: 要查找的数据流类型
- `sampling_rate`: 目标采样率
- `save_formats`: 要保存的文件格式

## 数据格式

### CSV 格式
```csv
Timestamp,Channel_1,Channel_2,Channel_3,...
1234.567,0.123,0.456,0.789,...
```

### JSON 格式
```json
{
  "timestamps": [...],
  "data": [...],
  "channels": [...],
  "metadata": {
    "sampling_rate": 250,
    "start_time": "2024-01-15T10:30:00",
    "device_info": "..."
  }
}
```

### HDF5 结构
```
/data
  /timestamps
  /channels
  /raw_data
  /metadata
```

## 常见问题

1. **找不到数据流？**
   - 确保 LSL 设备已正确连接
   - 检查设备驱动是否正确安装
   - 验证网络连接是否正常

2. **数据保存失败？**
   - 检查磁盘空间是否充足
   - 确保有写入权限
   - 查看日志文件获取详细错误信息

3. **采样率异常？**
   - 检查系统性能监控
   - 调整缓冲区大小
   - 考虑降低采样率

## 贡献指南

我们欢迎各种形式的贡献，包括但不限于：

- 提交 Bug 报告
- 提供新功能建议
- 改进文档
- 提交代码修改

### 贡献步骤

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 更新日志

### [1.0.0] - 2024-01-15
- 初始版本发布
- 基本数据流处理功能
- 多格式数据保存支持

### [0.9.0] - 2024-01-10
- Beta 测试版本
- 核心功能实现
- 基础错误处理

## 许可证

该项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系
- 作者：[ZhuQinghui]
- 邮箱：[601625293@qq.com或者support@xmuse.cn]
- 项目主页：[https://github.com/AI-Xmuse/Xmuse-Coding.git]
- 项目链接: [https://github.com/AI-Xmuse/Xmuse-Coding.git](https://github.com/AI-Xmuse/Xmuse-Coding.git)

## 致谢

- [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) - LSL 项目
- [NumPy](https://numpy.org/) - 科学计算库
- [h5py](https://www.h5py.org/) - HDF5 数据格式支持 