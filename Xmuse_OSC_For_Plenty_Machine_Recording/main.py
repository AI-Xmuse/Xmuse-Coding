import argparse
import logging
import os
import sys
from typing import List, Optional

from .osc_receiver.core.receiver import OSCDataReceiver
from .osc_receiver.ui.signal_selector import select_signals


def setup_logging(debug: bool = False) -> None:
    """配置日志系统"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('osc_receiver.log', encoding='utf-8')
        ]
    )


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='多端口 OSC 数据接收器')
    parser.add_argument('--ports', nargs='+', type=int, default=[8001, 8002],
                      help='OSC 服务器端口列表')
    parser.add_argument('--save-dir', type=str, default='data',
                      help='数据保存目录')
    parser.add_argument('--debug', action='store_true',
                      help='启用调试模式')
    parser.add_argument('--all-signals', action='store_true',
                      help='接收所有信号')
    
    return parser.parse_args()


def main() -> None:
    """主函数"""
    args = parse_arguments()
    setup_logging(args.debug)
    
    try:
        # 创建保存目录
        os.makedirs(args.save_dir, exist_ok=True)
        
        # 选择信号
        if not args.all_signals:
            selected_signals = select_signals()
        else:
            selected_signals = None
        
        # 创建接收器
        receiver = OSCDataReceiver(
            ports=args.ports,
            signal_types=selected_signals,
            save_dir=args.save_dir
        )
        
        # 启动接收
        receiver.start()
        
        # 保持运行
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logging.info("接收到退出信号")
        finally:
            receiver.stop()
            
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()