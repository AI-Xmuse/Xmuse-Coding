# LSL信号采集工具

这是一个基于Lab Streaming Layer (LSL)的多通道生理信号实时采集工具。支持采集、保存和可视化多种生理信号数据，如脑电图(EEG)、光电容积脉搏波(PPG)等。

## 目录
- [功能特点](#功能特点)
- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [使用说明](#使用说明)
- [数据格式说明](#数据格式说明)
- [支持的信号类型](#支持的信号类型)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 功能特点

- 多种生理信号实时采集
  - 支持LSL数据流
  - 自动检测和连接可用的数据流
  - 自适应不同采样率的数据流

- 实时数据可视化
  - EEG数据实时波形显示
  - 4通道同步显示
  - 自适应显示范围

- 数据存储管理
  - 自动保存数据为CSV格式
  - 按LSL信号流类型创建独立存储目录
  - 支持多通道数据记录

## 系统要求

- Python 3.8 或更高版本
- Windows/Linux/MacOS 操作系统
- LSL兼容的数据采集设备

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/AI-Xmuse/Xmuse-Coding.git
cd lsl-signal-collector
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用说明

1. 设备准备：
   - 确保LSL设备已正确连接
   - 检查设备驱动是否正确安装
   - 确认LSL数据流可用

2. 运行程序：
```bash
python main.py
```

3. 程序功能：
   - 自动检测并显示可用的数据流
   - 实时显示EEG数据波形
   - 自动保存所有数据流

4. 数据存储：
   - 数据保存在`signal_data/时间戳/`目录下
   - 每个信号类型单独保存为CSV文件
   - 文件命名格式：`信号类型_signal.csv`

5. 程序退出：
   - 使用Ctrl+C正常退出程序
   - 确保数据完整保存

## 数据格式说明

### CSV文件结构
每个信号类型的CSV文件包含以下列：
```
timestamp, channel_1, channel_2, ..., channel_n
```

- timestamp: Unix时间戳，精确到毫秒
- channel_x: 对应通道的数据值

### 采样率说明
- 每种信号类型保持其原始采样率
- 数据保存频率与信号源保持一致
- 时间戳精确记录每个数据点的采集时间

## 支持的信号类型

| 信号类型 | 说明 |
|---------|------|
| EEG | 脑电图数据 |
| PPG | 光电容积脉搏波 |
| Accel | 加速度数据 |
| Gyro | 陀螺仪数据 |
| Blink | 眨眼检测 |
| 其他 | 更多信号类型 |

## 常见问题


1. 找不到数据流？
   - 检查设备连接
   - 确认LSL驱动正确安装
   - 验证设备是否正常工作

2. 数据保存不完整？
   - 使用Ctrl+C正常退出程序
   - 确保磁盘空间充足
   - 检查文件写入权限

3. 显示卡顿？
   - 降低采样率
   - 关闭不需要的数据流
   - 检查系统资源占用
## 联系
- 作者：[ZhuQinghui]
- 邮箱：[601625293@qq.com或者support@xmuse.cn]
- 项目主页：[https://github.com/AI-Xmuse/Xmuse-Coding.git]
- 项目链接: [https://github.com/AI-Xmuse/Xmuse-Coding.git](https://github.com/AI-Xmuse/Xmuse-Coding.git)

## 贡献指南

欢迎贡献代码，提出问题或建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 