import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QRegularExpression 
from PyQt6.QtGui import QAction, QRegularExpressionValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Néonaure")
        self.setMinimumSize(600, 600) 
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        self.main_layout = QVBoxLayout(widget_central)
        self.init_menu()

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_layout.addLayout(self.grid_layout)
        
        self.create_grid()
    
    def init_menu(self):
        menu_bar = self.menuBar() 

        file_menu = menu_bar.addMenu("&File")
        
        reset_action = QAction("&Reset grid", self)
        reset_action.triggered.connect(self.reset_grid)
        reset_action.setShortcut("Ctrl+R")
        file_menu.addAction(reset_action)

        load_action = QAction("&Load grid", self)
        load_action.triggered.connect(self.load_grid)
        load_action.setShortcut("Ctrl+L")
        file_menu.addAction(load_action)
        
        save_action = QAction("&Save grid", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_grid)
        file_menu.addAction(save_action)
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        settings_menu = menu_bar.addMenu("&Settings")

        self.show_timer_action = QAction("Show timer", self, checkable=True)
        self.show_timer_action.triggered.connect(self.toggle_timer)
        settings_menu.addAction(self.show_timer_action)

        
        rules_action = QAction("&Game Rules", self)
        rules_action.setShortcut("Ctrl+H")  
        rules_action.triggered.connect(self.show_rules)
        settings_menu.addAction(rules_action)

    def create_grid(self):
        regex = QRegularExpression("^[1-5]$")
        validator = QRegularExpressionValidator(regex, self)
        
        for line in range(8):
            for column in range(8):
                cell = QLineEdit()
                cell.setValidator(validator)
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFixedSize(50, 50)                
                self.grid_layout.addWidget(cell, line, column)

    def show_rules(self):
        rules_box = QMessageBox(self)
        rules_box.setWindowTitle("Règles du Néonaure")   
        rules_box.setText("Bienvenue dans le Néonaure !\n"
            "Voici les règles pour résoudre la grille :\n\n"
            "• un chiffre par case\n"
            "• un chiffre doit être entouré de chiffres différents (y compris en diagonale)\n "
            "• un motif de N cases (repéré en traits gras) doit comporter tous les chiffres de 1 à N\n"
           )
        rules_box.exec()

    def reset_grid(self):
        print("Request to reset the grid.")
    
    def load_grid(self):
        print("Request to load a grid (Crtl+L).")

    def save_grid(self):
        print("Request to save the grid (Ctrl+S).")

    def toggle_timer(self):
        if self.show_timer_action.isChecked():
            print("Timer will be shown.")
        else:
            print("Timer will be hidden.")
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())