import os, sys, glob, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton, QHBoxLayout,QScrollArea,QApplication,QDialog, QMainWindow,QFormLayout, QSpinBox, QDoubleSpinBox, QDialogButtonBox, QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton, QHBoxLayout,QFileDialog,QGraphicsScene, QGraphicsPixmapItem, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QKeySequence,QPixmap,QPainter,QColor, QPen
from .components.grid_widget import GridWidget
from view.settings_window import SettingsWindow
from view.components.grid_carrousel import GridCarousel
from view.components.grid_thumbnail import GridThumbnail

class BackgroundWidget(QWidget):
    """Widget qui dessine une image floue en fond derrière ses enfants."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_pixmap = None

    def set_bg_pixmap(self, pixmap):
        self._bg_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._bg_pixmap and not self._bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            scaled = self._bg_pixmap.scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
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
    signal_back_to_menu = pyqtSignal()
    
    def __init__(self, parent=None):
            super().__init__(parent)
            
            self.setMinimumSize(800, 600) 
            self.setStyleSheet("""
                QWidget {
                    background-color: #12121A;
                BackgroundWidget {
                    background-color: transparent;
                }
                }
            """)
            
            
            central = BackgroundWidget()
            self.setCentralWidget(central)
            main_vertical_layout = QVBoxLayout(central)
            main_vertical_layout.setContentsMargins(10, 10, 10, 10)
            main_vertical_layout.setSpacing(0)
            
            
            # ── Top bar ──
            self.top_layout = QHBoxLayout()
            
            self.settings_button = QPushButton("☰")
            self.settings_button.setFixedSize(80,80)
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
            self.settings_panel.signal_background_change.connect(self.change_background)
            self.root_layout.addWidget(self.settings_panel)

            self.game_widget = QWidget()
            self.game_layout = QVBoxLayout(self.game_widget)
            self.game_layout.setContentsMargins(0, 0, 0, 0)

            self.root_layout.addWidget(self.game_widget, 1)

            self.grid_widget = GridWidget()
            self.grid_widget.setStyleSheet("background-color: transparent;")
            self.grid_widget.signal_cell_changed.connect(self.signal_cell_changed)
            self.game_layout.addWidget(self.grid_widget, 1)
            self.grid_widget.create_grid()
            
            # ── Timer label ──
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
            
            # ── Carousel panel (close) ──
            self.carousel_panel = QWidget()
            self.carousel_panel.setMaximumHeight(0)
            self.carousel_panel.setStyleSheet("background-color: #1A1A28; border-top: 1px solid #383A59;")
            
            cp_layout = QHBoxLayout(self.carousel_panel)
            cp_layout.setContentsMargins(12, 8, 12, 8)
            
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setStyleSheet("border: none; background: transparent;")
            
            thumb_container = QWidget()
            thumb_container.setStyleSheet("background: transparent;")
            
            self._thumbs_layout = QHBoxLayout(thumb_container)
            self._thumbs_layout.setSpacing(12)
            self._thumbs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            for path in sorted(glob.glob(os.path.join("examples/", "*.json"))):
                name = os.path.splitext(os.path.basename(path))[0]
                thumb = GridThumbnail(path, name)
                thumb.clicked.connect(self._on_grid_selected)
                self._thumbs_layout.addWidget(thumb)
            scroll.setWidget(thumb_container)
            
            cp_layout.addWidget(scroll)
            self.game_layout.addWidget(self.carousel_panel, 0)
            
            self._carousel_anim = QPropertyAnimation(self.carousel_panel, b"maximumHeight")
            self._carousel_anim.setDuration(280)
            self._carousel_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self._carousel_open = False

            # ── Bottom bar ──
            
            self.undo_button = QPushButton("↶")
            self.undo_button.setShortcut("Ctrl+Z")
            self.undo_button.setFixedSize(80,80)
            self.undo_button.setStyleSheet("""
            QPushButton {
                background-color: #2A2A35; 
                color: #E0E0FF; 
                border-radius: 10px; 
                border: 1px solid #383A59;
                font-size: 50px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #383A59;
            }
            """)
            self.undo_button.clicked.connect(self.undo)
            self.bottom_layout.addWidget(self.undo_button)

            self.hint_button = QPushButton("💡")
            self.hint_button.setShortcut(QKeySequence("Ctrl+H"))
            self.hint_button.setFixedSize(80,80)
            self.hint_button.setStyleSheet("""
                    background-color: gold; 
                    color: white; 
                    border-radius: 10px; 
                    font-size: 50px;
                    """)
            self.hint_button.clicked.connect(self.give_hint)
            self.bottom_layout.addWidget(self.hint_button)
            
            self.hint_timer = QTimer(self)
            self.hint_cooldown = 0
            self.hint_timer.timeout.connect(self.update_hint_cooldown)
            
            self.bottom_layout.addStretch()

            self.carousel_btn = QPushButton("▼  Grilles")
            self.carousel_btn.setFixedSize(160, 80)
            self.carousel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E6E6E; color: #E0E0FF;
                border-radius: 10px; border: none; font-size: 22px;
            }
            QPushButton:hover { background-color: #28908F; }
            """)
            self.carousel_btn.clicked.connect(self.toggle_carousel)
            self.bottom_layout.addWidget(self.carousel_btn)

            self.bottom_layout.addStretch()

            self.solve_button = QPushButton("✓")
            self.solve_button.setFixedSize(80,80)
            self.solve_button.setStyleSheet("""
            QPushButton {
                background-color: #9D4EDD; 
                color: #E0E0FF; 
                border-radius: 10px; 
                border: none;
                font-size: 50px;
            }
            QPushButton:hover {
                background-color: #B57EDC;
            }
            """)
            self.solve_button.clicked.connect(self.solve_grid)
            self.bottom_layout.addWidget(self.solve_button)
            
            self.game_layout.addLayout(self.bottom_layout, 0)
            
            self.timer_enabled = False
            
            self.settings_panel.signal_generate.connect(self.generate_grid)

    def _create_action(self, menu, text, shortcut, slot_function):
        action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot_function)
        menu.addAction(action)
        return action 

    def _on_grid_selected(self, path: str):
        self.signal_load_grid.emit(path)
        self._close_carousel()

    def toggle_carousel(self):
        if self._carousel_open:
            self._close_carousel()
        else:
            self._open_carousel()

    def _open_carousel(self):
        self._carousel_open = True
        self.carousel_btn.setText("▲  Grilles")
        self._carousel_anim.stop()
        self._carousel_anim.setStartValue(self.carousel_panel.maximumHeight())
        self._carousel_anim.setEndValue(210)
        self._carousel_anim.start()

    def _close_carousel(self):
        self._carousel_open = False
        self.carousel_btn.setText("▼  Grilles")
        self._carousel_anim.stop()
        self._carousel_anim.setStartValue(self.carousel_panel.maximumHeight())
        self._carousel_anim.setEndValue(0)
        self._carousel_anim.start()
        
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
            
    def start_hint_cooldown(self,seconds = 60):
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
                self.centralWidget().set_bg_pixmap(blurred)
               
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())