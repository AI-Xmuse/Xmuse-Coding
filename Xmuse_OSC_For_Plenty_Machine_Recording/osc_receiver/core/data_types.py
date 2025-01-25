"""
数据类型和缓冲区管理模块
"""

from dataclasses import dataclass
from queue import Queue
from threading import Lock
import time
import logging
from typing import Dict, Optional


@dataclass
class OSCMessage:
    """OSC消息数据类"""
    port: int
    address: str
    args: tuple
    timestamp: str


class DataBuffer:
    """数据缓冲区管理"""

    def __init__(self, max_size: int = 1000):
        self.buffer = Queue(maxsize=max_size)
        self.lock = Lock()
        self._stats = {
            'received': 0,
            'dropped': 0,
            'processed': 0,
            'last_time': time.time()
        }

    def put(self, data: OSCMessage) -> bool:
        try:
            self.buffer.put_nowait(data)
            with self.lock:
                self._stats['received'] += 1
            return True
        except:
            with self.lock:
                self._stats['dropped'] += 1
            return False

    def get(self) -> Optional[OSCMessage]:
        try:
            data = self.buffer.get_nowait()
            with self.lock:
                self._stats['processed'] += 1
            return data
        except:
            return None

    def get_stats(self) -> Optional[Dict]:
        """获取性能统计"""
        current_time = time.time()
        with self.lock:
            time_diff = current_time - self._stats['last_time']
            if time_diff >= 1.0:
                stats = {
                    'received_rate': self._stats['received'] / time_diff,
                    'dropped_rate': self._stats['dropped'] / time_diff,
                    'buffer_usage': self.buffer.qsize() / self.buffer._maxsize * 100
                }
                self._stats.update({'received': 0, 'dropped': 0, 'last_time': current_time})
                return stats
        return None 