from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from mqtt.client_manager import MqttManager
from ui.command_tab import CommandTab
from ui.sensing_tab import SensingTab
from ui.ai_prompt_tab import AiPromptTab

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC Car Control")
        self.resize(800, 600)

        self.mqtt_manager = MqttManager(self)

        self.tab_widget = QTabWidget()
        self.command_tab = CommandTab(self.mqtt_manager)
        self.sensing_tab = SensingTab(self.mqtt_manager)
        self.ai_prompt_tab = AiPromptTab()

        self.tab_widget.addTab(self.command_tab, "Command")
        self.tab_widget.addTab(self.sensing_tab, "Sensing")
        self.tab_widget.addTab(self.ai_prompt_tab, "AI Prompt")

        self.stop_btn = QPushButton("정지")
        self.start_btn = QPushButton("시작/종료")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.start_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.stop_btn.clicked.connect(self.command_tab.on_btn_stop)
        self.start_btn.clicked.connect(self.command_tab.on_btn_start)

        self.mqtt_manager.connect_clients()
