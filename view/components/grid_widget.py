from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from .cell_widget import CellWidget

class GridWidget(QWidget):
    signal_cell_changed = pyqtSignal(int, int, str)

    def __init__(self, max_lines=8, max_columns=8):
        super().__init__()
        self.max_lines = max_lines
        self.max_columns = max_columns
        
   
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
  
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.outer_layout.addWidget(self.grid_container)
        
        self.cells = {}
        self.create_grid()

    def create_grid(self, row=8, col=8):  # ← col=8 au lieu de col=0
        for line in range(row):
            for column in range(col):
                cell = CellWidget(line, column)
                
                cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
                cell.textChanged.connect(self.on_cell_changed)
                self.grid_layout.addWidget(cell, line, column)
                self.cells[(line, column)] = cell
            
                

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        
        raw_size = min(self.width(), self.height()) - 40 
    
        clean_size = raw_size - (raw_size % self.max_columns)
        
        self.grid_container.setFixedSize(clean_size, clean_size)

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