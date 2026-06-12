import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Signal as pyqtSignal, QTimer, Qt
from .components.grid_widget import GridWidget
from .settings_window import SettingsWindow

class MainWindow(QWidget):
    signal_load_grid = pyqtSignal()
    signal_save_grid = pyqtSignal()
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()
    signal_cell_changed = pyqtSignal(int, int, str)
    signal_back_to_menu = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMinimumSize(800, 600) 
        self.setStyleSheet("""
            QWidget {
                background-color: #12121A;
            }
        """)
        
        main_vertical_layout = QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(10, 10, 10, 10)
        main_vertical_layout.setSpacing(0)
        
        # ── Top bar ──
        self.top_layout = QHBoxLayout()
        
        self.settings_button = QPushButton("☰")
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setStyleSheet("""
        QPushButton {
            background-color: #2A2A35; 
            color: #E0E0FF; 
            border-radius: 5px; 
            border: 1px solid #383A59;
            font-size: 25px;
        }
        QPushButton:hover {
            background-color: #383A59;
        }
        """)
        self.settings_button.clicked.connect(self.toggle_settings) 
        self.top_layout.addWidget(self.settings_button) 
        self.top_layout.addStretch() 
        main_vertical_layout.addLayout(self.top_layout, 0)
        
        # ── Middle: settings + game ──
        self.root_layout = QHBoxLayout()
        self.root_layout.setContentsMargins(0, 10, 0, 0)
        self.root_layout.setSpacing(0) 
        main_vertical_layout.addLayout(self.root_layout, 1)
        
        self.settings_panel = SettingsWindow()
        self.settings_panel.setFixedWidth(350) 
        self.settings_panel.hide() 

        self.settings_panel.signal_load.connect(self.load_grid)
        self.settings_panel.signal_save.connect(self.save_grid)
        self.settings_panel.signal_reset.connect(self.reset_grid)
        self.settings_panel.signal_quit.connect(self.signal_back_to_menu.emit)
        self.settings_panel.signal_toggle_timer.connect(self.toggle_timer)
        
        self.root_layout.addWidget(self.settings_panel)

        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout(self.game_widget)
        self.game_layout.setContentsMargins(0, 0, 0, 0) 
        
        self.root_layout.addWidget(self.game_widget, 1) 
        
        self.grid_widget = GridWidget()
        self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
        self.game_layout.addWidget(self.grid_widget, 1)
        self.grid_widget.create_grid()
        
        self.timer_label = QLabel("") 
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 10px; margin-bottom: 10px;")
        self.game_layout.addWidget(self.timer_label, 0)
        
        self.time_counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.timer.start(1000)
        
        # ── Bottom bar ──
        self.bottom_layout = QHBoxLayout()
        
        self.undo_button = QPushButton("↶")
        self.undo_button.setShortcut("Ctrl+Z")
        self.undo_button.setFixedSize(50, 50)
        self.undo_button.setStyleSheet("""
        QPushButton {
            background-color: #2A2A35; 
            color: #E0E0FF; 
            border-radius: 10px; 
            border: 1px solid #383A59;
            font-size: 25px;
            margin-left: 10px;
        }
        QPushButton:hover {
            background-color: #383A59;
        }
        """)
        self.undo_button.clicked.connect(self.undo)
        self.bottom_layout.addWidget(self.undo_button)

        self.bottom_layout.addStretch()

        self.solve_button = QPushButton("✓")
        self.solve_button.setFixedSize(50, 50)
        self.solve_button.setStyleSheet("""
        QPushButton {
            background-color: #9D4EDD; 
            color: #E0E0FF; 
            border-radius: 10px; 
            border: none;
            font-size: 25px;
        }
        QPushButton:hover {
            background-color: #B57EDC;
        }
        """)
        self.solve_button.clicked.connect(self.solve_grid)
        self.bottom_layout.addWidget(self.solve_button)
        
        self.game_layout.addLayout(self.bottom_layout, 0)
        
        self.timer_enabled = False
    
    def toggle_settings(self):
        if self.settings_panel.isVisible():
            self.settings_panel.hide()
        else:
            self.settings_panel.show()
            
    def update_timer_display(self):
        self.time_counter += 1
        if self.timer_enabled:
            minutes = self.time_counter // 60
            seconds = self.time_counter % 60
            self.timer_label.setText(f"{minutes}:{seconds:02d}")

    def toggle_timer(self, is_checked):
        self.timer_enabled = is_checked
        if is_checked:
            minutes = self.time_counter // 60
            seconds = self.time_counter % 60
            self.timer_label.setText(f"{minutes}:{seconds:02d}")
        else:
            self.timer_label.setText("")       
    
    def show_victory(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Congratulations !")
        msg.setText("Nice bro, you did it!")
        msg.exec()

    def reset_grid(self):
        print("Request to reset the grid.")
        self.signal_reset_grid.emit()
    
    def load_grid(self):
        print("Request to load a grid (Ctrl+L).")
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
    
    def update_cell(self, row, col, value):
        self.grid_widget.cells[(row, col)].setText(str(value))
    
    def update_cell_error(self, row, col, is_error):
        self.grid_widget.change_color_cell_error(row, col, is_error)

    def set_cell_readonly(self, row, col, value):
        self.grid_widget.cells[(row, col)].set_value(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())