"""
Module for the cell widget.

This widget is a line edit that allows the user to enter a number in the cell.
"""
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


class CellWidget(QLineEdit):
    """
    A widget representing a cell in the grid.

    It derives from QLineEdit and allows the user to enter a number in the cell between 1 and 5.
    It also allows the user to set the borders of the cell.
    """
    def __init__(self, line, column):
        """
        Initialise the cell widget,setup input validation and style.

        Args:
            line (int): The line of the cell.
            column (int): The column of the cell.
        """
        super().__init__()
        
        regex = QRegularExpression("^[1-5]$")
        validator = QRegularExpressionValidator(regex, self)
        self.setValidator(validator)
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            background-color: white;
            border: none; 
            padding: 0px;
            color: black;
            font-weight : bold;          
        """)

        self.row : int  = line
        self.column : int = column
        self.is_error : bool = False
        
    
        # Borders 
        self.bold_borders : dict = {'top': "0.5px solid lightgray",
                             'right': "0.5px solid lightgray", 
                             'bottom': "0.5px solid lightgray", 
                             'left': "0.5px solid lightgray"} 

        # Add Drag and drop support to cell 
        self.setAcceptDrops(True)

        
    def set_borders(self, top_bold, right_bold, bottom_bold, left_bold):
        """
        Update the borders of the cell widget.

        Args:
            top_bold (bool): True to make the top border bold.
            right_bold (bool): True to make the right border bold.
            bottom_bold (bool): True to make the bottom border bold.
            left_bold (bool): True to make the left border bold.
        """
        BOLD_BORDER = "1.5px solid black"
        NORMAL_BORDER = "0.5px solid #474747"

        if top_bold:
            self.bold_borders['top'] = BOLD_BORDER
        else : 
            self.bold_borders['top'] = NORMAL_BORDER
        
        if right_bold:
            self.bold_borders['right'] = BOLD_BORDER 
        else :
            self.bold_borders['right'] = NORMAL_BORDER
            
        if bottom_bold:
            self.bold_borders['bottom'] = BOLD_BORDER
        else :
            self.bold_borders['bottom'] = NORMAL_BORDER
            
        if left_bold:
            self.bold_borders['left'] = BOLD_BORDER
        else :
            self.bold_borders['left'] = NORMAL_BORDER
            
        self._apply_cell_style()


    def _apply_cell_style(self):
        """
        Apply the style to the cell widget based on its state(read-only, error, or default).
        """
        if self.isReadOnly():
            background_color = "#ADADAD"
        elif self.is_error:
            background_color = "#FFCCCC" 
        else:
            background_color = "white"
        
    
        self.setStyleSheet(f"""
            background-color: {background_color};
            border-top: {self.bold_borders['top']};
            border-right: {self.bold_borders['right']}; 
            border-bottom: {self.bold_borders['bottom']};
            border-left: {self.bold_borders['left']};
            color: black;
            font-weight: bold;
            margin: -0.25px; 
        """)

    def set_value(self, value):
        """
        Set the value of the cell widget.

        Args:
            value (int): The value of the cell widget.
        """
        self.setText(str(value))
        self.setReadOnly(True)
        self.is_error = False
        self._apply_cell_style()


    def set_error(self, is_error):
        """
        Set the error state of the cell widget.

        Args:
            is_error (bool): True if the cell widget is in error state, False otherwise.
        """
        if not self.isReadOnly():
            self.is_error = is_error
            self._apply_cell_style()


    def clear_cell(self):
        """
        Clear the cell widget by removing its value, enabling editing, and resetting the error state.
        """
        self.clear()
        self.setReadOnly(False)
        self.is_error = False
        self._apply_cell_style()

    
    def dropEvent(self, event):
        """Handle the drop: set the number or erase the cell."""
        mime = event.mimeData()
        if self.isReadOnly():
            return

        if mime.hasFormat("application/x-suguru-number"):
            number = mime.data("application/x-suguru-number").data().decode()
            self.setText(number)
        elif mime.hasFormat("application/x-suguru-erase"):
            self.setText("")