import numpy as np
import os
import pandas as pd
from data_loader import loadEEGData
from preprocessor import preprocess_eeg, augment_eeg
from feature_extractor import extract_features, spectral_analysis
from analyzer import EEGAnalyzer
from visualizer import EEGVisualizer


class EEGProcessor:
    def __init__(self, sample_rate: int = 256):
        """
        Description: EEG处理器主类
        -------------------------------
        Parameters:
        sample_rate: 采样率，默认256Hz
        """
        self.sample_rate = sample_rate
        self.analyzer = EEGAnalyzer(sample_rate)
        self.visualizer = EEGVisualizer(sample_rate)

    def process_file(self, file_path: str, window_size: float = 2.0,
                     overlap: float = 0.5, preprocess_methods: list = None):
        """
        Description: 处理单个EEG文件
        -------------------------------
        Parameters:
        file_path: EEG文件路径
        window_size: 窗口大小(秒)
        overlap: 重叠比例
        preprocess_methods: 预处理方法列表

        Returns:
        results: 处理结果字典
        """
        try:
            # 1. 加载数据
            print(f"正在加载数据: {file_path}")
            data = loadEEGData(file_path, window_size, overlap, self.sample_rate,channels=4)

            # 2. 预处理
            print("正在进行预处理...")
            if preprocess_methods is None:
                preprocess_methods = ['filter', 'normalize']
            processed_data, preprocess_params = preprocess_eeg(data, preprocess_methods, self.sample_rate)

            # 3. 特征提取
            print("正在提取特征...")
            features = extract_features(processed_data, self.sample_rate)

            # 4. 数据质量评估
            print("正在评估数据质量...")
            quality_metrics = self.analyzer.assess_data_quality(processed_data)

            # 5. 时频分析
            print("正在进行时频分析...")
            tf_data = self.analyzer.time_frequency_analysis(
                processed_data.reshape(-1, processed_data.shape[-1])
            )

            # 6. 相位分析
            print("正在进行相位分析...")
            phase_data = self.analyzer.phase_analysis(
                processed_data.reshape(-1, processed_data.shape[-1])
            )

            # 7. 可视化结果
            print("正在生成可视化结果...")
            output_dir = os.path.join("results", os.path.splitext(os.path.basename(file_path))[0])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            self._visualize_results(processed_data, tf_data, quality_metrics, output_dir)

            # 8. 保存结果
            print("正在保存结果...")
            
            # 保存原始幅值的预处理数据
            if 'mean' in preprocess_params and 'std' in preprocess_params:
                # 恢复原始幅值
                original_scale_data = processed_data.copy()
                if len(original_scale_data.shape) == 3:
                    # 对于3D数据，需要对每个片段分别处理
                    for i in range(original_scale_data.shape[0]):
                        original_scale_data[i] = original_scale_data[i] * preprocess_params['std'] + preprocess_params['mean']
                else:
                    original_scale_data = original_scale_data * preprocess_params['std'] + preprocess_params['mean']
                
                # 打印调试信息
                print("\n数据统计信息:")
                print(f"原始数据均值: {preprocess_params['mean']}")
                print(f"原始数据标准差: {preprocess_params['std']}")
                print(f"处理后数据形状: {original_scale_data.shape}")
                
                # 保存为CSV文件
                if len(original_scale_data.shape) == 3:
                    # 如果是分段数据，保存第一段作为示例
                    save_data = original_scale_data[0]
                    print(f"保存第一段数据，形状: {save_data.shape}")
                else:
                    save_data = original_scale_data
                    print(f"保存数据形状: {save_data.shape}")
                
                # 检查数据是否包含有效值
                if np.any(np.isfinite(save_data)):
                    processed_df = pd.DataFrame(save_data,
                                             columns=[f'Channel_{i+1}' for i in range(save_data.shape[1])])
                    
                    # 打印数据范围
                    print("\n各通道数据范围:")
                    for ch in range(save_data.shape[1]):
                        ch_data = save_data[:, ch]
                        print(f"Channel_{ch+1}: {np.min(ch_data):.2f} to {np.max(ch_data):.2f}")
                    
                    # 保存CSV文件
                    csv_path = os.path.join(output_dir, 'processed_data_original_scale.csv')
                    processed_df.to_csv(csv_path, index=False, float_format='%.6f')
                    print(f"\nCSV文件已保存到: {csv_path}")
                    
                    # 验证保存的CSV文件
                    try:
                        test_df = pd.read_csv(csv_path)
                        print(f"CSV文件验证 - 形状: {test_df.shape}")
                        print("CSV文件前5行:")
                        print(test_df.head())
                    except Exception as e:
                        print(f"CSV文件验证失败: {str(e)}")
                else:
                    print("警告：数据全部为无效值，跳过保存CSV文件")
                
                # 保存为NPY文件（保存完整数据）
                npy_path = os.path.join(output_dir, 'processed_data_original_scale.npy')
                np.save(npy_path, original_scale_data)
                print(f"\nNPY文件已保存到: {npy_path}")
                
                # 验证保存的NPY文件
                try:
                    test_data = np.load(npy_path)
                    print(f"NPY文件验证 - 形状: {test_data.shape}")
                except Exception as e:
                    print(f"NPY文件验证失败: {str(e)}")
            else:
                print("警告：未找到预处理参数，无法恢复原始幅值")
            
            # 保存时域特征
            time_features_df = pd.DataFrame({
                'mean': features['mean'].mean(axis=0),
                'std': features['std'].mean(axis=0),
                'var': features['var'].mean(axis=0),
                'max': features['max'].mean(axis=0),
                'min': features['min'].mean(axis=0),
                'ptp': features['ptp'].mean(axis=0),
                'skewness': features['skewness'].mean(axis=0),
                'kurtosis': features['kurtosis'].mean(axis=0),
                'rms': features['rms'].mean(axis=0),
                'energy': features['energy'].mean(axis=0),
                'zero_crossing_rate': features['zero_crossing_rate'].mean(axis=0)
            })
            time_features_df.to_csv(os.path.join(output_dir, 'time_features.csv'))

            # 保存频域特征
            freq_features_df = pd.DataFrame({
                'delta': features['delta'].mean(axis=0),
                'theta': features['theta'].mean(axis=0),
                'alpha': features['alpha'].mean(axis=0),
                'beta': features['beta'].mean(axis=0),
                'gamma': features['gamma'].mean(axis=0),
                'spectral_entropy': features['spectral_entropy'].mean(axis=0),
                'median_frequency': features['median_frequency'].mean(axis=0),
                'mean_frequency': features['mean_frequency'].mean(axis=0)
            })
            freq_features_df.to_csv(os.path.join(output_dir, 'frequency_features.csv'))

            # 保存频段能量比
            band_power_df = pd.DataFrame(
                features['band_power'].mean(axis=0),
                columns=['delta_ratio', 'theta_ratio', 'alpha_ratio', 'beta_ratio', 'gamma_ratio']
            )
            band_power_df.to_csv(os.path.join(output_dir, 'band_power_ratio.csv'))

            # 保存非线性特征
            nonlinear_features_df = pd.DataFrame({
                'activity': features['hjorth'].mean(axis=0)[:, 0],
                'mobility': features['hjorth'].mean(axis=0)[:, 1],
                'complexity': features['hjorth'].mean(axis=0)[:, 2],
            })
            nonlinear_features_df.to_csv(os.path.join(output_dir, 'nonlinear_features.csv'))

            # 保存质量指标
            quality_df = pd.DataFrame({
                'missing_ratio': [quality_metrics['missing_ratio']],
                'average_snr': [np.mean(quality_metrics['snr'])],
                'baseline_drift': [quality_metrics['baseline_drift']]
            })
            quality_df.to_csv(os.path.join(output_dir, 'quality_metrics.csv'))

            # 保存预处理参数
            if preprocess_params:
                np.save(os.path.join(output_dir, 'preprocess_params.npy'), preprocess_params)

            # 整理返回结果
            results = {
                'data': processed_data,
                'features': features,
                'quality_metrics': quality_metrics,
                'time_frequency': tf_data,
                'phase_data': phase_data,
                'preprocess_params': preprocess_params
            }

            print(f"结果已保存到: {output_dir}")
            return results

        except Exception as e:
            print(f"处理过程中出现错误: {str(e)}")
            raise

    def _visualize_results(self, data, tf_data, quality_metrics, save_dir):
        """
        Description: 生成可视化结果
        -------------------------------
        Parameters:
        data: 处理后的EEG数据
        tf_data: 时频分析结果
        quality_metrics: 质量指标
        save_dir: 保存目录
        """
        # 选择第一个数据段进行可视化
        if len(data.shape) == 3:
            segment_data = data[0]  # 使用第一个数据段
        else:
            segment_data = data

        # 计算相位连接性
        phase_data = self.analyzer.phase_analysis(segment_data)

        # 绘制相位连接性图
        self.visualizer.plot_phase_connectivity(
            plv_matrix=phase_data['plv_matrix'],
            save_dir=save_dir,
            title='通道间相位连接性'
        )

        # 绘制综合视图
        self.visualizer.plot_comprehensive_view(
            segment_data,
            tf_data,
            quality_metrics,
            save_dir
        )

        # 绘制时频图
        self.visualizer.plot_time_frequency(tf_data, save_dir)


