import numpy as np
from scipy import signal
from scipy import stats


def spectral_analysis(data: np.ndarray, sample_rate: int, window: str = 'hann'):
    """
    Description: EEG频域分析
    -------------------------------
    Parameters:
    data: 输入数据，形状为(samples, channels)或(segments, samples, channels)
    sample_rate: 采样率
    window: 窗函数类型

    Returns:
    freqs: 频率数组
    psd: 功率谱密度，形状为(channels, frequencies)
    """
    if len(data.shape) == 3:
        # 如果是分段数据，计算平均功率谱
        freqs = None
        psd_sum = None

        for i in range(data.shape[0]):
            for ch in range(data.shape[2]):
                f, p = signal.welch(data[i, :, ch], fs=sample_rate, window=window,
                                    nperseg=min(256, data.shape[1]))
                if psd_sum is None:
                    freqs = f
                    psd_sum = np.zeros((data.shape[2], len(f)))
                psd_sum[ch] += p

        psd = psd_sum / data.shape[0]
    else:
        # 对每个通道分别计算功率谱
        freqs = None
        psd = None

        for ch in range(data.shape[1]):
            f, p = signal.welch(data[:, ch], fs=sample_rate, window=window,
                                nperseg=min(256, data.shape[0]))
            if psd is None:
                freqs = f
                psd = np.zeros((data.shape[1], len(f)))
            psd[ch] = p

    return freqs, psd


def extract_features(data: np.ndarray, sample_rate: int):
    """
    Description: 提取EEG特征
    -------------------------------
    Parameters:
    data: 输入数据，形状为(segments, samples, channels)
    sample_rate: 采样率

    Returns:
    features: 特征字典
    """
    features = {}

    # 时域特征
    features['mean'] = np.mean(data, axis=1)  # 平均值
    features['std'] = np.std(data, axis=1)    # 标准差
    features['var'] = np.var(data, axis=1)    # 方差
    features['max'] = np.max(data, axis=1)    # 最大值
    features['min'] = np.min(data, axis=1)    # 最小值
    features['ptp'] = np.ptp(data, axis=1)    # 峰峰值
    features['skewness'] = stats.skew(data, axis=1)  # 偏度
    features['kurtosis'] = stats.kurtosis(data, axis=1)  # 峰度
    features['rms'] = np.sqrt(np.mean(np.square(data), axis=1))  # 均方根
    features['energy'] = np.sum(np.square(data), axis=1)  # 能量

    # 计算过零率
    zero_crosses = np.diff(np.signbit(data), axis=1).sum(axis=1)
    features['zero_crossing_rate'] = zero_crosses / (data.shape[1] - 1)

    # 频域特征
    features['delta'] = np.zeros((data.shape[0], data.shape[2]))  # (0.5-4 Hz)
    features['theta'] = np.zeros((data.shape[0], data.shape[2]))  # (4-8 Hz)
    features['alpha'] = np.zeros((data.shape[0], data.shape[2]))  # (8-13 Hz)
    features['beta'] = np.zeros((data.shape[0], data.shape[2]))   # (13-30 Hz)
    features['gamma'] = np.zeros((data.shape[0], data.shape[2]))  # (30-100 Hz)
    features['band_power'] = np.zeros((data.shape[0], data.shape[2], 5))  # 各频段能量
    features['spectral_entropy'] = np.zeros((data.shape[0], data.shape[2]))  # 谱熵
    features['median_frequency'] = np.zeros((data.shape[0], data.shape[2]))  # 中值频率
    features['mean_frequency'] = np.zeros((data.shape[0], data.shape[2]))    # 平均频率

    for i in range(data.shape[0]):  # 对每个片段
        freqs, psd = spectral_analysis(data[i], sample_rate)  # psd shape: (channels, frequencies)

        # 提取各频段能量
        delta_mask = (freqs >= 0.5) & (freqs <= 4)
        theta_mask = (freqs >= 4) & (freqs <= 8)
        alpha_mask = (freqs >= 8) & (freqs <= 13)
        beta_mask = (freqs >= 13) & (freqs <= 30)
        gamma_mask = (freqs >= 30) & (freqs <= 100)

        # 计算各频段能量
        for ch in range(data.shape[2]):
            features['delta'][i, ch] = np.sum(psd[ch, delta_mask])
            features['theta'][i, ch] = np.sum(psd[ch, theta_mask])
            features['alpha'][i, ch] = np.sum(psd[ch, alpha_mask])
            features['beta'][i, ch] = np.sum(psd[ch, beta_mask])
            features['gamma'][i, ch] = np.sum(psd[ch, gamma_mask])
            
            # 计算频段能量占比
            total_power = np.sum(psd[ch])
            features['band_power'][i, ch] = [
                features['delta'][i, ch] / total_power,
                features['theta'][i, ch] / total_power,
                features['alpha'][i, ch] / total_power,
                features['beta'][i, ch] / total_power,
                features['gamma'][i, ch] / total_power
            ]
            
            # 计算谱熵
            psd_norm = psd[ch] / np.sum(psd[ch])
            features['spectral_entropy'][i, ch] = -np.sum(psd_norm * np.log2(psd_norm + 1e-10))
            
            # 计算中值频率和平均频率
            cumsum = np.cumsum(psd[ch])
            features['median_frequency'][i, ch] = freqs[np.where(cumsum >= cumsum[-1]/2)[0][0]]
            features['mean_frequency'][i, ch] = np.sum(freqs * psd[ch]) / np.sum(psd[ch])

    # 非线性特征
    features['hjorth'] = np.zeros((data.shape[0], data.shape[2], 3))  # Hjorth参数

    for i in range(data.shape[0]):
        for ch in range(data.shape[2]):
            # Hjorth参数
            activity, mobility, complexity = hjorth_parameters(data[i, :, ch])
            features['hjorth'][i, ch] = [activity, mobility, complexity]



    return features


def nonlinear_features(data: np.ndarray):
    """
    Description: 提取EEG非线性特征
    -------------------------------
    Parameters:
    data: 输入数据，形状为(samples, channels)

    Returns:
    features: 非线性特征字典
    """
    features = {}

    for ch in range(data.shape[1]):


        # Hjorth参数
        activity, mobility, complexity = hjorth_parameters(data[:, ch])
        features[f'hjorth_activity_ch{ch}'] = activity
        features[f'hjorth_mobility_ch{ch}'] = mobility
        features[f'hjorth_complexity_ch{ch}'] = complexity


    return features


def hjorth_parameters(x):
    """计算Hjorth参数"""
    dx = np.diff(x)
    ddx = np.diff(dx)

    activity = np.var(x)
    mobility = np.sqrt(np.var(dx) / activity)
    complexity = np.sqrt(np.var(ddx) / np.var(dx)) / mobility

    return activity, mobility, complexity




