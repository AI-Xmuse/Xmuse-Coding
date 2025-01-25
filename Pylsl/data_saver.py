import os
import csv
import json
import h5py
import numpy as np
from datetime import datetime
from typing import List

class DataSaver:
    """数据保存器类"""
    def __init__(self, base_path: str = "data"):
        """
        初始化数据保存器

        Args:
            base_path: 数据保存的基础路径
        """
        self.base_path = base_path
        self.current_segment = 0
        self.segment_data = []
        self.segment_timestamps = []
        self.max_segment_size = 1000  # 每个分段的最大样本数

        # 存储所有数据的列表
        self.all_data = []
        self.all_timestamps = []

        # 创建保存目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_path = os.path.join(base_path, f"session_{timestamp}")
        os.makedirs(self.session_path, exist_ok=True)

    def add_data(self, data: List[float], timestamp: float):
        """
        添加数据到当前分段和总数据列表

        Args:
            data: 数据样本
            timestamp: 时间戳
        """
        # 添加到分段数据
        self.segment_data.append(data)
        self.segment_timestamps.append(timestamp)

        # 添加到总数据列表
        self.all_data.append(data)
        self.all_timestamps.append(timestamp)

        # 检查是否需要保存当前分段
        if len(self.segment_data) >= self.max_segment_size:
            self.save_current_segment()

    def save_all_data(self):
        """保存所有数据到单个文件"""
        if not self.all_data:
            return

        # 保存为单个CSV文件
        self._save_all_csv()
        # 保存为单个JSON文件
        self._save_all_json()
        # 保存为单个HDF5文件
        self._save_all_hdf5()

    def _save_all_csv(self):
        """保存所有数据为单个CSV文件"""
        filepath = os.path.join(self.session_path, "all_data.csv")
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            # 写入头部
            writer.writerow(['Timestamp'] + [f'Channel_{i}' for i in range(len(self.all_data[0]))])
            # 写入所有数据
            for data, ts in zip(self.all_data, self.all_timestamps):
                writer.writerow([ts] + data)

    def _save_all_json(self):
        """保存所有数据为单个JSON文件"""
        filepath = os.path.join(self.session_path, "all_data.json")
        data_dict = {
            'timestamps': self.all_timestamps,
            'data': self.all_data,
            'channels': [f'Channel_{i}' for i in range(len(self.all_data[0]))],
            'total_samples': len(self.all_data),
            'start_time': self.all_timestamps[0] if self.all_timestamps else None,
            'end_time': self.all_timestamps[-1] if self.all_timestamps else None
        }
        with open(filepath, 'w') as f:
            json.dump(data_dict, f, indent=2)

    def _save_all_hdf5(self):
        """保存所有数据为单个HDF5文件"""
        filepath = os.path.join(self.session_path, "all_data.h5")
        with h5py.File(filepath, 'w') as f:
            # 创建数据集
            f.create_dataset('timestamps', data=np.array(self.all_timestamps))
            f.create_dataset('data', data=np.array(self.all_data))
            # 添加元数据
            f.attrs['channels'] = [f'Channel_{i}'.encode() for i in range(len(self.all_data[0]))]
            f.attrs['total_samples'] = len(self.all_data)
            f.attrs['start_time'] = self.all_timestamps[0] if self.all_timestamps else 0
            f.attrs['end_time'] = self.all_timestamps[-1] if self.all_timestamps else 0

    def save_current_segment(self):
        """保存当前数据分段"""
        if not self.segment_data:
            return

        segment_name = f"segment_{self.current_segment:04d}"

        try:
            # 保存为CSV文件
            filepath = os.path.join(self.session_path, f"{segment_name}.csv")
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                # 写入头部
                writer.writerow(['Timestamp'] + [f'Channel_{i}' for i in range(len(self.segment_data[0]))])
                # 写入数据
                for data, ts in zip(self.segment_data, self.segment_timestamps):
                    writer.writerow([ts] + data)

            print(f"已保存分段数据到: {filepath}")

            # 清空当前分段数据
            self.segment_data = []
            self.segment_timestamps = []
            self.current_segment += 1

        except Exception as e:
            print(f"保存分段数据时出错: {e}")

    def close(self):
        """关闭数据保存器，保存所有数据"""
        try:
            # 保存所有数据到单个文件
            self.save_all_data()
            print(f"已保存所有数据到: {self.session_path}")
        except Exception as e:
            print(f"保存所有数据时出错: {e}") 