def main():
    """主函数"""
    # 设置参数
    SAMPLE_RATE = 256  # 采样率
    WINDOW_SIZE = 2.0  # 窗口大小(秒)
    OVERLAP = 0.5  # 重叠比例

    # 创建EEG处理器实例
    processor = EEGProcessor(sample_rate=SAMPLE_RATE)

    # 设置数据文件路径
    data_dir = "data"  # 数据目录
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 处理目录中的所有EEG文件
    for file_name in os.listdir(data_dir):
        if file_name.endswith(('.csv', '.npy', '.edf')):
            file_path = os.path.join(data_dir, file_name)
            print(f"\n开始处理文件: {file_name}")

            try:
                # 处理文件
                results = processor.process_file(
                    file_path,
                    window_size=WINDOW_SIZE,
                    overlap=OVERLAP,
                    preprocess_methods=['filter', 'normalize']
                )

                # 保存结果
                output_dir = os.path.join("results", os.path.splitext(file_name)[0])
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # 保存处理后的数据
                np.save(os.path.join(output_dir, "processed_data.npy"),
                        results['data'])

                # 保存特征数据
                np.save(os.path.join(output_dir, "features.npy"),
                        results['features'])

                print(f"结果已保存到: {output_dir}")

            except Exception as e:
                print(f"处理文件 {file_name} 时出错: {str(e)}")
                continue


if __name__ == "__main__":
    main()