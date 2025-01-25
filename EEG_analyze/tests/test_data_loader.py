"""
测试数据加载模块
"""
import os
import numpy as np
import pytest
from eeg_analyze.data_loader import loadEEGData, loadEEGCSV, loadEEGNPY, loadEEGEDF

def test_load_npy():
    # 生成测试数据
    data = np.random.randn(2500, 4)  # 10秒数据，250Hz采样率，4通道
    test_file = 'test_data.npy'
    np.save(test_file, data)
    
    try:
        # 测试数据加载
        loaded_data = loadEEGNPY(
            data_path=test_file,
            window=2.0,
            frame=1.0,
            sample_rate=250
        )
        
        # 验证数据形状
        assert loaded_data.shape[0] == 9  # 应该有9个段
        assert loaded_data.shape[1] == 500  # 每段2秒，250Hz采样率
        assert loaded_data.shape[2] == 4  # 4个通道
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_invalid_input():
    with pytest.raises(ValueError):
        # 测试无效的文件格式
        loadEEGData(
            data_path='invalid.txt',
            window=2.0,
            frame=1.0,
            sample_rate=250
        )

def test_window_too_large():
    # 生成测试数据
    data = np.random.randn(100, 4)  # 很短的数据
    test_file = 'test_data.npy'
    np.save(test_file, data)
    
    try:
        with pytest.raises(ValueError):
            # 测试窗口大小超过数据长度的情况
            loadEEGNPY(
                data_path=test_file,
                window=10.0,  # 太长的窗口
                frame=1.0,
                sample_rate=250
            )
    finally:
        if os.path.exists(test_file):
            os.remove(test_file) 