import sys
import os 
from PyQt6.QtWidgets import QApplication,QDialog, QMainWindow,QFormLayout, QSpinBox, QDoubleSpinBox, QDialogButtonBox, QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton, QHBoxLayout,QFileDialog,QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence,QPixmap,QPainter
from .components.grid_widget import GridWidget

class MainWindow(QMainWindow):
    signal_load_grid = pyqtSignal(str)
    signal_save_grid = pyqtSignal(str)
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()
    signal_hint = pyqtSignal()
    signal_cell_changed = pyqtSignal(int, int, str)
    signal_background_change = pyqtSignal(str)
    signal_generate_grid = pyqtSignal(int,int,float)

    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Néonaure")
        self.setMinimumSize(600, 600)
        
        self.bg_label = QLabel()
        self.bg_label.setScaledContents(True)
        self.setCentralWidget(self.bg_label)
        self.main_layout = QVBoxLayout(self.bg_label)
         
        """widget_central = QWidget()
        self.setCentralWidget(widget_central)
        self.main_layout = QVBoxLayout(widget_central)"""
        self.init_menu()

        self.time_counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        
        self.grid_widget = GridWidget()
        self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
        self.main_layout.addWidget(self.grid_widget)
        self.grid_widget.create_grid(8,8)
        
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
        
        self.hint_button = QPushButton("💡")
        self.hint_button.setShortcut(QKeySequence("Ctrl+H"))
        self.hint_button.setFixedSize(50, 50)
        self.hint_button.setStyleSheet("""
                background-color: gold; 
                color: white; 
                border-radius: 10px; 
                """)
        self.hint_button.clicked.connect(self.give_hint)
        self.bottom_layout.addWidget(self.hint_button)
        
        self.hint_cooldown = 0
        self.hint_timer = QTimer(self)
        self.hint_timer.timeout.connect(self.update_hint_cooldown)

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
        self._create_action(file_menu, "&Generate grid", "Ctrl+N", self.generate_grid)
        self._create_action(file_menu, "&Quit", "Ctrl+Q", self.close)

        settings_menu = menu_bar.addMenu("&Settings")
        
        self.show_timer_action = QAction("Show timer", self, checkable=True)
        self.show_timer_action.triggered.connect(self.toggle_timer)
        settings_menu.addAction(self.show_timer_action)
        
        self._create_action(settings_menu, "&Game Rules", "Ctrl+G", self.show_rules)

        Theme_menu = menu_bar.addMenu("&Theme")
        
        self._create_action(Theme_menu, "&Change background-image", "Ctrl+B", self.change_background)
        
        
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
    
    def start_hint_cooldown(self,seconds = 1000):
        self.hint_cooldown = seconds
        self.hint_button.setEnabled(False)
        self.hint_button.setText(str(seconds))
        self.hint_button.setStyleSheet("""
                               background-color:grey ;
                               color:white;
                               border-radius: 10px;
                                      
                                       """)
        self.hint_timer.start(1000)
    
    def update_hint_cooldown(self):
        self.hint_cooldown -= 1
        if self.hint_cooldown <= 0:
            self.hint_timer.stop()
            self.hint_button.setEnabled(True)
            self.hint_button.setText('💡')
            self.hint_button.setStyleSheet("""
                background-color: gold; 
                color: white; 
                border-radius: 10px; 
                """)
        else :
            self.hint_button.setText(str(self.hint_cooldown))
    
    def reset_grid(self):
        print("Request to reset the grid.")
        self.signal_reset_grid.emit()
    
    def load_grid(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose grid", "", "")
        if path:
            self.signal_load_grid.emit(path)
        print("Request to load a grid (Crtl+L).")
        

    def save_grid(self):
        path, _ = QFileDialog.getSaveFileName(self, "Choose image", "", ".json")
        if path:
            self.signal_save_grid.emit(path)
        print("Request to save the grid (Ctrl+S).")
        
    def generate_grid(self, checked=False):

        dialog = QDialog(self)
        dialog.setWindowTitle("Générer une grille")

        form = QFormLayout(dialog)

        spin_row = QSpinBox()
        spin_row.setRange(4, 12)
        spin_row.setValue(8)
        form.addRow("Lignes :", spin_row)

        spin_col = QSpinBox()
        spin_col.setRange(4, 12)
        spin_col.setValue(8)
        form.addRow("Colonnes :", spin_col)

        spin_pct = QDoubleSpinBox()
        spin_pct.setRange(0,100)
        spin_pct.setSingleStep(5)
        spin_pct.setValue(35)
        form.addRow("% cases données :", spin_pct)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            row = spin_row.value()
            col = spin_col.value()
            
            pct = spin_pct.value()/100
            print(f"DEBUG {pct}")
            print(f"[DEBUG] generate_grid dialog : row={row}, col={col}, pct={pct}")
            self.signal_generate_grid.emit(row, col, pct)
        
    def clear_grid(self):
        for cell in self.grid_widget.cells.values():
            self.grid_widget.grid_layout.removeWidget(cell)
            cell.deleteLater()
        self.grid_widget.cells.clear()
    
    def rebuild_grid(self, rows, cols):
        self.clear_grid()
        self.grid_widget.create_grid(rows, cols)
        
    def solve_grid(self):
        print("Request to solve the grid.")
        self.signal_solve_grid.emit()

    def undo(self):
        print("Request to undo.")
        self.signal_undo.emit()

    def give_hint(self):
        print("Request to give an hint")
        self.signal_hint.emit()
        
    def toggle_timer(self):
        if self.show_timer_action.isChecked():
            self.timer_label.show()       
            self.timer.start(1000)        
        else:
            self.timer_label.hide()       
            self.timer.stop()
    
    def update_cell(self, row, col, value):
        cell = self.grid_widget.cells[(row, col)]
        cell.blockSignals(True)
        if value == 0:
            cell.setText("")
        else:
            cell.setText(str(value))
        cell.blockSignals(False)
    
    def update_cell_error(self, row, col, is_error):
        self.grid_widget.change_color_cell_error(row, col, is_error)

    def set_cell_readonly(self, row, col, value):
        cell = self.grid_widget.cells[(row, col)]
        cell.blockSignals(True)
        cell.set_value(value)
        cell.setReadOnly(True)
        cell.blockSignals(False)
    
    def change_background(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose image", "", "Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        if path:
            self.signal_background_change.emit(path)
        print("Request to change background-image")

    def set_background(self, path):
        if os.path.exists(path):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                small = pixmap.scaled(
                pixmap.width() // 40,
                pixmap.height() // 40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
                )
                blurred = small.scaled(
                    pixmap.width(),
                    pixmap.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.bg_label.setPixmap(blurred)
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())