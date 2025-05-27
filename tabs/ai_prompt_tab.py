from PyQt6.QtWidgets import (
    QWidget, QTextEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt, QTimer

from prompt import get_response  # GPT 호출 함수


class EnterTextEdit(QTextEdit):
    def __init__(self, on_submit_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_submit = on_submit_callback

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.on_submit()
        else:
            super().keyPressEvent(event)


class AIPromptTab(QWidget):
    def __init__(self, mqtt_handler):
        super().__init__()
        self.mqtt_handler = mqtt_handler

        # 결과 표시 영역
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.result_container = QWidget()
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setSpacing(3)
        self.result_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area.setWidget(self.result_container)

        # 입력 필드
        self.input_field = EnterTextEdit(self.delayed_submit)
        self.input_field.setFixedHeight(50)

        # 제출 버튼
        self.submit_button = QPushButton("제출")
        self.submit_button.setFixedHeight(50)
        self.submit_button.clicked.connect(self.delayed_submit)

        # 입력 영역 수평 정렬
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)

        # 전체 레이아웃
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.addWidget(self.scroll_area)
        layout.addLayout(input_layout)

    def delayed_submit(self):
        QTimer.singleShot(100, self.handle_submit)

    def handle_submit(self):
        user_input = self.input_field.toPlainText().rstrip()
        if user_input:
            try:
                response = get_response(user_input)
                self.display_response(user_input, response)
            except Exception as e:
                self.display_response(user_input, f"[오류 발생] {e}")
            finally:
                self.input_field.clear()

    def display_response(self, user_input, response):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(3)
        layout.setContentsMargins(3, 3, 3, 3)

        input_label = QLabel(f"<b>입력:</b> {user_input}")
        input_label.setWordWrap(True)

        response_label = QLabel(f"<b>응답:</b> {response}")
        response_label.setWordWrap(True)

        exec_button = QPushButton("실행")
        exec_button.clicked.connect(lambda: self.execute(response))

        layout.addWidget(input_label)
        layout.addWidget(response_label)
        layout.addWidget(exec_button)

        # 가장 위에 추가되도록
        self.result_layout.insertWidget(0, frame)
        self.scroll_area.verticalScrollBar().setValue(0)

    def execute(self, response):
        print(f"[EXECUTE] 실행할 응답:\n{response}")
        parsing_commands = [line.strip() for line in response.strip().splitlines() if line.strip()]
        print(f"[EXECUTE] 파싱된 명령어들: {parsing_commands}")
        for command in parsing_commands:
            self.mqtt_handler.publish_command("move", command)
