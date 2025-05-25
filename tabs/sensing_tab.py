from PySide6.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import QDateTime


class SensingTab(QWidget):
    def __init__(self, mqtt_handler):
        super().__init__()
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        self.send_to_ai_btn = QPushButton("GPT 분석 요청")
        self.send_to_ai_btn.setFixedHeight(40)

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)
        layout.addWidget(self.send_to_ai_btn)

        # MQTT 메시지 핸들러 연결
        mqtt_handler.sensing_client.on_message = self.on_message_received

    def on_message_received(self, client, userdata, msg):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        payload = msg.payload.decode()
        self.editor.append(f"[{timestamp}] 수신 메시지: {payload}")
