"""
EEG信号分析模块

该模块提供了EEG信号分析的核心功能,包括:
- 数据质量评估
- 时频分析 
- 相位分析

主要类:
- EEGAnalyzer: EEG信号分析器类
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


class EEGAnalyzer:
    def __init__(self, sample_rate: int):
        """
        Description: EEG分析器类
        -------------------------------
        Parameters:
        sample_rate: 采样率
        """
        self.sample_rate = sample_rate

    def assess_data_quality(self, data: np.ndarray):
        """
        Description: 评估EEG数据质量
        -------------------------------
        Parameters:
        data: 输入数据，形状为(samples, channels)或(segments, samples, channels)

        Returns:
        quality_metrics: 质量指标字典
        """
        if len(data.shape) == 3:
            data = np.mean(data, axis=0)  # 如果是分段数据，取平均

        quality_metrics = {}

        # 计算缺失值比例
        missing_ratio = np.mean(np.isnan(data))
        quality_metrics['missing_ratio'] = missing_ratio

        # 计算信噪比
        signal_power = np.mean(np.square(data), axis=0)
        noise_power = np.var(data, axis=0)
        snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
        quality_metrics['snr'] = snr

        # 计算基线漂移
        baseline_drift = np.mean(np.abs(np.diff(np.mean(data, axis=1))))
        quality_metrics['baseline_drift'] = baseline_drift

        return quality_metrics

    def time_frequency_analysis(self, data: np.ndarray, window_size: float = 1.0,
                                overlap: float = 0.5, freq_range: tuple = (0.5, 50)):
        """
        Description: 时频分析
        -------------------------------
        Parameters:
        data: 输入数据，形状为(samples, channels)
        window_size: 窗口大小(秒)
        overlap: 重叠比例
        freq_range: 频率范围(Hz)

        Returns:
        tf_data: 时频数据字典
        """
        tf_data = {}

        # 计算STFT参数
        nperseg = int(window_size * self.sample_rate)
        noverlap = int(nperseg * overlap)

        for ch in range(data.shape[1]):
            # 短时傅里叶变换
            f, t, Zxx = signal.stft(data[:, ch], fs=self.sample_rate,
                                    nperseg=nperseg, noverlap=noverlap)

            # 提取指定频率范围
            mask = (f >= freq_range[0]) & (f <= freq_range[1])
            tf_data[f'channel_{ch}'] = {
                'frequencies': f[mask],
                'times': t,
                'power': np.abs(Zxx[mask, :])
            }

        return tf_data

    def phase_analysis(self, data: np.ndarray, freq_band: tuple = (8, 13)):
        """
        Description: 相位分析
        -------------------------------
        Parameters:
        data: 输入数据，形状为(samples, channels)
        freq_band: 感兴趣的频段范围(Hz)

        Returns:
        phase_data: 相位数据字典
        """
        phase_data = {}
        n_channels = data.shape[1]

        # 计算相位锁定值(PLV)矩阵
        plv_matrix = np.zeros((n_channels, n_channels))

        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                # 带通滤波
                b, a = signal.butter(4, [freq_band[0], freq_band[1]],
                                     btype='band', fs=self.sample_rate)
                sig1 = signal.filtfilt(b, a, data[:, i])
                sig2 = signal.filtfilt(b, a, data[:, j])

                # 希尔伯特变换获取相位
                phase1 = np.angle(signal.hilbert(sig1))
                phase2 = np.angle(signal.hilbert(sig2))

                # 计算相位差
                phase_diff = phase1 - phase2

                # 计算PLV
                plv = np.abs(np.mean(np.exp(1j * phase_diff)))
                plv_matrix[i, j] = plv
                plv_matrix[j, i] = plv

        phase_data['plv_matrix'] = plv_matrix

        return phase_data