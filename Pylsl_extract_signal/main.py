import pylsl
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from collections import deque
import os
import numpy as np
from datetime import datetime
matplotlib.use('TkAgg')
print('finished importing packages')
# 定义所有需要采集的数据类型
STREAM_TYPES = ['ThetaRel', 'DeltaScore', 'IsGood', 'EEG', 'DeltaAbs', 'HsiPrec',
                'JawClench', 'GammaRel', 'PPG', 'BetaScore', 'DeltaRel', 'HeadOn',
                'ThetaAbs', 'ThetaScore', 'BetaRel', 'AlphaRel', 'GammaAbs',
                'GammaScore', 'Blink', 'BetaAbs', 'Gyro', 'Therm', 'AlphaAbs',
                'Accel', 'AlphaScore', 'Batt']

# 创建数据保存目录
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_dir = os.path.join("signal_data", timestamp)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 创建字典来存储所有数据流的inlet和信息
inlets = {}
stream_details = {}

# 查找并创建所有类型的数据流inlet
for stream_type in STREAM_TYPES:
    streams = pylsl.resolve_byprop("type", stream_type, timeout=2.0)
    if streams:
        print(f"找到 {stream_type} 数据流")
        stream_info = streams[0]
        inlet = pylsl.StreamInlet(stream_info)
        inlets[stream_type] = inlet
        
        # 获取采样率
        nominal_srate = stream_info.nominal_srate()
        if nominal_srate <= 0:  # 如果采样率未指定，设置默认值
            nominal_srate = 1.0
            
        stream_details[stream_type] = {
            'channel_count': stream_info.channel_count(),
            'nominal_srate': nominal_srate,
            'channel_format': stream_info.channel_format()
        }
        
        # 创建信号流的CSV文件并写入头部
        if stream_type == 'EEG':
            annot_path = os.path.join(save_dir, f"EEG_Annot_signal.csv")
            channel_columns = [f'channel_{i+1}' for i in range(stream_info.channel_count())]
            df = pd.DataFrame(columns=['timestamp','Annot'] + channel_columns )
            df.to_csv(annot_path, index=False)

        else:
            csv_path = os.path.join(save_dir, f"{stream_type}_signal.csv")
            channel_columns = [f'channel_{i+1}' for i in range(stream_info.channel_count())]
            df = pd.DataFrame(columns=['timestamp'] + channel_columns)
            df.to_csv(csv_path, index=False)


        
        print(f"{stream_type} 数据流信息：通道数={stream_info.channel_count()}, 采样率={nominal_srate}")

if not inlets:
    print("未找到任何数据流。请确保设备已连接并处于运行状态。")
    exit()

# 如果有EEG数据流，设置实时可视化
if 'EEG' in inlets:
    window_size = 100
    eeg_data_windows = [deque(maxlen=window_size) for _ in range(4)]
    plt.ion()
    fig, ax = plt.subplots(4, 1, figsize=(10, 8))
    lines = [ax[i].plot([], [], label=f'Channel {i+1}')[0] for i in range(4)]

    for i in range(4):
        ax[i].set_xlim(0, window_size)
        ax[i].set_ylim(-500, 500)
        ax[i].set_ylabel('EEG Value')
        ax[i].legend(loc='upper right')
        ax[i].set_title(f'Real-time EEG Data (Channel {i+1})')
    plt.xlabel('Samples')

def update_visualization(eeg_data):
    if 'EEG' not in inlets:
        return

    for i in range(4):
        eeg_data_windows[i].append(eeg_data[i])
        lines[i].set_ydata(list(eeg_data_windows[i]))
        lines[i].set_xdata(range(len(eeg_data_windows[i])))
        min_y = min(eeg_data_windows[i])
        max_y = max(eeg_data_windows[i])
        ax[i].set_ylim(min_y - 100, max_y + 100)

    fig.canvas.draw()
    fig.canvas.flush_events()

