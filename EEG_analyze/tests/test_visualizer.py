"""
测试可视化模块
"""
import os
import shutil
import numpy as np
from eeg_analyze.visualizer import EEGVisualizer
from eeg_analyze.analyzer import EEGAnalyzer

class TestVisualizer:
    @classmethod
    def setup_class(cls):
        """测试开始前的设置"""
        cls.test_dir = 'test_results'
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.sample_rate = 250
        cls.visualizer = EEGVisualizer(sample_rate=cls.sample_rate)
        
        # 生成测试数据
        cls.data = np.random.randn(1000, 4)  # 4秒数据，4通道
        cls.channel_names = ['Fp1', 'Fp2', 'F3', 'F4']
        
        # 生成时频数据
        analyzer = EEGAnalyzer(sample_rate=cls.sample_rate)
        cls.tf_data = analyzer.time_frequency_analysis(cls.data)
        cls.quality_metrics = analyzer.assess_data_quality(cls.data)
    
    @classmethod
    def teardown_class(cls):
        """测试结束后的清理"""
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
    
    def test_plot_time_domain(self):
        """测试时域波形图绘制"""
        self.visualizer.plot_time_domain(
            data=self.data,
            save_dir=self.test_dir,
            title='测试时域波形',
            channel_names=self.channel_names
        )
        assert os.path.exists(os.path.join(self.test_dir, 'time_domain.png'))
    
    def test_plot_psd(self):
        """测试功率谱密度图绘制"""
        freqs = np.linspace(0, self.sample_rate/2, 100)
        psd = np.random.rand(4, 100)  # 4通道，100个频率点
        
        self.visualizer.plot_psd(
            freqs=freqs,
            psd=psd,
            save_dir=self.test_dir,
            channel_names=self.channel_names,
            title='测试功率谱密度'
        )
        assert os.path.exists(os.path.join(self.test_dir, 'psd.png'))
    
    def test_plot_time_frequency(self):
        """测试时频图绘制"""
        self.visualizer.plot_time_frequency(
            tf_data=self.tf_data,
            save_dir=self.test_dir,
            channel_idx=0,
            title='测试时频分析'
        )
        assert os.path.exists(os.path.join(self.test_dir, 'time_frequency_ch1.png'))
    
    def test_plot_brain_map(self):
        """测试脑地形图绘制"""
        channel_positions = {
            'Fp1': (-0.5, 0.5),
            'Fp2': (0.5, 0.5),
            'F3': (-0.5, -0.5),
            'F4': (0.5, -0.5)
        }
        
        feature_values = np.random.rand(4)  # 4个通道的特征值
        
        self.visualizer.plot_brain_map(
            data=feature_values,
            save_dir=self.test_dir,
            channel_positions=channel_positions,
            title='测试脑地形图'
        )
        assert os.path.exists(os.path.join(self.test_dir, 'brain_map.png'))
    
    def test_plot_comprehensive_view(self):
        """测试综合视图绘制"""
        self.visualizer.plot_comprehensive_view(
            data=self.data,
            tf_data=self.tf_data,
            quality_metrics=self.quality_metrics,
            save_dir=self.test_dir,
            channel_names=self.channel_names
        )
        assert os.path.exists(os.path.join(self.test_dir, 'comprehensive_view.png'))
    
    def test_chinese_support(self):
        """测试中文支持"""
        self.visualizer.plot_time_domain(
            data=self.data,
            save_dir=self.test_dir,
            title='测试中文标题支持',
            channel_names=['通道1', '通道2', '通道3', '通道4']
        )
        assert os.path.exists(os.path.join(self.test_dir, 'time_domain.png')) 