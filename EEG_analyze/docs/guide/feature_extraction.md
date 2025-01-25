# 特征提取

## 支持的特征

EEG-Analyze 支持提取以下特征：

### 时域特征
- 均值
- 标准差
- 方差
- 最大值/最小值
- 峰峰值
- 偏度
- 峰度
- 均方根
- 能量
- 过零率

### 频域特征
- 各频段能量
  - Delta (0.5-4 Hz)
  - Theta (4-8 Hz)
  - Alpha (8-13 Hz)
  - Beta (13-30 Hz)
  - Gamma (30-100 Hz)
- 频段能量占比
- 谱熵
- 中值频率
- 平均频率

### 非线性特征
- Hjorth 参数
  - Activity
  - Mobility
  - Complexity

## 使用示例

```python
from eeg_analyze.feature_extractor import extract_features

# 提取特征
features = extract_features(data, sample_rate=250)

# 访问特征
print("Delta频段能量:", features['delta'])
print("Alpha/Beta比值:", features['alpha'] / features['beta'])
```

## 频谱分析

```python
from eeg_analyze.feature_extractor import spectral_analysis

# 计算功率谱密度
freqs, psd = spectral_analysis(
    data=eeg_data,
    sample_rate=250,
    window='hann'
)
```

## 特征选择建议

1. 时域特征
   - 适用于快速变化的信号特征
   - 计算简单，实时性好
   - 易受噪声影响

2. 频域特征
   - 反映信号的频率组成
   - 对应不同脑电节律
   - 需要较长时间窗口

3. 非线性特征
   - 描述信号的复杂性
   - 反映脑电的非线性特性
   - 计算量较大

## 注意事项

1. 特征提取前确保数据已经过预处理
2. 根据应用场景选择合适的特征
3. 考虑计算效率和实时性要求
4. 注意特征的可解释性 