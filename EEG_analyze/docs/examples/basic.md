# 基础示例

本文档提供了一些基础的使用示例，帮助你快速上手 EEG-Analyze。

## 1. 数据加载和预处理

```python
import numpy as np
from eeg_analyze import EEGAnalyzer, EEGVisualizer
from eeg_analyze.preprocessor import preprocess_eeg
from eeg_analyze.data_loader import loadEEGData

# 加载数据
data = loadEEGData(
    data_path='sample_eeg.npy',
    window=2.0,
    frame=1.0,
    sample_rate=250
)

# 预处理
processed_data, _ = preprocess_eeg(
    data=data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=250
)
```

## 2. 基本分析

```python
# 创建分析器
analyzer = EEGAnalyzer(sample_rate=250)

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

## 3. 基本可视化

```python
# 创建可视化器
visualizer = EEGVisualizer(sample_rate=250)

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
    channel_idx=0
)
```

## 4. 完整的分析流程

```python
def analyze_eeg_basic():
    """基本的EEG分析流程示例"""
    
    # 1. 加载数据
    data = loadEEGData(
        data_path='sample_eeg.npy',
        window=2.0,
        frame=1.0,
        sample_rate=250
    )
    
    # 2. 预处理
    processed_data, _ = preprocess_eeg(
        data=data,
        methods=['clean', 'filter', 'normalize'],
        sample_rate=250
    )
    
    # 3. 创建分析器和可视化器
    analyzer = EEGAnalyzer(sample_rate=250)
    visualizer = EEGVisualizer(sample_rate=250)
    
    # 4. 分析
    tf_data = analyzer.time_frequency_analysis(processed_data[0])
    quality_metrics = analyzer.assess_data_quality(processed_data[0])
    
    # 5. 可视化
    visualizer.plot_comprehensive_view(
        data=processed_data[0],
        tf_data=tf_data,
        quality_metrics=quality_metrics,
        save_dir='results'
    )

if __name__ == '__main__':
    analyze_eeg_basic()
```

## 5. 数据增强示例

```python
from eeg_analyze.preprocessor import augment_eeg

# 添加噪声
noisy_data = augment_eeg(
    data=processed_data,
    method='noise',
    noise_level=0.1
)

# 时间移位
shifted_data = augment_eeg(
    data=processed_data,
    method='shift',
    shift_range=10
)
```

## 6. 保存结果

```python
from eeg_analyze.preprocessor import save_eeg_data

# 保存处理后的数据
save_eeg_data(processed_data, 'processed_data.npy')

# 保存为CSV格式
save_eeg_data(processed_data, 'processed_data.csv', format='csv')
```

## 下一步

- 查看[进阶示例](advanced.md)了解更多高级用法
- 阅读[API文档](../api/analyzer.md)获取详细接口信息
- 参考[基础教程](../guide/tutorial.md)学习更多基础知识 