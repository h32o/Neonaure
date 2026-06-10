import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QRegularExpression, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QRegularExpressionValidator 

class MainWindow(QMainWindow):
    signal_load_grid = pyqtSignal()
    signal_save_grid = pyqtSignal()
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Néonaure")
        self.setMinimumSize(600, 600) 
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        self.main_layout = QVBoxLayout(widget_central)
        self.init_menu()

        self.time_counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_layout.addLayout(self.grid_layout)
        
        self.bottom_layout = QHBoxLayout()
        
        self.undo_button = QPushButton("↶")
        self.undo_button.setFixedSize(50, 50)
        self.undo_button.setStyleSheet("""
                background-color: grey; 
                color: white; 
                border-radius: 10px; 
                """)
        self.undo_button.clicked.connect(self.undo)
        self.bottom_layout.addWidget(self.undo_button)

        self.bottom_layout.addStretch()

        self.solve_button = QPushButton("✓")
        self.solve_button.setFixedSize(50, 50)
        self.solve_button.setStyleSheet("""
                background-color: green; 
                color: white; 
                border-radius: 10px; 
                """)
        self.solve_button.clicked.connect(self.solve_grid)
        self.bottom_layout.addWidget(self.solve_button)
        
        self.main_layout.addLayout(self.bottom_layout)
        
        self.cells = {}   
        self.create_grid()
    
    def init_menu(self):
        menu_bar = self.menuBar() 

        file_menu = menu_bar.addMenu("&File")
        self._create_action(file_menu, "&Reset grid", "Ctrl+R", self.reset_grid)
        self._create_action(file_menu, "&Load grid", "Ctrl+L", self.load_grid)
        self._create_action(file_menu, "&Save grid", "Ctrl+S", self.save_grid)
        self._create_action(file_menu, "&Quit", "Ctrl+Q", self.close)

        settings_menu = menu_bar.addMenu("&Settings")
        
        self.show_timer_action = QAction("Show timer", self, checkable=True)
        self.show_timer_action.triggered.connect(self.toggle_timer)
        settings_menu.addAction(self.show_timer_action)
        
        self._create_action(settings_menu, "&Game Rules", "Ctrl+H", self.show_rules)

        self.timer_label = QLabel("0s  ", self) 
        self.timer_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff;")
        self.timer_label.hide()  
        
        menu_bar.setCornerWidget(self.timer_label, Qt.Corner.TopRightCorner)

    def _create_action(self, menu, text, shortcut, slot_function):
        action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot_function)
        menu.addAction(action)
        return action 

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
                cell.setStyleSheet("""
                    background-color: white;
                    border: 0.5px solid black;
                    color: black;
                    font-weight : bold;                  
                """)
                cell.row = line
                cell.column = column
                cell.textChanged.connect(self.on_cell_changed)
                self.grid_layout.addWidget(cell, line, column)
                self.cells[(line, column)] = cell

    def on_cell_changed(self, text):
        pass

    def show_rules(self):
        rules_box = QMessageBox(self)
        rules_box.setWindowTitle("Règles du Néonaure")   
        rules_box.setText(
            "Bienvenue dans le Néonaure !\n"
            "Voici les règles pour résoudre la grille :\n\n"
            "• un chiffre par case\n"
            "• un chiffre doit être entouré de chiffres différents (y compris en diagonale)\n"
            "• un motif de N cases (repéré en traits gras) doit comporter tous les chiffres de 1 à N\n"
        )
        rules_box.exec()
    
    def show_victory(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Congratulations !")
        msg.setText("Nice bro, you did it!")
        msg.exec()

    def update_timer_display(self):
        self.time_counter += 1
        self.timer_label.setText(f"{self.time_counter}s")

    def reset_grid(self):
        print("Request to reset the grid.")
        self.signal_reset_grid.emit()
    
    def load_grid(self):
        print("Request to load a grid (Crtl+L).")
        self.signal_load_grid.emit()

    def save_grid(self):
        print("Request to save the grid (Ctrl+S).")
        self.signal_save_grid.emit()

    def solve_grid(self):
        print("Request to solve the grid.")
        self.signal_solve_grid.emit()

    def undo(self):
        print("Request to undo.")
        self.signal_undo.emit()

    def toggle_timer(self):
        if self.show_timer_action.isChecked():
            self.timer_label.show()       
            self.timer.start(1000)        
        else:
            self.timer_label.hide()       
            self.timer.stop()         

    def set_index_cell(self, line, column, value):
        cell = self.cells[(line, column)]
        cell.setText(str(value))
        cell.setReadOnly(True)
        cell.setStyleSheet("""
        background-color: #E0E0E0;
        border: 0.5px solid black;
        color: #333333;
        font-weight: bold;
         """)    
    
    def change_color_cell_error(self, line, column, is_error):
        cell = self.cells[(line, column)]
        if cell.isReadOnly():
            return 
        if is_error:
            cell.setStyleSheet("background-color: #FFCCCC;")
        else:
            cell.setStyleSheet("background-color: white;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())