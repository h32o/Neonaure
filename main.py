import sys
from PyQt6.QtWidgets import QApplication
from view import MainWindow
from controller import Controller
from model import Model

def main():
    app = QApplication(sys.argv)
    
    model = Model("grille8.json", "Grille 8")
    
 
    view = MainWindow()
    
  
    controller = Controller(model, view)

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
