"""
测试特征提取模块
"""
import numpy as np
from eeg_analyze.feature_extractor import extract_features, spectral_analysis

def test_spectral_analysis():
    """测试频谱分析"""
    # 生成测试数据
    sample_rate = 250
    duration = 4  # 秒
    t = np.linspace(0, duration, duration * sample_rate)
    
    # 生成包含已知频率的信号
    freq_10hz = np.sin(2 * np.pi * 10 * t)  # 10 Hz
    freq_20hz = 0.5 * np.sin(2 * np.pi * 20 * t)  # 20 Hz
    signal = freq_10hz + freq_20hz
    
    # 添加两个通道
    data = np.column_stack([signal, signal])
    
    # 进行频谱分析
    freqs, psd = spectral_analysis(data, sample_rate)
    
    # 验证结果
    assert len(freqs) > 0
    assert psd.shape[0] == data.shape[1]  # 通道数
    assert psd.shape[1] == len(freqs)  # 频率点数
    
    # 验证是否检测到主要频率成分
    peak_freqs = freqs[np.argmax(psd, axis=1)]
    assert any(np.abs(peak_freqs - 10) < 1)  # 10 Hz 附近有峰值

def test_extract_features():
    """测试特征提取"""
    # 生成测试数据
    n_segments = 5
    n_samples = 1000
    n_channels = 4
    sample_rate = 250
    
    data = np.random.randn(n_segments, n_samples, n_channels)
    
    # 提取特征
    features = extract_features(data, sample_rate)
    
    # 验证时域特征
    assert features['mean'].shape == (n_segments, n_channels)
    assert features['std'].shape == (n_segments, n_channels)
    assert features['var'].shape == (n_segments, n_channels)
    assert features['max'].shape == (n_segments, n_channels)
    assert features['min'].shape == (n_segments, n_channels)
    assert features['ptp'].shape == (n_segments, n_channels)
    assert features['skewness'].shape == (n_segments, n_channels)
    assert features['kurtosis'].shape == (n_segments, n_channels)
    assert features['rms'].shape == (n_segments, n_channels)
    assert features['energy'].shape == (n_segments, n_channels)
    assert features['zero_crossing_rate'].shape == (n_segments, n_channels)
    
    # 验证频域特征
    assert features['delta'].shape == (n_segments, n_channels)
    assert features['theta'].shape == (n_segments, n_channels)
    assert features['alpha'].shape == (n_segments, n_channels)
    assert features['beta'].shape == (n_segments, n_channels)
    assert features['gamma'].shape == (n_segments, n_channels)
    assert features['band_power'].shape == (n_segments, n_channels, 5)
    assert features['spectral_entropy'].shape == (n_segments, n_channels)
    assert features['median_frequency'].shape == (n_segments, n_channels)
    assert features['mean_frequency'].shape == (n_segments, n_channels)
    
    # 验证非线性特征
    assert features['hjorth'].shape == (n_segments, n_channels, 3)
    
    # 验证特征值的有效性
    assert not np.any(np.isnan(features['mean']))
    assert not np.any(np.isinf(features['mean']))
    assert np.all(features['std'] >= 0)
    assert np.all(features['energy'] >= 0)
    assert np.all(features['spectral_entropy'] >= 0) 