"""
测试预处理模块
"""
import numpy as np
from eeg_analyze.preprocessor import preprocess_eeg, augment_eeg

def test_preprocess():
    # 生成测试数据
    data = np.random.randn(1000, 4)  # 4秒数据，250Hz采样率，4通道
    
    # 添加一些异常值
    data[100, 0] = np.nan
    data[200, 1] = np.inf
    data[300, 2] = -np.inf
    
    # 测试预处理
    processed_data, params = preprocess_eeg(
        data=data,
        methods=['clean', 'filter', 'normalize'],
        sample_rate=250
    )
    
    # 验证结果
    assert processed_data.shape == data.shape
    assert not np.any(np.isnan(processed_data))
    assert not np.any(np.isinf(processed_data))
    assert 'mean' in params
    assert 'std' in params

def test_augment():
    # 生成测试数据
    data = np.random.randn(1000, 4)
    
    # 测试噪声增强
    noisy_data = augment_eeg(
        data=data,
        method='noise',
        noise_level=0.1
    )
    assert noisy_data.shape == data.shape
    assert not np.array_equal(data, noisy_data)
    
    # 测试时间移位
    shifted_data = augment_eeg(
        data=data,
        method='shift',
        shift_range=10
    )
    assert shifted_data.shape == data.shape
    assert not np.array_equal(data, shifted_data)
    
    # 测试幅值缩放
    scaled_data = augment_eeg(
        data=data,
        method='scale',
        scale_range=(0.8, 1.2)
    )
    assert scaled_data.shape == data.shape
    assert not np.array_equal(data, scaled_data) 