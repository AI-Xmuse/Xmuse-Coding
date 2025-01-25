# EEGVisualizer API 参考

## 类：EEGVisualizer

用于 EEG 数据可视化的类。

### 初始化参数

```python
EEGVisualizer(sample_rate: int)
```

- `sample_rate` (int): 采样率（Hz）

### 方法

#### plot_time_domain

绘制时域波形图。

```python
def plot_time_domain(
    self,
    data: np.ndarray,
    save_dir: str,
    title: str = "EEG时域波形",
    channel_names: list = None
)
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (samples, channels)
- `save_dir` (str): 保存目录
- `title` (str): 图标题
- `channel_names` (list): 通道名称列表

#### plot_psd

绘制功率谱密度图。

```python
def plot_psd(
    self,
    freqs: np.ndarray,
    psd: np.ndarray,
    save_dir: str,
    channel_names: list = None,
    title: str = "功率谱密度"
)
```

**参数：**
- `freqs` (np.ndarray): 频率数组
- `psd` (np.ndarray): 功率谱密度数组，形状为 (channels, frequencies)
- `save_dir` (str): 保存目录
- `channel_names` (list): 通道名称列表
- `title` (str): 图标题

#### plot_time_frequency

绘制时频图。

```python
def plot_time_frequency(
    self,
    tf_data: dict,
    save_dir: str,
    channel_idx: int = 0,
    title: str = "时频分析"
)
```

**参数：**
- `tf_data` (dict): 时频分析数据
- `save_dir` (str): 保存目录
- `channel_idx` (int): 要显示的通道索引
- `title` (str): 图标题

#### plot_brain_map

绘制脑地形图。

```python
def plot_brain_map(
    self,
    data: np.ndarray,
    save_dir: str,
    channel_positions: dict = None,
    title: str = "脑地形图"
)
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (channels,)
- `save_dir` (str): 保存目录
- `channel_positions` (dict): 通道位置字典
- `title` (str): 图标题

#### plot_comprehensive_view

绘制综合分析视图。

```python
def plot_comprehensive_view(
    self,
    data: np.ndarray,
    tf_data: dict,
    quality_metrics: dict,
    save_dir: str,
    channel_names: list = None
)
```

**参数：**
- `data` (np.ndarray): 输入数据，形状为 (samples, channels)
- `tf_data` (dict): 时频分析数据
- `quality_metrics` (dict): 质量指标数据
- `save_dir` (str): 保存目录
- `channel_names` (list): 通道名称列表

### 示例

```python
import numpy as np
from eeg_analyze import EEGVisualizer

# 创建可视化器实例
visualizer = EEGVisualizer(sample_rate=250)

# 生成示例数据
data = np.random.randn(1000, 4)  # 4秒数据，4通道
channel_names = ['Fp1', 'Fp2', 'F3', 'F4']

# 绘制时域波形
visualizer.plot_time_domain(
    data=data,
    save_dir='results',
    title='EEG时域波形',
    channel_names=channel_names
)

# 定义通道位置
channel_positions = {
    'Fp1': (-0.5, 0.5),
    'Fp2': (0.5, 0.5),
    'F3': (-0.5, -0.5),
    'F4': (0.5, -0.5)
}

# 绘制脑地形图
feature_values = np.random.rand(4)
visualizer.plot_brain_map(
    data=feature_values,
    save_dir='results',
    channel_positions=channel_positions,
    title='特征分布图'
) 