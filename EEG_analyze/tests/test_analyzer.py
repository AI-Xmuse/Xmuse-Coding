"""
测试分析器模块
"""
import numpy as np
from eeg_analyze.analyzer import EEGAnalyzer

class TestAnalyzer:
    @classmethod
    def setup_class(cls):
        """测试开始前的设置"""
        cls.sample_rate = 250
        cls.analyzer = EEGAnalyzer(sample_rate=cls.sample_rate)
        
        # 生成测试数据
        cls.data = np.random.randn(1000, 4)  # 4秒数据，4通道
    
    def test_assess_data_quality(self):
        """测试数据质量评估"""
        quality_metrics = self.analyzer.assess_data_quality(self.data)
        
        assert 'missing_ratio' in quality_metrics
        assert 'snr' in quality_metrics
        assert 'baseline_drift' in quality_metrics
        assert len(quality_metrics['snr']) == self.data.shape[1]
    
    def test_time_frequency_analysis(self):
        """测试时频分析"""
        tf_data = self.analyzer.time_frequency_analysis(
            data=self.data,
            window_size=1.0,
            overlap=0.5
        )
        
        # 验证返回的时频数据
        for ch in range(self.data.shape[1]):
            ch_data = tf_data[f'channel_{ch}']
            assert 'frequencies' in ch_data
            assert 'times' in ch_data
            assert 'power' in ch_data
            assert ch_data['power'].shape[0] == len(ch_data['frequencies'])
            assert ch_data['power'].shape[1] == len(ch_data['times'])
    
    def test_phase_analysis(self):
        """测试相位分析"""
        phase_data = self.analyzer.phase_analysis(
            data=self.data,
            freq_band=(8, 13)  # Alpha频段
        )
        
        # 验证相位锁定值矩阵
        plv_matrix = phase_data['plv_matrix']
        assert plv_matrix.shape == (self.data.shape[1], self.data.shape[1])
        assert np.all(plv_matrix >= 0) and np.all(plv_matrix <= 1)
        assert np.allclose(plv_matrix, plv_matrix.T)  # 对称矩阵
        assert np.allclose(np.diag(plv_matrix), 1)  # 对角线为1 