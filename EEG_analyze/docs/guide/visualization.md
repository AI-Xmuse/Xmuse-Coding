# 可视化指南

## 可视化功能

EEG-Analyze 提供了丰富的可视化功能：

1. 时域波形图
2. 功率谱密度图
3. 时频分析图
4. 相位连接性图
5. 脑地形图
6. 综合分析视图

## 基本使用

```python
from eeg_analyze.visualizer import EEGVisualizer

# 创建可视化器
visualizer = EEGVisualizer(sample_rate=250)

# 绘制时域波形
visualizer.plot_time_domain(
    data=eeg_data,
    save_dir='results',
    title='EEG时域波形',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)
```

## 时频分析可视化

```python
# 绘制时频图
visualizer.plot_time_frequency(
    tf_data=tf_data,
    save_dir='results',
    channel_idx=0,  # 选择要显示的通道
    title='时频分析结果'
)
```

## 相位连接性可视化

```python
# 绘制相位连接性热力图
visualizer.plot_phase_connectivity(
    plv_matrix=phase_data['plv_matrix'],
    save_dir='results',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4'],
    title='通道间相位连接性'
)
```

## 脑地形图

```python
# 定义通道位置
channel_positions = {
    'Fp1': (-0.5, 0.5),
    'Fp2': (0.5, 0.5),
    'F3': (-0.5, -0.5),
    'F4': (0.5, -0.5)
}

# 绘制脑地形图
visualizer.plot_brain_map(
    data=feature_values,
    save_dir='results',
    channel_positions=channel_positions,
    title='特征分布图'
)
```

## 综合视图

```python
# 绘制综合分析视图
visualizer.plot_comprehensive_view(
    data=eeg_data,
    tf_data=tf_data,
    quality_metrics=quality_metrics,
    save_dir='results',
    channel_names=['Fp1', 'Fp2', 'F3', 'F4']
)
```

## 自定义选项

1. 图形大小
   - 可通过参数调整图形尺寸
   - 默认尺寸适合大多数显示设备

2. 配色方案
   - 支持多种颜色映射
   - 可根据需要自定义颜色

3. 字体设置
   - 自动适配中文显示
   - 可调整字体大小和样式

4. 保存格式
   - 支持PNG、JPG、PDF等格式
   - 可调整输出分辨率

## 最佳实践

1. 数据展示
   - 选择合适的时间窗口
   - 适当的数据缩放
   - 清晰的标签和图例

2. 布局优化
   - 合理安排子图位置
   - 避免信息过度拥挤
   - 保持视觉层次感

3. 可读性
   - 使用恰当的字体大小
   - 添加清晰的标题和说明
   - 保持配色的一致性 