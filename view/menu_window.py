from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
import sys


class MenuWindow(QWidget):                          
    signal_start_game = pyqtSignal()
    def __init__(self, parent=None):                
        super().__init__(parent)                    

        self.setStyleSheet("""                    
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

        main_layout = QVBoxLayout(self)
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
        quit_button.clicked.connect(self.start_quit)
        main_layout.addWidget(quit_button)

    def start_game(self):
        self.signal_start_game.emit()

    def start_quit(self):
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()