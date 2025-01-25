# EEGProcessor API 参考

## 函数：preprocess_eeg

对 EEG 数据进行预处理。

```python
def preprocess_eeg(
    data: np.ndarray,
    methods: list = None,
    sample_rate: int = None
) -> Tuple[np.ndarray, dict]
```

### 参数
- `data` (np.ndarray): 输入数据，形状为 (segments, samples, channels) 或 (samples, channels)
- `methods` (list): 预处理方法列表，可包含：
  - 'clean': 清理无效值
  - 'normalize': Z-score标准化
  - 'filter': 带通滤波
  - 'detrend': 去趋势
- `sample_rate` (int): 采样率（Hz），在使用'filter'方法时必需

### 返回值
- `processed_data` (np.ndarray): 预处理后的数据
- `preprocess_params` (dict): 预处理参数字典，包含均值和标准差等信息

### 示例

```python
import numpy as np
from eeg_analyze.preprocessor import preprocess_eeg

# 生成示例数据
data = np.random.randn(1000, 4)  # 4秒数据，4通道

# 预处理数据
processed_data, params = preprocess_eeg(
    data=data,
    methods=['clean', 'filter', 'normalize'],
    sample_rate=250
)
```

## 函数：augment_eeg

对 EEG 数据进行数据增强。

```python
def augment_eeg(
    data: np.ndarray,
    method: str,
    **kwargs
) -> np.ndarray
```

### 参数
- `data` (np.ndarray): 输入数据，形状为 (segments, samples, channels)
- `method` (str): 增强方法
  - 'noise': 添加高斯噪声
  - 'shift': 时间移位
  - 'scale': 幅值缩放
- `**kwargs`: 其他参数
  - noise_level (float): 噪声水平（用于'noise'方法）
  - shift_range (int): 移位范围（用于'shift'方法）
  - scale_range (tuple): 缩放范围（用于'scale'方法）

### 返回值
- `augmented_data` (np.ndarray): 增强后的数据

### 示例

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

# 幅值缩放
scaled_data = augment_eeg(
    data=processed_data,
    method='scale',
    scale_range=(0.8, 1.2)
)
```

## 函数：save_eeg_data

保存处理后的 EEG 数据。

```python
def save_eeg_data(
    data: np.ndarray,
    save_path: str,
    format: str = 'npy'
)
```

### 参数
- `data` (np.ndarray): 要保存的数据
- `save_path` (str): 保存路径
- `format` (str): 保存格式，支持'npy'和'csv'

### 示例

```python
from eeg_analyze.preprocessor import save_eeg_data

# 保存为 NPY 格式
save_eeg_data(processed_data, 'processed_data.npy', format='npy')

# 保存为 CSV 格式
save_eeg_data(processed_data, 'processed_data.csv', format='csv')
``` 