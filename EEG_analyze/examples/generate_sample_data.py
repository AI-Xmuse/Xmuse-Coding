"""
生成示例EEG数据用于测试
"""

import numpy as np
import os

def generate_sample_eeg():
    # 设置参数
    n_channels = 4
    sample_rate = 250  # Hz
    duration = 10      # 秒
    n_samples = duration * sample_rate
    
    # 生成时间序列
    t = np.linspace(0, duration, n_samples)
    
    # 生成各频段的信号
    delta = 0.5 * np.sin(2 * np.pi * 2 * t)   # 2 Hz (Delta)
    theta = 0.3 * np.sin(2 * np.pi * 6 * t)   # 6 Hz (Theta)
    alpha = 0.8 * np.sin(2 * np.pi * 10 * t)  # 10 Hz (Alpha)
    beta = 0.2 * np.sin(2 * np.pi * 20 * t)   # 20 Hz (Beta)
    
    # 合成信号
    signal = delta + theta + alpha + beta
    
    # 为每个通道添加不同的噪声和相位差
    data = np.zeros((n_samples, n_channels))
    for ch in range(n_channels):
        noise = 0.1 * np.random.randn(n_samples)
        phase_shift = ch * np.pi / 4
        data[:, ch] = signal * np.cos(phase_shift) + noise
    
    return data

def main():
    # 生成数据
    print("生成示例数据...")
    data = generate_sample_eeg()
    
    # 创建数据目录
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 保存数据
    data_path = os.path.join(data_dir, 'sample_eeg.npy')
    np.save(data_path, data)
    print(f"示例数据已保存到: {data_path}")
    print(f"数据形状: {data.shape}")

if __name__ == '__main__':
    main() 