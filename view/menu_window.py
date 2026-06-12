from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
import sys


class MenuWindow(QMainWindow):
    signal_start_game = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Néonaure - Menu")
        self.setMinimumSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("""
            QWidget {
                background-color: #12121A;
            }
            QPushButton {
                background-color: #2A2A35;
                color: #E0E0FF;
                border: 1px solid #383A59;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #383A59;
            }
        """)

        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        play_button = QPushButton("Play")
        play_button.setFixedSize(200, 50)
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #9D4EDD;
                color: #E0E0FF;
                border: none;
                border-radius: 10px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #B57EDC;
            }
        """)
        play_button.clicked.connect(self.start_game)
        main_layout.addWidget(play_button)

        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(200, 50)
        quit_button.clicked.connect(self.close)
        main_layout.addWidget(quit_button)

        self._main_window = None

    def start_game(self):
        self.signal_start_game.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())