from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class AIPromptTab(QWidget):
    def __init__(self):
        super().__init__()
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

    def append_analysis(self, text):
        self.editor.append(text)
