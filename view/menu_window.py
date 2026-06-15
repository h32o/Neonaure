"""
Module for the menu window.

Provides  a clean interface for the user to start a new game or exit the application.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal,QSize
from PyQt6.QtGui import QPixmap
import sys

class MenuWindow(QWidget):    
    """
    Main menu window for the Néonaure application.

    This window serves as the starting point for the user, offering the choice to start a new game or exit the application.

    Signals:
    signal_start_game (pyqtSignal): Emitted when the user clicks the start game button.
    """                      
    signal_start_game = pyqtSignal()
    def __init__(self, parent=None):    
        """
        Initialize the menu window and set up the layout and buttons.
        """            
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

        logo = QLabel()
        pixmap = QPixmap("assets/misc/images/logo-neonaur.png").scaled(QSize(200,200), Qt.AspectRatioMode.KeepAspectRatio)
        logo.setPixmap(pixmap)
        main_layout.addWidget(logo)
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
        """
        Ask for start the game by emmiting a signal.
        """
        self.signal_start_game.emit()

    def start_quit(self):
        """
        Ask for quitting the application by emitting a signal.
        """
        QApplication.instance().quit()