import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Signal as pyqtSignal
from PySide6.QtGui import QAction, QKeySequence
from .components.grid_widget import GridWidget

class MainWindow(QMainWindow):
    signal_load_grid = pyqtSignal()
    signal_save_grid = pyqtSignal()
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()
    signal_cell_changed = pyqtSignal(int, int, str)

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
        
        self.grid_widget = GridWidget()
        self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
        self.main_layout.addWidget(self.grid_widget)
        self.grid_widget.create_grid()
        
        self.bottom_layout = QHBoxLayout()
        
        self.undo_button = QPushButton("↶")
        self.undo_button.setShortcut(QKeySequence("Ctrl+Z"))
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
        self.timer_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff; margin-right: 70px;")
        self.timer_label.hide()  
        
        menu_bar.setCornerWidget(self.timer_label, Qt.Corner.TopRightCorner)

    def _create_action(self, menu, text, shortcut, slot_function):
        action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot_function)
        menu.addAction(action)
        return action 

    def show_rules(self):
        rules_box = QMessageBox(self)
        rules_box.setWindowTitle("Rules of the Néonaure")   
        rules_box.setText(
            "Welcome to the Néonaure!\n"
            "Here are the rules for solving the grid:\n\n"
            "• one number per cell\n"
            "• a number must be surrounded by different numbers (including diagonally)\n"
            "• a pattern of N cells (marked with bold lines) must contain all numbers from 1 to N\n"
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
    
    def update_cell(self, row, col, value):
        self.grid_widget.cells[(row, col)].setText(str(value))
    
    def update_cell_error(self, row, col, is_error):
        self.grid_widget.change_color_cell_error(row, col, is_error)

    def set_cell_readonly(self, row, col, value):
        self.grid_widget.cells[(row, col)].set_value(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())