import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from view.menu_window import MenuWindow
from view.main_window import MainWindow as GamePage
from controller import Controller
from model import Model

class AppWindow(QMainWindow):
    """Single QMainWindow for Android — holds all pages in a QStackedWidget."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Néonaure")
        self.setStyleSheet("""
            QMainWindow, QStackedWidget {
                background-color: #12121A;
            }""")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Menu
        self.menu_page = MenuWindow(parent=self)
        self.stack.addWidget(self.menu_page)

        # Game
        self.game_page = GamePage(parent=self)
        self.stack.addWidget(self.game_page)

def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    controller = Controller(Model((8,8), "selima"), window)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()