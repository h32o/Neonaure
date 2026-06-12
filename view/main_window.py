import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QTimer, Qt,QPropertyAnimation
from .components.grid_widget import GridWidget
from .settings_window import SettingsWindow

class MainWindow(QMainWindow):
    signal_load_grid = pyqtSignal()
    signal_save_grid = pyqtSignal()
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()
    signal_redo = pyqtSignal()
    signal_cell_changed = pyqtSignal(int, int, str)

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Néonaure")
        self.setMinimumSize(800, 600) 
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        widget_central.setStyleSheet("""
            QWidget {
                background-color: #12121A;
            }
        """)
        
        main_vertical_layout = QVBoxLayout(widget_central)
        main_vertical_layout.setContentsMargins(10, 10, 10, 10)
        main_vertical_layout.setSpacing(0)
        
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
        self.pseudo_label = QLabel("")
        self.pseudo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pseudo_label.setStyleSheet("""
            QLabel {
                color: #8888AA; 
                font-size: 12px; 
                background-color: transparent;
            }
        """)
        self.top_layout.addWidget(self.pseudo_label)

        self.top_layout.addStretch()

        self.quit_button = QPushButton("✕")
        self.quit_button.setFixedSize(40, 40)
        self.quit_button.setToolTip("Quit application")
        self.quit_button.setStyleSheet("""
        QPushButton {
            background-color: red;
            color: white;
            border-radius: 5px;
            border: 1px solid #383A59;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #C0392B;
            color: #E0E0FF;
            border: 1px solid #C0392B;
        }
        """)
        self.quit_button.clicked.connect(QApplication.instance().quit)
        self.top_layout.addWidget(self.quit_button)

        main_vertical_layout.addLayout(self.top_layout, 0)
        
        self.root_layout = QHBoxLayout()
        self.root_layout.setContentsMargins(0, 10, 0, 0)
        self.root_layout.setSpacing(0) 
        main_vertical_layout.addLayout(self.root_layout, 1)
        
        self.settings_panel = SettingsWindow()
        self.settings_panel.setMinimumWidth(0)
        self.settings_panel.setMaximumWidth(0) 
        
        self.anim = QPropertyAnimation(self.settings_panel, b"maximumWidth")
        self.anim.setDuration(500) 
        self.anim.finished.connect(self.on_anim_finished)
        self.settings_panel.signal_load.connect(self.load_grid)
        self.settings_panel.signal_save.connect(self.save_grid)
        self.settings_panel.signal_reset.connect(self.reset_grid)
        self.settings_panel.signal_quit.connect(QApplication.instance().quit)
        self.settings_panel.signal_toggle_timer.connect(self.toggle_timer)
        self.settings_panel.signal_pseudo_changed.connect(self.update_pseudo_label)
        
        self.root_layout.addWidget(self.settings_panel)

        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout(self.game_widget)
        self.game_layout.setContentsMargins(0, 0, 0, 0) 
        
        self.root_layout.addWidget(self.game_widget, 1) 
        
        self.game_layout.addStretch(1)

        self.grid_widget = GridWidget()
        self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
        self.game_layout.addWidget(self.grid_widget, 0)
        self.grid_widget.create_grid()
        
        self.timer_label = QLabel("") 
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 36px; font-weight: bold; color: #ffffff; "
            "letter-spacing: 4px; margin-top: 2px; margin-bottom: 4px;"
        )
        self.game_layout.addWidget(self.timer_label, 0)

        self.game_layout.addStretch(1)

        self.time_counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.timer.start(1000)
        
        nav_button_style = """
        QPushButton {
            background-color: #2A2A35;
            color: #E0E0FF;
            border-radius: 8px;
            border: 1px solid #383A59;
            font-size: 22px;
        }
        QPushButton:hover {
            background-color: #383A59;
        }
        """

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(5, 5, 5, 5)
        self.bottom_layout.setSpacing(8)

        self.undo_button = QPushButton("↶")
        self.undo_button.setShortcut("Ctrl+Z")
        self.undo_button.setFixedSize(45, 45)
        self.undo_button.setToolTip("Cancel (Ctrl+Z)")
        self.undo_button.setStyleSheet(nav_button_style)
        self.undo_button.clicked.connect(self.undo)
        self.bottom_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("↷")
        self.redo_button.setShortcut("Ctrl+Y")
        self.redo_button.setFixedSize(45, 45)
        self.redo_button.setToolTip("Redo (Ctrl+Y)")
        self.redo_button.setStyleSheet(nav_button_style)
        self.redo_button.clicked.connect(self.redo)
        self.bottom_layout.addWidget(self.redo_button)

        self.bottom_layout.addStretch()

        self.solve_button = QPushButton("✓")
        self.solve_button.setFixedSize(50, 50)
        self.solve_button.setToolTip("Solve the grid")
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
        if self.settings_panel.maximumWidth() == 350:
            self.settings_panel.setMinimumWidth(0) 
            self.anim.setStartValue(350)
            self.anim.setEndValue(0)
        else:
            self.anim.setStartValue(0)
            self.anim.setEndValue(350)
            
        self.anim.start()

    def on_anim_finished(self):
        if self.settings_panel.maximumWidth() == 350:
            self.settings_panel.setMinimumWidth(350) 
           
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
    
    def update_pseudo_label(self, pseudo):
        self.pseudo_label.setText(f"connected as {pseudo}")

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

    def redo(self):
        print("Request to redo.")
        self.signal_redo.emit()
    
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