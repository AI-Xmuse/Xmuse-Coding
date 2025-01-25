from pythonosc import dispatcher, osc_server
import logging
import threading
import time


class OSCServer:
    def __init__(self, data_buffer, exit_event):
        self.data_buffer = data_buffer
        self.exit_event = exit_event

    def handler_factory(self, signal_type):
        def handler(unused_addr, *args):
            self.data_buffer.put((signal_type, args))

        return handler

    def start(self):
        dispatcher1 = dispatcher.Dispatcher()
        prefix = "/8000"
        eeg_signal = "/eeg"
        full_signal = prefix + eeg_signal
        dispatcher1.map(full_signal, self.handler_factory(full_signal))

        server = osc_server.ThreadingOSCUDPServer(('0.0.0.0', 8000), dispatcher1)
        logging.info(f"Listening on port 8000 for EEG data")
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        while not self.exit_event.is_set():
            time.sleep(0.1)

        server.shutdown()
        server_thread.join()
        logging.info("OSC server has been stopped.")