"""
Module defining the main window of the Néonaure application.

Handles the display of the grid, the timer, the undo/redo buttons, the solve button, and the settings panel.

"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QLabel,QDialog,QFormLayout,QDialogButtonBox,QDoubleSpinBox,QSpinBox,QFileDialog
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, QPropertyAnimation
from PyQt6.QtGui import QKeySequence,QPixmap,QPainter,QColor
from .components.grid_widget import GridWidget
from .settings_window import SettingsWindow

class MainWindow(QWidget):
    """
    Main window of the Néonaure application.

    This class build the user interface of the application.
    And manages the opening and closing of the settings panel, updates the game timer, and forward user actions to the controller via PyQt Signals.

    Signals:
    signal_load_grid (pyqtSignal [str]): Emitted when the user clicks the load button in the settings panel.
    signal_save_grid (pyqtSignal [str]): Emitted when the user clicks the save button in the settings panel.
    signal_reset_grid (pyqtSignal): Emitted when the user clicks the reset button in the settings panel.
    signal_solve_grid (pyqtSignal): Emitted when the user clicks the solve button in the settings panel.
    signal_undo (pyqtSignal): Emitted when the user clicks the undo button 
    signal_redo (pyqtSignal): Emitted when the user clicks the redo button 
    signal_cell_changed (pyqtSignal [int, int, str]): Emitted when the user textualy changes a cell.

    """
    signal_load_grid = pyqtSignal(str)
    signal_save_grid = pyqtSignal(str)
    signal_reset_grid = pyqtSignal()
    signal_solve_grid = pyqtSignal()
    signal_undo = pyqtSignal()
    signal_redo = pyqtSignal()
    signal_cell_changed = pyqtSignal(int, int, str)
    signal_back_to_menu = pyqtSignal()
    signal_hint = pyqtSignal()
    signal_generate_grid = pyqtSignal(int, int, float)


    def __init__(self, parent=None):
        """
        Initialise the main window, set up layouts,create widgets, and connect internal signals to controller.
        """
        super().__init__(parent)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #12121A;
            }
        """)
        
        main_vertical_layout = QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(10, 10, 10, 10)
        main_vertical_layout.setSpacing(0)
   
        self.container = QWidget()
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        main_vertical_layout.setSpacing(0)
        
        self.top_layout = QHBoxLayout(self.container)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName("top-layout")
        
        self.settings_button = QPushButton("☰")
        self.settings_button.setFixedSize(80, 80)
        self.settings_button.setStyleSheet("""
        QPushButton {
            background-color: #2A2A35; 
            color: #E0E0FF; 
            border-radius: 5px; 
            border: 1px solid #383A59;
            font-size: 50px;
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
                font-size: 24px; 
                background-color: transparent;
            }
        """)
        self.top_layout.addWidget(self.pseudo_label)

        self.top_layout.addStretch()

        self.quit_button = QPushButton("✕")
        self.quit_button.setFixedSize(80, 80)
        self.quit_button.setToolTip("Quit application")
        self.quit_button.setStyleSheet("""
        QPushButton {
            background-color: red;
            color: white;
            border-radius: 5px;
            border: 1px solid #383A59;
            font-size: 36px;
            font-weight: bold;
        }
        QPushButton:hover {
            b signal_toggle_timer (pyqtSignal):
    signal_pseudo_changed (pyqtSignal):ackground-color: #C0392B;
            color: #E0E0FF;
            border: 1px solid #C0392B;
        }
        """)
        self.quit_button.clicked.connect(QApplication.instance().quit)
        self.top_layout.addWidget(self.quit_button)

        main_vertical_layout.addWidget(self.container, 0)
        
       
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
        self.settings_panel.signal_generate.connect(self.generate_grid)
        self.settings_panel.signal_quit.connect(self.signal_back_to_menu.emit)
        self.settings_panel.signal_toggle_timer.connect(self.toggle_timer)
        self.settings_panel.signal_pseudo_changed.connect(self.update_pseudo_label)
        self.settings_panel.signal_change_theme.connect(self.Theme_changed)
        
        self.root_layout.addWidget(self.settings_panel)

        self.game_widget = QWidget()
        self.game_layout = QVBoxLayout(self.game_widget)
        self.game_layout.setContentsMargins(0, 0, 0, 0) 
        
        self.root_layout.addWidget(self.game_widget, 1) 
        
        self.game_layout.addStretch(0)

        self.grid_widget = GridWidget()
        self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
        self.game_layout.addWidget(self.grid_widget, 1)
       
        
        self.timer_label = QLabel("")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
            background-color: #1E1E2E;
            border: 1px solid #383A59;
            border-radius: 8px;
            padding: 4px 20px;
            letter-spacing: 4px;
            margin-top: 8px;
            margin-bottom: 4px;
        """)
        self.game_layout.addWidget(self.timer_label, 0, Qt.AlignmentFlag.AlignHCenter)
        self.timer_label.setVisible(False)

        self.game_layout.addStretch(0)

        self.time_counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.timer.start(1000)
        
        self.hint_timer = QTimer(self)
        self.hint_cooldown = 0
        self.hint_timer.timeout.connect(self.update_hint_cooldown)
        
        # ── Bottom bar ──
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

        self.undo_button = QPushButton("↶  Undo")
        self.undo_button.setShortcut("Ctrl+Z")
        self.undo_button.setFixedSize(110, 80)
        self.undo_button.setToolTip("Undo (Ctrl+Z)")
        self.undo_button.setStyleSheet(nav_button_style)
        self.undo_button.clicked.connect(self.undo)
        self.bottom_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("↷  Redo")
        self.redo_button.setShortcut("Ctrl+Y")
        self.redo_button.setFixedSize(110, 80)
        self.redo_button.setToolTip("Redo (Ctrl+Y)")
        self.redo_button.setStyleSheet(nav_button_style)
        self.redo_button.clicked.connect(self.redo)
        self.bottom_layout.addWidget(self.redo_button)

        self.bottom_layout.addStretch()

        self.hint_button = QPushButton("?")
        self.hint_button.setShortcut(QKeySequence("Ctrl+H"))
        self.hint_button.setFixedSize(110, 80)
        self.hint_button.setStyleSheet("""
            background-color: #99cfe0;
            color: white;
            font-size: 35px;
            border-radius: 10px;
        """)
        self.hint_button.clicked.connect(self.give_hint)
        self.bottom_layout.addWidget(self.hint_button)
        
        self.solve_button = QPushButton("Solve  ✓")
        self.solve_button.setFixedSize(110, 80)
        self.solve_button.setToolTip("Solve the grid")
        self.solve_button.setStyleSheet("""
        QPushButton {
            background-color: #9D4EDD;
            color: #E0E0FF;
            border-radius: 8px;
            border: none;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        QPushButton:hover {
            background-color: #B57EDC;
        }
        QPushButton:pressed {
            background-color: #7B2FBE;
        }
        """)
        self.solve_button.clicked.connect(self.solve_grid)
        self.bottom_layout.addWidget(self.solve_button)

        self.game_layout.addLayout(self.bottom_layout, 0)
        
        self.timer_enabled = False
    
    def toggle_settings(self):
        """
        Trigger the sliding animation of the settings panel to open or close it.
        """
        if self.settings_panel.maximumWidth() == 350:
            self.settings_panel.setMinimumWidth(0) 
            self.anim.setStartValue(350)
            self.anim.setEndValue(0)
        else:
            self.anim.setStartValue(0)
            self.anim.setEndValue(350)
            
        self.anim.start()

    def on_anim_finished(self):
        """
        Set the minimum width of the settings panel to 350 when the animation is finished.
        """
        if self.settings_panel.maximumWidth() == 350:
            self.settings_panel.setMinimumWidth(350) 
           
    def update_timer_display(self):
        """
        Update the timer display every second and update the display if the timer is enabled.
        """
        self.time_counter += 1
        if self.timer_enabled:
            minutes = self.time_counter // 60
            seconds = self.time_counter % 60
            self.timer_label.setText(f"{minutes}:{seconds:02d}")

    def toggle_timer(self, is_checked):
        """
        Toggle the timer display and counter updates.

        Args:
            is_checked (bool): True if the timer should be enabled, False otherwise.
        """
        self.timer_enabled = is_checked
        self.timer_label.setVisible(is_checked)
        if is_checked:
            minutes = self.time_counter // 60
            seconds = self.time_counter % 60
            self.timer_label.setText(f"{minutes}:{seconds:02d}")
        else:
            self.timer_label.setText("")       
    def start_hint_cooldown(self, seconds=60):
        self.hint_cooldown = seconds
        self.hint_button.setEnabled(False)
        self.hint_button.setText(str(seconds))
        self.hint_button.setStyleSheet("""
            background-color: grey;
            color: white;
            border-radius: 10px;
        """)
        self.hint_timer.start(1000)

    def update_hint_cooldown(self):
        self.hint_cooldown -= 1
        if self.hint_cooldown <= 0:
            self.hint_timer.stop()
            self.hint_button.setEnabled(True)
            self.hint_button.setText("💡")
            self.hint_button.setStyleSheet("""
                background-color: gold;
                color: white;
                border-radius: 10px;
            """)
        else:
            self.hint_button.setText(str(self.hint_cooldown))
            
    def update_pseudo_label(self, pseudo):
        """
        Update the pseudo label.

        Args:
            pseudo (str): The pseudo of the current player to display.
        """
        self.pseudo_label.setText(f"connected as {pseudo}")

    def show_victory(self):
        """
        Show the victory message.
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("Congratulations !")
        msg.setText("Nice bro, you did it!")
        msg.exec()

    def reset_grid(self):
        """
        Ask for reset grid by emitting a signal.
        """
        print("Request to reset the grid.")
        self.signal_reset_grid.emit()
    
    def load_grid(self):
        """
        Ask for load grid by emitting a signal.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Choose grid", "", ".json")
        if path:
            self.signal_load_grid.emit(path)
        print("Request to load a grid (Ctrl+L).")

    def save_grid(self):
        """
        Ask for save the grid by emitting a signal.
        """
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
        spin_pct.setRange(0, 100)
        spin_pct.setSingleStep(5)
        spin_pct.setValue(35)
        form.addRow("% cases données :", spin_pct)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            row = spin_row.value()
            col = spin_col.value()
            pct = spin_pct.value() / 100
            self.signal_generate_grid.emit(row, col, pct)

    def solve_grid(self):
        """
        Ask for solve the grid by emitting a signal.
        """
        print("Request to solve the grid.")
        self.signal_solve_grid.emit()

    def undo(self):
        """
        Ask for undo by emitting a signal.
        """
        print("Request to undo.")
        self.signal_undo.emit()

    def give_hint(self):
        print("Request to give a hint")
        self.signal_hint.emit()

    def clear_grid(self):
        for cell in self.grid_widget.cells.values():
            self.grid_widget.grid_layout.removeWidget(cell)
            cell.deleteLater()
        self.grid_widget.cells.clear()

    def rebuild_grid(self, rows, cols):
        self.clear_grid()
        self.grid_widget.create_grid(rows, cols)

    def redo(self):
        """
        Ask for redo by emitting a signal.
        """
        print("Request to redo.")
        self.signal_redo.emit()
    
    def update_cell(self, row, col, value):
        """
        Update the text of a cell.
        
        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            value (int): The new value of the cell.
        """
        cell = self.grid_widget.cells[(row, col)]
        cell.blockSignals(True)
        cell.setText("" if value == 0 else str(value))
        cell.blockSignals(False)

    def update_cell_error(self, row, col, is_error):
        """
        Update the color of a cell.
        
        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            is_error (bool): True if the cell should be in error, False otherwise.
        """
        self.grid_widget.change_color_cell_error(row, col, is_error)

    def set_cell_readonly(self, row, col, value):
        """
        Set the value of a cell and make it read-only.
        
        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            value (int): The value of the cell.
        """
        cell = self.grid_widget.cells[(row, col)]
        cell.blockSignals(True)
        cell.set_value(value)
        cell.setReadOnly(True)
        cell.blockSignals(False)
    
    def Theme_changed(self, Theme):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme};
            }}
        """)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(Theme))
        self.setPalette(palette)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())