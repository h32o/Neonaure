"""
Module of the grid widget.

This widget is the main widget of the game, it contains the grid of cells.
"""
from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal as pyqtSignal, QSize
from .cell_widget import CellWidget

class GridWidget(QWidget):
    """
    A widget representing the grid of the game.

    Signals:
    signal_cell_changed (pyqtSignal): Emitted when a cell is changed.
    """
    signal_cell_changed = pyqtSignal(int, int, str)

    def __init__(self, max_lines=8, max_columns=8):
        """
        Initialize the grid widget and set up the grid layout.

        Args:
            max_lines (int): The maximum number of lines in the grid.
            max_columns (int): The maximum number of columns in the grid.
        """
        super().__init__()
        self.max_lines = max_lines
        self.max_columns = max_columns

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(200, 200)
        
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.outer_layout.addWidget(self.grid_container)
        
        self.cells = {}
        self.create_grid()

    def create_grid(self,row = 8, col = 8):
        """
        Create the grid of cells.

        Args:
            row (int): The number of rows in the grid.
            col (int): The number of columns in the grid.
        """
        for line in range(row):
            for column in range(col):
                cell = CellWidget(line, column)
                cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                cell.textChanged.connect(self.on_cell_changed)
                self.grid_layout.addWidget(cell, line, column)
                self.cells[(line, column)] = cell

    def resizeEvent(self, event):
        """
        Handle the resize event of the grid widget.

        Args:
            event (QResizeEvent): The resize event.
        """
        super().resizeEvent(event)
        
        raw_size = min(self.width(), self.height()) - 40 

        if raw_size < 0:
            return 
            
        clean_size = raw_size - (raw_size % self.max_columns)
        
        if clean_size > 0:
            self.grid_container.setFixedSize(clean_size, clean_size)

    def on_cell_changed(self, text):
        """
        Handle the change of a cell value.

        Args:
            text (str): The new value of the cell.
        """
        cell = self.sender()
        if cell:
            self.signal_cell_changed.emit(cell.row, cell.column, text)

    def set_index_cell(self, line, column, value):
        """
        Set a cell value and make it read-only.

        Args:
            line (int): The line of the cell.
            column (int): The column of the cell.
            value (int): The value of the cell.
        """
        cell = self.cells[(line, column)]
        cell.set_value(value) 

    def change_color_cell_error(self, line, column, is_error):
        """
        Change the color of a cell to indicate an error.

        Args:
            line (int): The line of the cell.
            column (int): The column of the cell.
            is_error (bool): True if the cell is in error state, False otherwise.
        """
        cell = self.cells[(line, column)]
        cell.set_error(is_error) 

    def set_cell_borders(self, line, column, top, right, bottom, left):
        """
        Set the borders of a cell.

        Args:
            line (int): The line of the cell.
            column (int): The column of the cell.
            top (bool): True to make the top border bold.
            right (bool): True to make the right border bold.
            bottom (bool): True to make the bottom border bold.
            left (bool): True to make the left border bold.
        """
        cell = self.cells[(line, column)]
        cell.set_borders(top, right, bottom, left)