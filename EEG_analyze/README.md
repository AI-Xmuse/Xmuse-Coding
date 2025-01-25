# EEG-Analyze

EEG-Analyze 是一个功能强大的脑电信号(EEG)分析工具包，提供了完整的数据处理、分析和可视化功能。本工具包支持多种数据格式，具有丰富的分析方法和直观的可视化功能。

## 主要特性

### 数据处理
- 支持多种数据格式导入 (CSV, NPY, EDF)
- 自动数据分段和窗口处理
- 完整的预处理流程（滤波、去噪、标准化等）
- 数据质量评估和异常检测

### 信号分析
- 时域特征提取（统计特征、Hjorth参数等）
- 频域分析（功率谱密度、频段能量等）
- 时频分析（短时傅里叶变换）
- 相位分析（相位锁定值）

### 可视化功能
- 时域波形图
- 功率谱密度图
- 时频分析图
- 相位连接性热力图
- 脑地形图
- 综合分析视图

### 其他特性
- 中文界面支持
- 完整的数据导出功能
- 丰富的示例代码
- 详细的文档说明


## 快速开始

### 基本使用
```python
import numpy as np
from eeg_analyze import EEGAnalyzer, EEGVisualizer
from eeg_analyze import preprocess_eeg
from eeg_analyze import loadEEGData

# 加载数据
data = loadEEGData(
    data_path='your_eeg_data.npy',
    window=2.0,
    frame=1.0,
    sample_rate=256
)

# 预处理
processed_data, _ = preprocess_eeg(
    data=data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=250
)

# 创建分析器和可视化器
analyzer = EEGAnalyzer(sample_rate=250)
visualizer = EEGVisualizer(sample_rate=250)

# 分析数据
tf_data = analyzer.time_frequency_analysis(processed_data[0])
phase_data = analyzer.phase_analysis(processed_data[0])
quality_metrics = analyzer.assess_data_quality(processed_data[0])

# 可视化结果
visualizer.plot_comprehensive_view(
    data=processed_data[0],
    tf_data=tf_data,
    quality_metrics=quality_metrics,
    save_dir='results'
)
```

## 文档

详细文档请参见 [docs](docs/) 目录：

- [安装说明](docs/guide/installation.md)
- [快速入门](docs/guide/quickstart.md)
- [基础教程](docs/guide/tutorial.md)
- [API参考](docs/api/)
- [示例代码](docs/examples/)

## 示例

查看 [examples](examples/) 目录获取更多使用示例：

- [基础分析示例](examples/basic_analysis.py)
- [高级分析示例](examples/advanced.md)
- [批处理示例](docs/examples/advanced.md#1-批处理多个数据文件)

## 系统要求

- Python >= 3.7
- NumPy >= 1.21.0
- SciPy >= 1.7.0
- Pandas >= 1.3.0
- Matplotlib >= 3.4.0
- MNE >= 1.0.0

## 开发相关

- [开发指南](docs/guide/development.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 问题反馈

如果您在使用过程中遇到任何问题，或有任何建议，欢迎：

 提交 [Issue](https://github.com/AI-Xmuse/Xmuse-Coding.git)

## 联系方式

- 作者：[ZhuQinghui]
- 邮箱：[601625293@qq.com或者support@xmuse.cn]
- 项目主页：[https://github.com/AI-Xmuse/Xmuse-Coding.git]

---
如有问题或建议，欢迎提交 Issue 或通过邮件联系。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