def save_stream_data(stream_type, samples, timestamps):
    """直接保存数据流数据到CSV文件"""
    if not samples:
        return
        
    try:
        # 准备数据
        new_data = [
            {
                'timestamp': ts,
                **{f'channel_{j+1}': value for j, value in enumerate(data)}
            }
            for data, ts in zip(samples, timestamps)
        ]
        
        # 将数据添加到DataFrame并保存
        df = pd.DataFrame(new_data)
        csv_path = os.path.join(save_dir, f"{stream_type}_signal.csv")
        df.to_csv(csv_path, mode='a', header=False, index=False)
            
    except Exception as e:
        print(f"保存 {stream_type} 数据时出错: {str(e)}")

import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import threading
from queue import Queue

# 共享标注队列（线程安全）
annotation_queue = Queue()

def setup_gui():
    root = tk.Tk()
    root.title("EEG Annotation")

    # 增加标注类型预设按钮
    ttk.Label(root, text="Quick annot:").pack()
    preset_frame = ttk.Frame(root)
    preset_frame.pack()
    
    presets = ["Blink", "Move", "Touch", "Frown","unknown"]
    for preset in presets:
        ttk.Button(preset_frame, text=preset, 
                 command=lambda p=preset: annotation_queue.put(p)).pack(side=tk.LEFT)

    # 自定义标注输入
    entry = ttk.Entry(root)
    entry.pack(pady=5)
    
    def submit_annotation():
        """提交标注（支持回车键）"""
        if text := entry.get().strip():
            annotation_queue.put(text)
            entry.delete(0, tk.END)
    
    ttk.Button(root, text="提交标注 (Enter)", command=submit_annotation).pack()
    root.bind('<Return>', lambda e: submit_annotation())
    
    root.mainloop()

# 启动GUI线程
threading.Thread(target=setup_gui, daemon=True).start()

def save_stream_EEG_data(stream_type, samples, timestamps):
    """修复后的数据保存函数"""
    if not samples:
        return

    try:
        # 获取当前所有未处理的标注
        annotations = []
        while not annotation_queue.empty():
            annotations.append(annotation_queue.get())
        


        annot_list = [''] * len(timestamps)
        annot_list[0] = annotations[-1] if annotations else ""

        # 保证列顺序一致性
        data_dict = {
            'timestamp': timestamps,
            'Annot': annot_list  # 只对一个chunk的第一个样本做标注。时间分辨率取决于chunk size
        }
        
        # 动态生成通道数据
        for j in range(len(samples[0])):
            data_dict[f'channel_{j+1}'] = [sample[j] for sample in samples]

        # 将数据添加到DataFrame并保存
        df = pd.DataFrame(data_dict)
        csv_path = os.path.join(save_dir, f"{stream_type}_Annot_signal.csv")        
        df.to_csv(csv_path, mode='a', header=False, index=False)
        
        # 调试输出
        if annot_list[0] != '':
            print(f"标注: '{annot_list[0]}'")
        
    except Exception as e:
        print(f"保存失败: {str(e)}")



try:
    print("开始记录数据...")
    print(f"数据将保存在: {save_dir}")
    print("按 Ctrl+C 停止记录")
    
    while True:
        # 从每个数据流读取数据
        for stream_type, inlet in inlets.items():
            try:
                # 根据采样率计算应该读取的样本数
                nominal_srate = stream_details[stream_type]['nominal_srate']
                chunk_size = max(1, int(nominal_srate * 0.1))  # 每0.1秒的数据量
                
                # 使用pull_chunk读取多个样本
                samples, timestamps = inlet.pull_chunk(
                    max_samples=chunk_size,
                    timeout=0.0
                )
                
                if samples:


                    # 如果是EEG数据，更新可视化（只显示最后一个样本）
                    if stream_type == 'EEG':
                        update_visualization(samples[-1])
                        #added
                        save_stream_EEG_data(stream_type, samples, timestamps)
                    else:
                        save_stream_data(stream_type, samples, timestamps)

                        
                    
                        
            except Exception as e:
                print(f"处理 {stream_type} 数据时出错: {str(e)}")
                continue

        time.sleep(0.001)  # 小的延迟以避免CPU过载

except KeyboardInterrupt:
    print("\n数据记录完成！")
    if 'EEG' in inlets:
        plt.close(fig)