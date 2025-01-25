"""
EEG可视化模块
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import platform
import matplotlib as mpl
import os

from feature_extractor import spectral_analysis


def setup_matplotlib_fonts():
    """
    Description: 设置matplotlib字体，支持中文显示
    """
    system = platform.system().lower()
    if system == 'windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']  # 优先使用微软雅黑
    elif system == 'darwin':  # macOS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC']
    elif system == 'linux':
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'WenQuanYi Micro Hei']

    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    
    # 设置全局字体大小
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.titlesize'] = 12


class EEGVisualizer:
    def __init__(self, sample_rate: int):
        """
        Description: EEG可视化类
        -------------------------------
        Parameters:
        sample_rate: 采样率
        """
        self.sample_rate = sample_rate
        setup_matplotlib_fonts()
        
    def save_plot(self, save_dir: str, filename: str):
        """保存当前图形到文件"""
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        plt.savefig(os.path.join(save_dir, filename))
        plt.close()

    def plot_time_domain(self, data: np.ndarray, save_dir: str, title: str = "EEG时域波形",
                         channel_names: list = None):
        """
        Description: 绘制时域波形图
        -------------------------------
        Parameters:
        data: 输入数据，形状为(samples, channels)
        save_dir: 保存目录
        title: 图标题
        channel_names: 通道名称列表
        """
        plt.figure(figsize=(15, 10))
        time = np.arange(data.shape[0]) / self.sample_rate

        for ch in range(data.shape[1]):
            plt.subplot(data.shape[1], 1, ch + 1)
            plt.plot(time, data[:, ch], 'b-', linewidth=0.5)

            if channel_names:
                plt.ylabel(channel_names[ch])
            else:
                plt.ylabel(f'Channel {ch + 1}')

            if ch == data.shape[1] - 1:
                plt.xlabel('时间 (秒)')

        plt.suptitle(title)
        plt.tight_layout()
        self.save_plot(save_dir, 'time_domain.png')

    def plot_psd(self, freqs: np.ndarray, psd: np.ndarray, save_dir: str,
                 channel_names: list = None, title: str = "功率谱密度"):
        """
        Description: 绘制功率谱密度图
        -------------------------------
        Parameters:
        freqs: 频率数组
        psd: 功率谱密度数组，形状为(channels, frequencies)
        save_dir: 保存目录
        channel_names: 通道名称列表
        title: 图标题
        """
        plt.figure(figsize=(12, 8))

        for ch in range(psd.shape[0]):
            plt.semilogy(freqs, psd[ch], label=channel_names[ch] if channel_names else f'Channel {ch + 1}')

        plt.grid(True)
        plt.xlabel('频率 (Hz)')
        plt.ylabel('功率谱密度 (uV^2/Hz)')
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        self.save_plot(save_dir, 'psd.png')

    def plot_time_frequency(self, tf_data: dict, save_dir: str, channel_idx: int = 0,
                            title: str = "时频分析"):
        """
        Description: 绘制时频图
        -------------------------------
        Parameters:
        tf_data: 时频数据字典
        save_dir: 保存目录
        channel_idx: 要绘制的通道索引
        title: 图标题
        """
        channel_data = tf_data[f'channel_{channel_idx}']

        plt.figure(figsize=(12, 8))
        plt.pcolormesh(channel_data['times'], channel_data['frequencies'],
                       channel_data['power'], shading='gouraud')
        plt.colorbar(label='幅度')
        plt.ylabel('频率 (Hz)')
        plt.xlabel('时间 (秒)')
        plt.title(f'{title} - Channel {channel_idx + 1}')
        plt.tight_layout()
        self.save_plot(save_dir, f'time_frequency_ch{channel_idx+1}.png')

    def plot_phase_connectivity(self, plv_matrix: np.ndarray, save_dir: str,
                                channel_names: list = None,
                                title: str = "通道间相位连接性"):
        """
        Description: 绘制相位连接性热力图
        -------------------------------
        Parameters:
        plv_matrix: 相位锁定值矩阵
        save_dir: 保存目录
        channel_names: 通道名称列表
        title: 图标题
        """
        plt.figure(figsize=(10, 8))
        im = plt.imshow(plv_matrix, cmap='hot', aspect='equal')
        plt.colorbar(im, label='PLV')

        if channel_names:
            plt.xticks(range(len(channel_names)), channel_names, rotation=45)
            plt.yticks(range(len(channel_names)), channel_names)

        plt.title(title)
        plt.tight_layout()
        self.save_plot(save_dir, 'phase_connectivity.png')

    def plot_brain_map(self, data: np.ndarray, save_dir: str,
                       channel_positions: dict = None,
                       title: str = "脑地形图"):
        """
        Description: 绘制脑地形图
        -------------------------------
        Parameters:
        data: 输入数据，形状为(channels,)
        save_dir: 保存目录
        channel_positions: 通道位置字典，格式为 {'channel_name': (x, y)}
        title: 图标题
        """
        if channel_positions is None:
            # 默认4通道位置
            channel_positions = {
                'Channel_1': (-0.5, 0.5),
                'Channel_2': (0.5, 0.5),
                'Channel_3': (-0.5, -0.5),
                'Channel_4': (0.5, -0.5)
            }

        plt.figure(figsize=(10, 10))
        
        # 绘制头部轮廓
        circle = plt.Circle((0, 0), 1, fill=False, color='black')
        plt.gca().add_patch(circle)
        
        # 绘制鼻子位置标记
        plt.plot([0, 0], [0.9, 1.1], 'k-', linewidth=2)
        
        # 绘制通道位置和值
        for i, (ch, pos) in enumerate(channel_positions.items()):
            plt.scatter(pos[0], pos[1], c=[data[i]], cmap='RdBu_r',
                       s=300, vmin=data.min(), vmax=data.max())
            plt.text(pos[0], pos[1], f'{data[i]:.2f}',
                     ha='center', va='bottom')

        plt.colorbar(label='幅值')
        plt.axis('equal')
        plt.title(title)
        self.save_plot(save_dir, 'brain_map.png')

    def plot_comprehensive_view(self, data: np.ndarray, tf_data: dict,
                                quality_metrics: dict, save_dir: str,
                                channel_names: list = None):
        """
        Description: 绘制综合视图
        -------------------------------
        Parameters:
        data: 输入数据，形状为(samples, channels)
        tf_data: 时频数据字典
        quality_metrics: 质量指标字典
        save_dir: 保存目录
        channel_names: 通道名称列表
        """
        plt.figure(figsize=(20, 15))
        gs = GridSpec(4, 4)

        # 1. 时域波形 (占据上半部分)
        ax1 = plt.subplot(gs[0:2, :])
        time = np.arange(data.shape[0]) / self.sample_rate
        
        # 为每个通道设置不同的颜色
        colors = ['b', 'r', 'g', 'c']
        for ch in range(data.shape[1]):
            # 对数据进行归一化，使不同通道的波形分开显示
            normalized_data = data[:, ch] + ch * 3 * np.std(data[:, ch])
            ax1.plot(time, normalized_data, color=colors[ch % len(colors)], linewidth=0.8,
                     label=channel_names[ch] if channel_names else f'Channel {ch + 1}')
        
        ax1.set_xlabel('时间 (秒)')
        ax1.set_ylabel('幅度 (相对值)')
        ax1.set_title('时域波形')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)

        # 2. 时频图 (左下)
        ax2 = plt.subplot(gs[2, 0:2])
        channel_data = tf_data['channel_0']  # 显示第一个通道的时频图
        im = ax2.pcolormesh(channel_data['times'], channel_data['frequencies'],
                           channel_data['power'], shading='gouraud', cmap='jet')
        plt.colorbar(im, ax=ax2, label='功率')
        ax2.set_ylabel('频率 (Hz)')
        ax2.set_xlabel('时间 (秒)')
        ax2.set_title('时频分析 (Channel 1)')

        # 3. 频段能量分布 (右下)
        ax3 = plt.subplot(gs[2, 2:])
        
        # 计算频谱
        freqs, psd = spectral_analysis(data, self.sample_rate)
        
        # 定义频段
        delta_mask = (freqs >= 0.5) & (freqs <= 4)
        theta_mask = (freqs >= 4) & (freqs <= 8)
        alpha_mask = (freqs >= 8) & (freqs <= 13)
        beta_mask = (freqs >= 13) & (freqs <= 30)
        gamma_mask = (freqs >= 30) & (freqs <= 100)
        
        band_names = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        x = np.arange(len(band_names))
        width = 0.8 / data.shape[1]
        
        for ch in range(data.shape[1]):
            band_powers = [
                np.sum(psd[ch, delta_mask]),
                np.sum(psd[ch, theta_mask]),
                np.sum(psd[ch, alpha_mask]),
                np.sum(psd[ch, beta_mask]),
                np.sum(psd[ch, gamma_mask])
            ]
            band_powers = np.array(band_powers) / np.sum(band_powers)  # 归一化
            ax3.bar(x + ch * width, band_powers, width,
                    label=channel_names[ch] if channel_names else f'Channel {ch + 1}',
                    color=colors[ch % len(colors)])
        
        ax3.set_ylabel('相对功率')
        ax3.set_title('频段能量分布')
        ax3.set_xticks(x + width * (data.shape[1] - 1) / 2)
        ax3.set_xticklabels(band_names)
        ax3.legend()

        # 4. 质量指标和统计信息 (最下面一行)
        ax4 = plt.subplot(gs[3, :])
        ax4.axis('off')
        
        # 计算一些统计指标
        mean_power = np.mean(psd, axis=1)
        peak_freq = freqs[np.argmax(psd, axis=1)]
        
        info_text = (
            f"数据质量指标:\n"
            f"缺失值比例: {quality_metrics['missing_ratio']:.2%}\n"
            f"平均信噪比: {np.mean(quality_metrics['snr']):.2f} dB\n"
            f"基线漂移: {quality_metrics['baseline_drift']:.2f}\n\n"
            f"统计信息:\n"
            f"平均功率: {mean_power.mean():.2f} uV^2\n"
            f"主频率: {peak_freq.mean():.1f} Hz\n"
            f"Alpha/Beta比值: {np.sum(psd[:, alpha_mask].mean()) / np.sum(psd[:, beta_mask].mean()):.2f}"
        )
        ax4.text(0.1, 0.1, info_text, fontsize=12, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.2))

        plt.suptitle('EEG信号综合分析', fontsize=16, y=0.95)
        plt.tight_layout()
        self.save_plot(save_dir, 'comprehensive_view.png') 