from PyQt6.QtCore import QThread, pyqtSignal
import requests

class MjpegStreamReader(QThread):
    frame_received = pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.running = True

    def run(self):
        print("[MJPEG] Thread started, requesting stream:", self.url)
        try:
            stream = requests.get(self.url, stream=True)
            buffer = b""
            for chunk in stream.iter_content(1024):
                if not self.running:
                    break
                buffer += chunk
                start = buffer.find(b'\xff\xd8')
                end = buffer.find(b'\xff\xd9')
                if start != -1 and end != -1 and end > start:
                    jpg = buffer[start:end+2]
                    buffer = buffer[end+2:]
                    print(f"[MJPEG] Frame received: {len(jpg)} bytes")
                    self.frame_received.emit(jpg)
        except Exception as e:
            print("Stream error:", e)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

