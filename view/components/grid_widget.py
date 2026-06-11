from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from .cell_widget import CellWidget

class GridWidget(QWidget):
    signal_cell_changed = pyqtSignal(int, int, str)

    def __init__(self):
        super().__init__()
        
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cells = {}   

    def create_grid(self):
        for line in range(8):
            for column in range(8):
                cell = CellWidget(line, column)
                cell.textChanged.connect(self.on_cell_changed)
                self.grid_layout.addWidget(cell, line, column)
                self.cells[(line, column)] = cell

    def on_cell_changed(self, text):
        cell = self.sender()
        if cell:
            self.signal_cell_changed.emit(cell.row, cell.column, text)

    def set_index_cell(self, line, column, value):
        cell = self.cells[(line, column)]
        cell.set_value(value) 

    def change_color_cell_error(self, line, column, is_error):
        cell = self.cells[(line, column)]
        cell.set_error(is_error) 

    def set_cell_borders(self, line, column, top, right, bottom, left):
        cell = self.cells[(line, column)]
        cell.set_borders(top, right, bottom, left) 