import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWidget
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec())
