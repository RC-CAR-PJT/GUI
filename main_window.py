from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QTabWidget
from tabs.command_tab import CommandTab
from tabs.sensing_tab import SensingTab
from tabs.ai_prompt_tab import AIPromptTab
from mqtt_handler import MQTTHandler


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC Car Control with MJPEG Viewer")
        self.resize(900, 700)

        # MQTT 핸들러
        self.mqtt_handler = MQTTHandler()

        # 탭 생성
        self.tab_widget = QTabWidget()
        self.command_tab = CommandTab(self.mqtt_handler)
        self.sensing_tab = SensingTab(self.mqtt_handler)
        self.ai_prompt_tab = AIPromptTab(self.mqtt_handler)

        self.tab_widget.addTab(self.command_tab, "Command")
        self.tab_widget.addTab(self.sensing_tab, "Sensing")
        self.tab_widget.addTab(self.ai_prompt_tab, "AI Prompt")

        # Action 버튼
        self.start_btn = QPushButton("시작/종료")
        self.stop_btn = QPushButton("정지")
        self.start_btn.clicked.connect(self.command_tab.toggle_start)
        self.stop_btn.clicked.connect(self.command_tab.stop_action)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.start_btn)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        self.mqtt_handler.shutdown()
        event.accept()
