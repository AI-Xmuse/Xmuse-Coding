"""
基本的 EEG 分析示例
演示了如何加载数据、预处理、特征提取和可视化
"""

import numpy as np
from preprocessor import preprocess_eeg
from feature_extractor import extract_features
from analyzer import EEGAnalyzer
from visualizer import EEGVisualizer
from data_loader import loadEEGData

def main():
    # 参数设置
    sample_rate = 250  # Hz
    window = 2.0      # 窗口大小（秒）
    frame = 1.0       # 帧移大小（秒）
    
    # 加载数据
    print("加载数据...")
    data = loadEEGData(
        data_path='data/sample_eeg.npy',
        window=window,
        frame=frame,
        sample_rate=sample_rate
    )
    
    # 数据预处理
    print("数据预处理...")
    processed_data, preprocess_params = preprocess_eeg(
        data=data,
        methods=['clean', 'filter', 'normalize'],
        sample_rate=sample_rate
    )
    
    # 特征提取
    print("特征提取...")
    features = extract_features(processed_data, sample_rate)
    
    # 创建分析器和可视化器
    analyzer = EEGAnalyzer(sample_rate=sample_rate)
    visualizer = EEGVisualizer(sample_rate=sample_rate)
    
    # 时频分析
    print("进行时频分析...")
    tf_data = analyzer.time_frequency_analysis(processed_data[0])  # 分析第一段数据
    
    # 相位分析
    print("进行相位分析...")
    phase_data = analyzer.phase_analysis(processed_data[0])
    
    # 数据质量评估
    print("评估数据质量...")
    quality_metrics = analyzer.assess_data_quality(processed_data[0])
    
    # 可视化结果
    print("生成可视化结果...")
    # 1. 时域波形
    visualizer.plot_time_domain(
        data=processed_data[0],
        save_dir='results',
        title='EEG时域波形'
    )
    
    # 2. 时频图
    visualizer.plot_time_frequency(
        tf_data=tf_data,
        save_dir='results',
        title='时频分析结果'
    )
    
    # 3. 相位连接性
    visualizer.plot_phase_connectivity(
        plv_matrix=phase_data['plv_matrix'],
        save_dir='results',
        title='通道间相位连接性'
    )
    
    # 4. 综合视图
    visualizer.plot_comprehensive_view(
        data=processed_data[0],
        tf_data=tf_data,
        quality_metrics=quality_metrics,
        save_dir='results'
    )
    
    print("分析完成！结果已保存到 results 目录")

if __name__ == '__main__':
    main() 