# 数据预处理

## 预处理流程

EEG-Analyze 提供了完整的预处理流程，包括：

1. 数据清理
   - 去除无效值
   - 异常值检测和处理
   - 基线漂移校正

2. 滤波
   - 高通滤波（去除基线漂移）
   - 低通滤波（去除高频噪声）
   - 带通滤波（提取特定频段）

3. 标准化
   - Z-score 标准化
   - Min-Max 归一化

## 使用示例

```python
from eeg_analyze.preprocessor import preprocess_eeg

# 预处理数据
processed_data, params = preprocess_eeg(
    data=raw_data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=250  # Hz
)
```

## 参数说明

### methods 参数
- 'clean': 清理无效值和异常值
- 'filter': 带通滤波 (0.5-45Hz)
- 'normalize': Z-score 标准化
- 'detrend': 去趋势

### 返回值
- processed_data: 预处理后的数据
- params: 预处理参数，包含均值和标准差等信息

## 数据增强

```python
from eeg_analyze.preprocessor import augment_eeg

# 添加高斯噪声
augmented_data = augment_eeg(
    data=processed_data,
    method='noise',
    noise_level=0.1
)
```

## 注意事项

1. 建议按照以下顺序进行预处理：
   - 首先进行数据清理
   - 然后进行滤波
   - 最后进行标准化

2. 滤波时需要注意：
   - 采样率应至少是目标频率的2倍
   - 避免过度滤波导致信息丢失

3. 标准化注意事项：
   - 对每个通道分别进行标准化
   - 保存标准化参数以便后续使用 