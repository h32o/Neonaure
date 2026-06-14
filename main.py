import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from view.menu_window import MenuWindow
from view.main_window import MainWindow as GamePage
from controller import Controller
from model import Model
import qasync

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Néonaure")
        self.setStyleSheet("""
            QMainWindow, QStackedWidget {
                background-color: #12121A;
            }""")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu_page = MenuWindow(parent=self)
        self.stack.addWidget(self.menu_page)

        self.game_page = GamePage(parent=self)
        self.stack.addWidget(self.game_page)

async def main_async():
    app = QApplication(sys.argv)
    
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = AppWindow()
    window.show()
    
    model = Model((8,8), "Grille8")
    controller = Controller(model, window)
    
    with loop:                  
        await app.exec_async()     # equivalent to app.exec() but async
    
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main_async())