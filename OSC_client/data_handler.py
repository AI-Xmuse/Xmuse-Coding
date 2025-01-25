import queue
import logging
import time
import os
import threading


class DataHandler:
    def __init__(self, data_buffer, clients, output_dir, exit_event):
        self.data_buffer = data_buffer
        self.clients = clients
        self.output_dir = output_dir
        self.exit_event = exit_event
        self.file_lock = threading.Lock()

    def save_to_txt(self, signal_type, data):
        filename = os.path.join(self.output_dir, f"{signal_type.replace('/', '_')[1:]}.txt")

        for _ in range(5):
            try:
                with self.file_lock:
                    with open(filename, 'a') as file:
                        timestamp = time.time()
                        file.write(f"Timestamp: {timestamp}, Data: {data}\n")
                break
            except PermissionError as e:
                logging.error(f"PermissionError: {e} - Retrying...")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Unexpected error while writing to {filename}: {e}")
                break

    def send_buffered_data(self):
        while not self.exit_event.is_set():
            try:
                signal_type, processed_data = self.data_buffer.get(timeout=0.0001)
                logging.info(f"Sending data to devices: {processed_data}")
                for device in self.clients.values():
                    device.send_message(f"respond/{signal_type}", processed_data)
                    logging.info(f"Data sent to device: {processed_data}")
                self.save_to_txt(signal_type, processed_data)
            except queue.Empty:
                logging.debug("Buffer is empty, waiting for new data...")