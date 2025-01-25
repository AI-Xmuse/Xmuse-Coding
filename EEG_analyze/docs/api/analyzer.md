# EEGAnalyzer API 参考

## 类：EEGAnalyzer

用于 EEG 信号分析的主要类。

### 初始化参数

```python
EEGAnalyzer(sample_rate: int)
```

- `sample_rate` (int): 采样率（Hz）

### 方法

#### assess_data_quality

评估 EEG 数据质量。

```python
def assess_data_quality(self, data: np.ndarray) -> dict
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (samples, channels)

**返回：**
- `dict`: 包含以下质量指标的字典：
  - `missing_ratio`: 缺失值比例
  - `snr`: 信噪比
  - `baseline_drift`: 基线漂移程度

#### time_frequency_analysis

进行时频分析。

```python
def time_frequency_analysis(
    self,
    data: np.ndarray,
    window_size: float = 1.0,
    overlap: float = 0.5,
    freq_range: tuple = (0.5, 50)
) -> dict
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (samples, channels)
- `window_size` (float): 时间窗口大小（秒）
- `overlap` (float): 窗口重叠比例
- `freq_range` (tuple): 频率范围（Hz）

**返回：**
- `dict`: 时频分析结果，包含：
  - `frequencies`: 频率数组
  - `times`: 时间点数组
  - `power`: 功率谱密度矩阵

#### phase_analysis

进行相位分析。

```python
def phase_analysis(
    self,
    data: np.ndarray,
    freq_band: tuple = (8, 13)
) -> dict
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (samples, channels)
- `freq_band` (tuple): 感兴趣的频段范围（Hz）

**返回：**
- `dict`: 相位分析结果，包含：
  - `plv_matrix`: 相位锁定值矩阵

### 示例

```python
import numpy as np
from eeg_analyze import EEGAnalyzer

# 创建分析器实例
analyzer = EEGAnalyzer(sample_rate=250)

# 生成示例数据
data = np.random.randn(1000, 4)  # 4秒数据，4通道

# 评估数据质量
quality = analyzer.assess_data_quality(data)
print("信噪比:", quality['snr'])

# 时频分析
tf_data = analyzer.time_frequency_analysis(data)
print("频率范围:", tf_data['frequencies'])

# 相位分析
phase_data = analyzer.phase_analysis(data)
print("PLV矩阵形状:", phase_data['plv_matrix'].shape)
``` 