import sys
from PyQt6.QtWidgets import QApplication
from view import MainWindow
from controller import Controller
from model import Model
from view.menu_window import MenuWindow

def main():
    app = QApplication(sys.argv)
    menu = MenuWindow()
    menu.show()

    def launch_game():
        controller = Controller(Model((8,8),"Grille8"), MainWindow())
        menu.close()
        controller.run()
        
    menu.signal_start_game.connect(launch_game)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()