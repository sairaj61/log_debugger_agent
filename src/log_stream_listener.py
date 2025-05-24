import os
import time
import threading


class LogStreamListener:
    def __init__(self, filepath, callback):
        self.filepath = filepath
        self.callback = callback
        self._stop_event = threading.Event()

    def read_old_logs(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.callback(line.strip())

    def _follow(self):
        with open(self.filepath, 'r') as f:
            f.seek(0, os.SEEK_END)
            while not self._stop_event.is_set():
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self.callback(line.strip())

    def start_streaming(self):
        threading.Thread(target=self._follow, daemon=True).start()

    def stop(self):
        self._stop_event.set()
