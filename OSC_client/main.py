import threading
import logging
import time

import keyboard
import queue
import sys
import os
from Server import OSCServer
from data_handler import DataHandler
from config import OUTPUT_DIR, setup_default_device


def listen_for_exit(exit_event):
    while True:
        if keyboard.is_pressed('q'):
            logging.info("Exit key pressed. Stopping all tasks and exiting the script.")
            exit_event.set()
            break
        time.sleep(0.1)


def main():
    # 初始化日志
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # 初始化变量
    data_buffer = queue.Queue()
    exit_event = threading.Event()

    # 创建输出目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        # 设置设备
        clients = setup_default_device()

        # 初始化服务器和数据处理器
        server = OSCServer(data_buffer, exit_event)
        data_handler = DataHandler(data_buffer, clients, OUTPUT_DIR, exit_event)

        # 启动线程
        exit_thread = threading.Thread(target=listen_for_exit, args=(exit_event,))
        server_thread = threading.Thread(target=server.start)
        send_thread = threading.Thread(target=data_handler.send_buffered_data)

        for thread in [exit_thread, server_thread, send_thread]:
            thread.daemon = True
            thread.start()

        server_thread.join()
        send_thread.join()

    except Exception as e:
        logging.error(f"An error occurred during program operation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()