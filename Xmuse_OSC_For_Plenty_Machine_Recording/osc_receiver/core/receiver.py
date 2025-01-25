"""
OSC接收器核心模块
"""

import os
import time
import csv
import logging
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import pandas as pd

from .data_types import DataBuffer, OSCMessage
from .signal_manager import SignalManager


class OSCDataReceiver:
    def __init__(self, ports: List[int], signal_types: Optional[List[str]] = None,
                 save_dir: str = "data", buffer_size: int = 1000):
        """
        初始化OSC数据接收器

        Args:
            ports: OSC服务器端口列表
            signal_types: 需要接收的信号类型列表
            save_dir: 数据保存目录
            buffer_size: 数据缓冲区大小
        """
        self.ports = ports
        self.save_dir = save_dir
        self.servers = []
        self.running = True
        self.data_buffer = DataBuffer(buffer_size)
        self.signal_manager = SignalManager()
        self.executor = ThreadPoolExecutor(max_workers=min(len(ports) + 2, 32))
        self.write_buffer = {port: [] for port in ports}
        self.write_buffer_size = 100
        self.last_debug_time = time.time()
        self.debug_interval = 5

        # 初始化配置
        self._init_config(signal_types)
        self._init_data_files()
        self._start_data_processor()
        self._start_stats_monitor()

    def _init_config(self, signal_types: Optional[List[str]]) -> None:
        """初始化配置"""
        self.port_signals = {port: [] for port in self.ports}
        if signal_types:
            for port in self.ports:
                port_signals = []
                for signal in signal_types:
                    clean_signal = signal.split('/')[-1] if signal.startswith('/') else signal
                    port_signal = f"/{port}/{clean_signal}"
                    port_signals.append(port_signal)
                    self.signal_manager.add_signal(port_signal)
                self.port_signals[port] = port_signals
                logging.debug(f"端口 {port} 配置的信号: {port_signals}")
        else:
            default_signals = SignalManager.get_available_signals()
            for port in self.ports:
                for category in default_signals.values():
                    for signal in category:
                        clean_signal = signal.split('/')[-1] if signal.startswith('/') else signal
                        port_signal = f"/{port}/{clean_signal}"
                        self.port_signals[port].append(port_signal)
                        self.signal_manager.add_signal(port_signal)

    def _init_data_files(self) -> None:
        """初始化数据文件"""
        os.makedirs(self.save_dir, exist_ok=True)
        self.csv_files = {}
        self.csv_writers = {}

        for port in self.ports:
            filename = f"osc_data_port_{port}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(self.save_dir, filename)
            self.csv_files[port] = open(filepath, 'w', newline='', buffering=8192)
            self.csv_writers[port] = csv.writer(self.csv_files[port])
            self.csv_writers[port].writerow(['Timestamp', 'Address', 'Data'])

    def _start_stats_monitor(self) -> None:
        """启动性能监控"""
        def monitor():
            while self.running:
                stats = self.data_buffer.get_stats()
                if stats and (stats['received_rate'] > 0 or stats['dropped_rate'] > 0):
                    logging.info(f"性能统计: {stats}")
                time.sleep(1)

        self.executor.submit(monitor)

    def handle_message(self, port: int, address: str, *args) -> None:
        """处理OSC消息"""
        if not self.signal_manager.is_active(address):
            return

        current_time = time.time()
        if current_time - self.last_debug_time >= self.debug_interval:
            logging.debug(f"信号匹配 - 端口: {port}, 地址: {address}")
            self.last_debug_time = current_time

        message = OSCMessage(
            port=port,
            address=address,
            args=args,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        )

        if not self.data_buffer.put(message):
            logging.warning("缓冲区已满，数据丢弃")

    def _write_data(self, message: OSCMessage) -> None:
        """写入数据（批量）"""
        try:
            port = message.port
            self.write_buffer[port].append([message.timestamp, message.address, message.args])

            if len(self.write_buffer[port]) >= self.write_buffer_size:
                with self.data_buffer.lock:
                    self.csv_writers[port].writerows(self.write_buffer[port])
                self.write_buffer[port] = []

        except Exception as e:
            logging.error(f"写入数据错误: {e}")

    def start_server(self, port: int) -> Optional[BlockingOSCUDPServer]:
        """启动单个OSC服务器"""
        try:
            dispatcher = Dispatcher()
            dispatcher.map("/*", lambda address, *args: self.handle_message(port, address, *args))

            server = BlockingOSCUDPServer(("0.0.0.0", port), dispatcher)
            logging.info(f"OSC服务器启动在端口 {port}")

            self._test_server_connection(port)

            return server
        except Exception as e:
            logging.error(f"启动服务器失败 (端口 {port}): {e}", exc_info=True)
            return None

    def _test_server_connection(self, port: int) -> None:
        """测试服务器连接"""
        def test():
            try:
                import socket
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.bind(('0.0.0.0', 0))
                    sock.sendto(b'test', ('127.0.0.1', port))
                logging.info(f"端口 {port} 测试成功")
            except Exception as e:
                logging.error(f"端口 {port} 测试失败: {e}")

        Thread(target=test, daemon=True).start()

    def start(self) -> None:
        """启动所有服务器"""
        for port in self.ports:
            server = self.start_server(port)
            if server:
                thread = Thread(target=server.serve_forever, daemon=True)
                thread.start()
                self.servers.append((server, thread))
                logging.info(f"服务器线程启动: 端口 {port}")

    def stop(self) -> None:
        """停止服务"""
        self.running = False
        time.sleep(0.2)

        while True:
            message = self.data_buffer.get()
            if not message:
                break
            self._write_data(message)

        for port in self.ports:
            if self.write_buffer[port]:
                try:
                    self.csv_writers[port].writerows(self.write_buffer[port])
                    self.csv_files[port].flush()
                except Exception as e:
                    logging.error(f"最终数据写入错误: {e}")

        self.executor.shutdown(wait=True)
        for server, _ in self.servers:
            try:
                server.shutdown()
            except:
                pass

        for file in self.csv_files.values():
            try:
                file.close()
            except:
                pass

        logging.info("所有资源已清理完毕")

    def _start_data_processor(self) -> None:
        """启动数据处理器"""
        def process_data():
            idle_count = 0
            while self.running:
                try:
                    message = self.data_buffer.get()
                    if message:
                        self._write_data(message)
                        idle_count = 0
                    else:
                        idle_count += 1
                        sleep_time = min(0.1, idle_count * 0.001)
                        time.sleep(sleep_time)
                except Exception as e:
                    logging.error(f"处理数据错误: {e}")
                    time.sleep(0.1)

        self.executor.submit(process_data) 