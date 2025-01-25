# 进阶示例

本文档提供了一些进阶的使用示例，展示 EEG-Analyze 的高级功能。

## 1. 批处理多个数据文件

```python
import os
import numpy as np
from eeg_analyze import EEGAnalyzer, EEGVisualizer
from eeg_analyze.preprocessor import preprocess_eeg
from eeg_analyze.data_loader import loadEEGData

def batch_process_files(data_dir: str, output_dir: str):
    """批量处理多个EEG数据文件"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建分析器和可视化器
    analyzer = EEGAnalyzer(sample_rate=250)
    visualizer = EEGVisualizer(sample_rate=250)
    
    # 遍历数据文件
    for filename in os.listdir(data_dir):
        if filename.endswith('.npy'):
            # 加载数据
            data_path = os.path.join(data_dir, filename)
            data = loadEEGData(
                data_path=data_path,
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
            
            # 分析
            results = {}
            for i in range(len(processed_data)):
                segment = processed_data[i]
                
                # 时频分析
                tf_data = analyzer.time_frequency_analysis(segment)
                
                # 相位分析
                phase_data = analyzer.phase_analysis(segment)
                
                # 保存结果
                results[f'segment_{i}'] = {
                    'tf_data': tf_data,
                    'phase_data': phase_data
                }
            
            # 保存结果
            output_path = os.path.join(output_dir, f'results_{filename}')
            np.save(output_path, results)
```

## 2. 自定义预处理流程

```python
def custom_preprocessing(data: np.ndarray, sample_rate: int):
    """自定义预处理流程"""
    from scipy import signal
    
    # 1. 去除基线漂移
    nyquist = sample_rate / 2
    b_high, a_high = signal.butter(4, 0.5 / nyquist, btype='high')
    
    # 2. 陷波滤波器（去除工频干扰）
    b_notch, a_notch = signal.iirnotch(50, 30, sample_rate)
    
    processed_data = data.copy()
    for ch in range(data.shape[1]):
        # 高通滤波
        processed_data[:, ch] = signal.filtfilt(b_high, a_high, data[:, ch])
        # 陷波滤波
        processed_data[:, ch] = signal.filtfilt(b_notch, a_notch, processed_data[:, ch])
    
    return processed_data

# 使用自定义预处理
data = loadEEGData('sample_eeg.npy', window=2.0, frame=1.0, sample_rate=250)
processed_data = custom_preprocessing(data[0], sample_rate=250)
```

## 3. 高级可视化

```python
def plot_advanced_visualization(data: np.ndarray, sample_rate: int):
    """创建高级可视化图表"""
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    
    # 创建分析器和可视化器
    analyzer = EEGAnalyzer(sample_rate=sample_rate)
    
    # 计算各种特征
    tf_data = analyzer.time_frequency_analysis(data)
    phase_data = analyzer.phase_analysis(data)
    quality = analyzer.assess_data_quality(data)
    
    # 创建复杂布局
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(3, 3)
    
    # 1. 时域波形
    ax1 = fig.add_subplot(gs[0, :])
    time = np.arange(data.shape[0]) / sample_rate
    for ch in range(data.shape[1]):
        ax1.plot(time, data[:, ch] + ch * 3, label=f'Channel {ch+1}')
    ax1.set_title('时域波形')
    ax1.legend()
    
    # 2. 时频图
    ax2 = fig.add_subplot(gs[1, :2])
    ch_data = tf_data['channel_0']
    im = ax2.pcolormesh(ch_data['times'], ch_data['frequencies'],
                       ch_data['power'], shading='gouraud')
    ax2.set_title('时频分析 (Channel 1)')
    plt.colorbar(im, ax=ax2)
    
    # 3. 相位连接性
    ax3 = fig.add_subplot(gs[1, 2])
    im = ax3.imshow(phase_data['plv_matrix'], cmap='hot')
    ax3.set_title('相位连接性')
    plt.colorbar(im, ax=ax3)
    
    # 4. 质量指标
    ax4 = fig.add_subplot(gs[2, :])
    ax4.bar(range(len(quality['snr'])), quality['snr'])
    ax4.set_title('信噪比')
    ax4.set_xlabel('通道')
    ax4.set_ylabel('SNR (dB)')
    
    plt.tight_layout()
    return fig

# 使用高级可视化
fig = plot_advanced_visualization(processed_data, sample_rate=250)
fig.savefig('advanced_visualization.png')
```

## 4. 自定义特征提取

```python
def extract_custom_features(data: np.ndarray, sample_rate: int):
    """提取自定义特征"""
    from scipy import stats
    
    features = {}
    
    # 1. Hjorth参数
    diff1 = np.diff(data, axis=0)
    diff2 = np.diff(diff1, axis=0)
    
    activity = np.var(data, axis=0)
    mobility = np.sqrt(np.var(diff1, axis=0) / activity)
    complexity = np.sqrt(np.var(diff2, axis=0) / np.var(diff1, axis=0)) / mobility
    
    features['hjorth'] = {
        'activity': activity,
        'mobility': mobility,
        'complexity': complexity
    }
    
    # 2. 样本熵
    def sample_entropy(x, m=2, r=0.2):
        n = len(x)
        r = r * np.std(x)
        
        def _maxdist(x_i, x_j):
            return max([abs(x_i[k] - x_j[k]) for k in range(len(x_i))])
        
        def _phi(m):
            x = [[x[j] for j in range(i, i + m)] for i in range(n - m + 1)]
            C = [len([1 for j in range(len(x)) if i != j and _maxdist(x[i], x[j]) <= r])
                 for i in range(len(x))]
            return sum(C)
        
        return -np.log(_phi(m+1) / _phi(m))
    
    features['sample_entropy'] = np.array([
        sample_entropy(data[:, ch]) for ch in range(data.shape[1])
    ])
    
    return features

# 使用自定义特征提取
custom_features = extract_custom_features(processed_data, sample_rate=250)
```

## 5. 数据增强

```python
def advanced_augmentation(data: np.ndarray, sample_rate: int):
    """高级数据增强方法"""
    from scipy import signal
    
    augmented_data = []
    
    # 1. 添加高斯噪声
    noise = np.random.normal(0, 0.1, data.shape)
    augmented_data.append(data + noise)
    
    # 2. 时间拉伸
    stretch_factor = 1.2
    n_samples = int(data.shape[0] * stretch_factor)
    stretched_data = np.zeros((n_samples, data.shape[1]))
    for ch in range(data.shape[1]):
        stretched_data[:, ch] = signal.resample(data[:, ch], n_samples)
    augmented_data.append(stretched_data)
    
    # 3. 频率调制
    t = np.arange(data.shape[0]) / sample_rate
    modulation = np.sin(2 * np.pi * 0.5 * t)[:, np.newaxis]
    modulated_data = data * (1 + 0.1 * modulation)
    augmented_data.append(modulated_data)
    
    return augmented_data

# 使用高级数据增强
augmented_datasets = advanced_augmentation(processed_data, sample_rate=250)
```

## 下一步

- 查看[API文档](../api/analyzer.md)了解更多接口细节
- 阅读[开发指南](../guide/development.md)学习如何扩展功能
- 参考[贡献指南](../guide/contributing.md)参与项目开发 