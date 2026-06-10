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
    
   
    for (r, c), cell in view.cells.items():
        cell.textChanged.connect(lambda text, row=r, col=c: 
                                 controller.update_cell_value(row, col, text))

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
