import numpy as np
from scipy import signal


def preprocess_eeg(data: np.ndarray, methods: list = None, sample_rate: int = None):
    """
    Description: EEG数据预处理函数
    -------------------------------
    Parameters:
    data: 输入数据，形状为(segments, samples, channels)或(samples, channels)
    methods: 预处理方法列表，可包含：
            - 'clean': 清理无效值
            - 'normalize': Z-score标准化
            - 'filter': 带通滤波
            - 'detrend': 去趋势
    sample_rate: 采样率（Hz），在使用'filter'方法时必需

    Returns:
    processed_data: 预处理后的数据
    preprocess_params: 预处理参数字典，包含均值和标准差等信息
    """
    if methods is None:
        return data, {}

    if len(data.shape) == 0 or 0 in data.shape:
        raise ValueError("输入数据形状无效")

    processed_data = data.copy()
    original_shape = processed_data.shape
    preprocess_params = {}

    # 打印输入数据的基本信息
    print("\n输入数据信息:")
    print(f"数据形状: {data.shape}")
    print(f"数据类型: {data.dtype}")
    print(f"是否包含NaN: {np.any(np.isnan(data))}")
    print(f"是否包含Inf: {np.any(np.isinf(data))}")
    
    # 如果输入是3D数据(segments, samples, channels)，转换为2D(samples, channels)
    if len(original_shape) == 3:
        processed_data = processed_data.reshape(-1, original_shape[-1])
        print(f"展平后的形状: {processed_data.shape}")

    # 首先进行数据清理
    # 1. 替换无限值为0
    processed_data[~np.isfinite(processed_data)] = 0
    
    # 2. 移除异常值（超过均值±5个标准差的值）
    for ch in range(processed_data.shape[1]):
        channel_data = processed_data[:, ch]
        mean_val = np.mean(channel_data[np.isfinite(channel_data)])
        std_val = np.std(channel_data[np.isfinite(channel_data)])
        outlier_mask = np.abs(channel_data - mean_val) > 5 * std_val
        processed_data[outlier_mask, ch] = mean_val

    # 记录原始数据的统计参数（使用清理后的数据）
    mean = np.mean(processed_data, axis=0, keepdims=True)
    std = np.std(processed_data, axis=0, keepdims=True)
    
    # 确保统计参数有效
    if np.any(np.isnan(mean)) or np.any(np.isnan(std)):
        print("警告：统计参数包含NaN，使用替代值")
        mean[np.isnan(mean)] = 0
        std[np.isnan(std)] = 1
    
    preprocess_params['mean'] = mean.squeeze()
    preprocess_params['std'] = std.squeeze()

    print("\n预处理参数:")
    print(f"均值: {preprocess_params['mean']}")
    print(f"标准差: {preprocess_params['std']}")

    for method in methods:
        if method == 'filter':
            if sample_rate is None:
                raise ValueError("使用'filter'方法时必须提供sample_rate参数")
            
            # 首先进行高通滤波去除基线漂移 (0.5 Hz)
            nyquist = sample_rate / 2
            b_high, a_high = signal.butter(4, 0.5 / nyquist, btype='high')
            
            # 然后进行低通滤波去除高频噪声 (45 Hz)
            b_low, a_low = signal.butter(4, 45 / nyquist, btype='low')
            
            # 对每个通道分别进行滤波
            for ch in range(processed_data.shape[1]):
                # 先进行高通滤波
                temp_data = signal.filtfilt(b_high, a_high, processed_data[:, ch])
                # 再进行低通滤波
                processed_data[:, ch] = signal.filtfilt(b_low, a_low, temp_data)

        elif method == 'detrend':
            # 去趋势
            for ch in range(processed_data.shape[1]):
                # 确保数据是有限值
                channel_data = processed_data[:, ch]
                if np.all(np.isfinite(channel_data)):
                    # 使用多项式拟合去除趋势
                    t = np.arange(len(channel_data))
                    p = np.polyfit(t, channel_data, 3)  # 使用3阶多项式
                    trend = np.polyval(p, t)
                    processed_data[:, ch] = channel_data - trend

        elif method == 'normalize':
            # Z-score标准化
            curr_mean = np.mean(processed_data, axis=0, keepdims=True)
            curr_std = np.std(processed_data, axis=0, keepdims=True)
            # 避免除以0
            curr_std[curr_std == 0] = 1
            processed_data = (processed_data - curr_mean) / curr_std

    # 最后再次检查并清理可能产生的无效值
    processed_data[~np.isfinite(processed_data)] = 0

    # 恢复原始形状
    if len(original_shape) == 3:
        processed_data = processed_data.reshape(original_shape)

    # 打印处理后的数据信息
    print("\n处理后数据信息:")
    print(f"数据范围: [{np.min(processed_data):.2f}, {np.max(processed_data):.2f}]")
    print(f"是否包含NaN: {np.any(np.isnan(processed_data))}")
    print(f"是否包含Inf: {np.any(np.isinf(processed_data))}")

    return processed_data, preprocess_params


def augment_eeg(data: np.ndarray, method: str, **kwargs):
    """
    Description: EEG数据增强函数
    -------------------------------
    Parameters:
    data: 输入数据，形状为(segments, samples, channels)
    method: 增强方法
           - 'noise': 添加高斯噪声
           - 'shift': 时间移位
           - 'scale': 幅值缩放

    Returns:
    augmented_data: 增强后的数据
    """
    if method == 'noise':
        noise_level = kwargs.get('noise_level', 0.1)
        noise = np.random.normal(0, noise_level, data.shape)
        return data + noise

    elif method == 'shift':
        shift_range = kwargs.get('shift_range', 10)
        shift = np.random.randint(-shift_range, shift_range)
        return np.roll(data, shift, axis=1)

    elif method == 'scale':
        scale_range = kwargs.get('scale_range', (0.8, 1.2))
        scale = np.random.uniform(scale_range[0], scale_range[1])
        return data * scale


def save_eeg_data(data: np.ndarray, save_path: str, format: str = 'npy'):
    """
    Description: 保存处理后的EEG数据
    -------------------------------
    Parameters:
    data: 要保存的数据
    save_path: 保存路径
    format: 保存格式，支持'npy'和'csv'
    """
    if format == 'npy':
        np.save(save_path, data)
    elif format == 'csv':
        np.savetxt(save_path, data, delimiter=',')