from PyQt6.QtWidgets import (
    QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSlider, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QPixmap
import os
from dotenv import load_dotenv
from mjpeg_stream import MjpegStreamReader

load_dotenv(override=True)
MJPEG_STREAM_URL = os.getenv("MJPEG_STREAM_URL")

class CommandTab(QWidget):
    def __init__(self, mqtt_handler):
        super().__init__()
        self.mqtt = mqtt_handler
        self.is_started = False

        # 텍스트 에디터
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("명령을 입력하세요...")

        # MJPEG 스트림 레이블
        self.mjpeg_label = QLabel("MJPEG 스트림 준비중...")
        self.mjpeg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reader = MjpegStreamReader(MJPEG_STREAM_URL)
        self.reader.frame_received.connect(self.update_image)
        self.reader.start()

        # 이동 버튼
        self.btn_forward = QPushButton("전진")
        self.btn_backward = QPushButton("후진")
        self.btn_left = QPushButton("좌")
        self.btn_right = QPushButton("우")
        self.btn_stop = QPushButton("정지")

        # 속도 조절
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(0, 255)
        self.speed_slider.setValue(255)

        self.speed_edit = QLineEdit("255")
        self.speed_edit.setValidator(QIntValidator(0, 255, self))
        self.speed_edit.setMaximumWidth(50)
        self.speed_label = QLabel("속도: 255")

        # 버튼 연결
        self.btn_forward.clicked.connect(lambda: self.send_command("GO"))
        self.btn_backward.clicked.connect(lambda: self.send_command("BACK"))
        self.btn_left.clicked.connect(lambda: self.send_command("LEFT"))
        self.btn_right.clicked.connect(lambda: self.send_command("RIGHT"))
        self.btn_stop.clicked.connect(lambda: self.send_command("STOP"))

        self.speed_slider.valueChanged.connect(self.update_speed)
        self.speed_edit.editingFinished.connect(self.set_speed_from_edit)

        # 레이아웃 구성
        main_layout = QVBoxLayout(self)

        # 에디터와 MJPEG를 가로로 반반 크기로 배치
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.editor)
        top_layout.addWidget(self.mjpeg_label)

        top_layout.setStretch(0, 1)
        top_layout.setStretch(1, 1)

        main_layout.addLayout(top_layout)

        move_layout = QHBoxLayout()
        move_layout.addWidget(self.btn_forward)
        move_layout.addWidget(self.btn_backward)
        move_layout.addWidget(self.btn_left)
        move_layout.addWidget(self.btn_right)
        move_layout.addWidget(self.btn_stop)
        main_layout.addLayout(move_layout)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("속도 설정:"))
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_edit)
        speed_layout.addWidget(self.speed_label)
        main_layout.addLayout(speed_layout)

    def update_image(self, jpg_bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(jpg_bytes, "JPEG")
        self.mjpeg_label.setPixmap(pixmap.scaled(
            self.mjpeg_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def send_command(self, cmd):
        self.editor.append(f"Command sent: {cmd}")
        self.mqtt.publish_command("move", cmd)

    def update_speed(self, value):
        self.speed_label.setText(f"속도: {value}")
        self.speed_edit.setText(str(value))
        self.mqtt.publish_command("speed", str(value))

    def set_speed_from_edit(self):
        value = int(self.speed_edit.text())
        self.speed_slider.setValue(value)

    def toggle_start(self):
        self.is_started = not self.is_started
        self.editor.append("START" if self.is_started else "STOP")

    def stop_action(self):
        self.editor.append("정지 명령 실행")
        self.send_command("STOP")

    def closeEvent(self, event):
        if self.reader and self.reader.isRunning():
            self.reader.stop()
        event.accept()
