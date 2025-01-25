# 基础教程

本教程将详细介绍 EEG-Analyze 的主要功能和使用方法。

## 目录

1. [数据加载与预处理](#数据加载与预处理)
2. [特征提取](#特征提取)
3. [时频分析](#时频分析)
4. [相位分析](#相位分析)
5. [数据可视化](#数据可视化)

## 数据加载与预处理

### 支持的数据格式

EEG-Analyze 支持多种数据格式：

```python
from data_loader import loadEEGData

# 加载 NPY 文件
data = loadEEGData(
    data_path='data.npy',
    window=2.0,
    frame=1.0,
    sample_rate=250
)

# 加载 CSV 文件
data = loadEEGData(
    data_path='data.csv',
    window=2.0,
    frame=1.0,
    sample_rate=250,
    channels=4
)

# 加载 EDF 文件
data = loadEEGData(
    data_path='data.edf',
    window=2.0,
    frame=1.0,
    sample_rate=250,
    edf_channels=['Fp1', 'Fp2', 'F3', 'F4']
)
```

### 数据预处理

```python
from preprocessor import preprocess_eeg

# 基本预处理
processed_data, params = preprocess_eeg(
    data=raw_data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=250
)

# 数据增强
from preprocessor import augment_eeg

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

## 特征提取

### 时域特征

```python
from feature_extractor import extract_features

features = extract_features(data, sample_rate=250)

# 访问时域特征
print("均值:", features['mean'])
print("标准差:", features['std'])
print("峰峰值:", features['ptp'])
print("过零率:", features['zero_crossing_rate'])
```

### 频域特征

```python
# 访问频域特征
print("Delta能量:", features['delta'])
print("Alpha能量:", features['alpha'])
print("Beta能量:", features['beta'])
print("频段能量占比:", features['band_power'])
print("谱熵:", features['spectral_entropy'])
```

## 时频分析

```python
from eeg_analyze import EEGAnalyzer

analyzer = EEGAnalyzer(sample_rate=250)

# 进行时频分析
tf_data = analyzer.time_frequency_analysis(
    data=processed_data,
    window_size=1.0,
    overlap=0.5
)

# 可视化时频结果
from eeg_analyze import EEGVisualizer

visualizer = EEGVisualizer(sample_rate=250)
visualizer.plot_time_frequency(
    tf_data=tf_data,
    save_dir='results',
    channel_idx=0
)
```

## 相位分析

```python
# 计算相位锁定值
phase_data = analyzer.phase_analysis(
    data=processed_data,
    freq_band=(8, 13)  # Alpha频段
)

# 可视化相位连接性
visualizer.plot_phase_connectivity(
    plv_matrix=phase_data['plv_matrix'],
    save_dir='results',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)
```

## 数据可视化

### 时域波形

```python
visualizer.plot_time_domain(
    data=processed_data,
    save_dir='results',
    title='EEG时域波形',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)
```

### 脑地形图

```python
# 定义通道位置
channel_positions = {
    'Fp1': (-0.5, 0.5),
    'Fp2': (0.5, 0.5),
    'F3': (-0.5, -0.5),
    'F4': (0.5, -0.5)
}

# 绘制脑地形图
visualizer.plot_brain_map(
    data=features['alpha'],  # 使用Alpha频段能量
    save_dir='results',
    channel_positions=channel_positions,
    title='Alpha频段能量分布'
)
```

### 综合视图

```python
# 评估数据质量
quality_metrics = analyzer.assess_data_quality(processed_data)

# 绘制综合视图
visualizer.plot_comprehensive_view(
    data=processed_data,
    tf_data=tf_data,
    quality_metrics=quality_metrics,
    save_dir='results',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)
```

## 最佳实践

1. 数据预处理
   - 始终进行数据清理和滤波
   - 根据需要选择合适的预处理方法
   - 保存预处理参数以便复用

2. 特征提取
   - 根据应用场景选择合适的特征
   - 注意特征的标准化
   - 考虑特征的生理意义

3. 可视化
   - 使用合适的配色方案
   - 添加清晰的标签和图例
   - 保存高质量的图像

4. 性能优化
   - 对大数据使用分段处理
   - 适当设置窗口大小和重叠
   - 根据需要调整采样率

## 下一步

- 查看[API文档](../api/analyzer.md)了解更多细节
- 参考[示例代码](../../examples)学习更多用法
- 阅读[贡献指南](../../CONTRIBUTING.md)参与项目开发 