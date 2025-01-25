"""
信号管理模块
"""

from typing import Dict, List, Optional, Callable


class SignalManager:
    """信号管理器"""

    def __init__(self):
        self.active_signals = set()
        self.signal_callbacks = {}

    def add_signal(self, signal: str, callback: Optional[Callable] = None):
        """添加信号"""
        self.active_signals.add(signal)
        if callback:
            self.signal_callbacks[signal] = callback

    def remove_signal(self, signal: str):
        """移除信号"""
        self.active_signals.discard(signal)
        self.signal_callbacks.pop(signal, None)

    def is_active(self, signal: str) -> bool:
        """检查信号是否激活"""
        return signal in self.active_signals

    @staticmethod
    def get_available_signals() -> Dict[str, List[str]]:
        """获取可用的信号类型"""
        return {
            "EEG": ["/eeg", "elements/is_good"],
            "生理信号": ["/ppg", "/batt", "/drlref"],
            "运动数据": ["/acc", "/gyro"]
        }

    @staticmethod
    def get_signal_description(signal: str) -> str:
        """获取信号描述"""
        descriptions = {
            "eeg": "脑电信号",
            "is_good": "信号质量指标",
            "ppg": "光电容积信号",
            "batt": "电池电量",
            "drlref": "参考电极信号",
            "acc": "加速度数据",
            "gyro": "陀螺仪数据"
        }

        for key, desc in descriptions.items():
            if key in signal:
                return desc
        return "" 