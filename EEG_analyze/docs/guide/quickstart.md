# 快速开始

本指南将帮助你快速上手 EEG-Analyze，了解基本功能的使用方法。

## 基本用法

### 1. 导入必要的模块

```python
import numpy as np
from eeg_analyze import EEGAnalyzer, EEGVisualizer
from eeg_analyze.preprocessor import preprocess_eeg
from eeg_analyze.data_loader import loadEEGData
```

### 2. 加载数据

```python
# 设置参数
sample_rate = 250  # Hz
window = 2.0      # 窗口大小（秒）
frame = 1.0       # 帧移大小（秒）

# 加载数据
data = loadEEGData(
    data_path='your_data.npy',  # 支持 .npy, .csv, .edf 格式
    window=window,
    frame=frame,
    sample_rate=sample_rate
)
```

### 3. 数据预处理

```python
# 预处理数据
processed_data, params = preprocess_eeg(
    data=data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=sample_rate
)
```

### 4. 分析数据

```python
# 创建分析器
analyzer = EEGAnalyzer(sample_rate=sample_rate)

# 时频分析
tf_data = analyzer.time_frequency_analysis(processed_data[0])

# 相位分析
phase_data = analyzer.phase_analysis(
    data=processed_data[0],
    freq_band=(8, 13)  # Alpha频段
)

# 数据质量评估
quality_metrics = analyzer.assess_data_quality(processed_data[0])
```

### 5. 可视化结果

```python
# 创建可视化器
visualizer = EEGVisualizer(sample_rate=sample_rate)

# 绘制时域波形
visualizer.plot_time_domain(
    data=processed_data[0],
    save_dir='results',
    title='EEG时域波形',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)

# 绘制时频图
visualizer.plot_time_frequency(
    tf_data=tf_data,
    save_dir='results',
    channel_idx=0,
    title='时频分析结果'
)

# 绘制综合视图
visualizer.plot_comprehensive_view(
    data=processed_data[0],
    tf_data=tf_data,
    quality_metrics=quality_metrics,
    save_dir='results'
)
```

## 完整示例

这里是一个完整的分析流程示例：

```python
import numpy as np
from eeg_analyze import EEGAnalyzer, EEGVisualizer
from eeg_analyze.preprocessor import preprocess_eeg
from eeg_analyze.data_loader import loadEEGData

def analyze_eeg():
    # 1. 参数设置
    sample_rate = 250  # Hz
    window = 2.0      # 窗口大小（秒）
    frame = 1.0       # 帧移大小（秒）
    
    # 2. 加载数据
    data = loadEEGData(
        data_path='data/sample_eeg.npy',
        window=window,
        frame=frame,
        sample_rate=sample_rate
    )
    
    # 3. 数据预处理
    processed_data, _ = preprocess_eeg(
        data=data,
        methods=['clean', 'filter', 'normalize'],
        sample_rate=sample_rate
    )
    
    # 4. 创建分析器和可视化器
    analyzer = EEGAnalyzer(sample_rate=sample_rate)
    visualizer = EEGVisualizer(sample_rate=sample_rate)
    
    # 5. 分析数据
    tf_data = analyzer.time_frequency_analysis(processed_data[0])
    quality_metrics = analyzer.assess_data_quality(processed_data[0])
    
    # 6. 可视化结果
    visualizer.plot_comprehensive_view(
        data=processed_data[0],
        tf_data=tf_data,
        quality_metrics=quality_metrics,
        save_dir='results'
    )

if __name__ == '__main__':
    analyze_eeg()
```

## 下一步

- 查看[基础教程](tutorial.md)了解更多功能
- 阅读[API文档](../api/analyzer.md)获取详细接口信息
- 参考[示例代码](../../examples)学习更多用法 