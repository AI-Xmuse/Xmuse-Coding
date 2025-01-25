"""
主程序入口模块
"""

import argparse
import logging
import threading
from typing import List

from .core.receiver import OSCDataReceiver
from .ui.signal_selector import select_signals


def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='多端口OSC数据接收器')
    parser.add_argument('--ports', type=int, nargs='+', default=[8001, 8002],
                        help='OSC服务器端口列表 (默认: 8001 8002)')
    parser.add_argument('--save-dir', type=str, default='data',
                        help='数据保存目录 (默认: data)')
    parser.add_argument('--all-signals', action='store_true',
                        help='接收所有信号 (默认: False)')
    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')

    args = parser.parse_args()

    # 如果启用调试模式，设置日志级别为DEBUG
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # 选择信号类型
        selected_signals = None if args.all_signals else select_signals()
        if selected_signals:
            logging.info(f"已启动信号监听，共 {len(selected_signals)} 个信号")
        else:
            logging.info("监听所有信号类型")

        # 创建接收器实例
        receiver = OSCDataReceiver(args.ports, selected_signals, args.save_dir)
        receiver.start()

        logging.info("程序已启动，按 Ctrl+C 停止...")

        # 添加定期状态检查
        def check_status():
            last_check = {port: False for port in args.ports}
            while True:
                for port in args.ports:
                    current_status = True
                    if current_status != last_check[port]:
                        if current_status:
                            logging.info(f"端口 {port} - 连接正常")
                        else:
                            logging.warning(f"端口 {port} - 连接异常")
                        last_check[port] = current_status

        status_thread = threading.Thread(target=check_status, daemon=True)
        status_thread.start()

        # 保持程序运行
        try:
            status_thread.join()
        except KeyboardInterrupt:
            logging.info("正在停止程序...")
            receiver.stop()
            logging.info("程序已退出")

    except KeyboardInterrupt:
        logging.info("正在停止程序...")
        if 'receiver' in locals():
            receiver.stop()
        logging.info("程序已退出")
    except Exception as e:
        logging.error(f"程序错误: {e}", exc_info=True)
        if 'receiver' in locals():
            receiver.stop()


if __name__ == "__main__":
    main() 