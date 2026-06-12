import sys
from PyQt6.QtWidgets import QApplication
from view import MainWindow
from controller import Controller
from model import Model
from view.menu_window import MenuWindow

def main():
    app = QApplication(sys.argv)
    controller = Controller(Model((8,8),"Grille8"), MenuWindow())
    sys.exit(app.exec())

if __name__ == "__main__":
    main()