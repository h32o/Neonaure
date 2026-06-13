"""
Module of the grid widget.

This widget is the main widget of the game, it contains the grid of cells.
"""
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from .cell_widget import CellWidget

class GridWidget(QWidget):
    """
    A widget representing the grid of the game.

    Signals:
    signal_cell_changed (pyqtSignal): Emitted when a cell is changed.
    """
    signal_cell_changed = pyqtSignal(int, int, str)

    def __init__(self):
        """
        Initialize the grid widget and set up the grid layout.
        """
        super().__init__()
        
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cells = {}   

    def create_grid(self):
        """
        Create the grid of cells.
        """
        for line in range(8):
            for column in range(8):
                cell = CellWidget(line, column)
                cell.textChanged.connect(self.on_cell_changed)
                self.grid_layout.addWidget(cell, line, column)
                self.cells[(line, column)] = cell

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