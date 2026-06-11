from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

class CellWidget(QLineEdit):
    def __init__(self, line, column):
        super().__init__()
        
        regex = QRegularExpression("^[1-5]$")
        validator = QRegularExpressionValidator(regex, self)
        self.setValidator(validator)
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(50, 50)   
        self.setStyleSheet("""
            background-color: white;
            border: 0.5px solid black;
            color: black;
            font-weight : bold;                  
        """)
        self.row = line
        self.column = column
        self.is_error = False
        self.bold_borders = {'top': "0.5px solid black",
                             'right': "0.5px solid black", 
                             'bottom': "0.5px solid black", 
                             'left': "0.5px solid black"} 
        
    def set_borders(self, top_bold, right_bold, bottom_bold, left_bold):
        if top_bold:
            self.bold_borders['top'] = "2px solid black"
        else : 
            self.bold_borders['top'] = "0.5px solid black"
        if right_bold:
            self.bold_borders['right'] = "2px solid black"  
        else :
            self.bold_borders['right'] = "0.5px solid black"
        if bottom_bold:
            self.bold_borders['bottom'] = "2px solid black"
        else :
            self.bold_borders['bottom'] = "0.5px solid black"
        if left_bold:
            self.bold_borders['left'] = "2px solid black"
        else :
            self.bold_borders['left'] = "0.5px solid black"
        self._apply_cell_style()


    def _apply_cell_style(self):
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
        font-weight : bold;
        """)

    def set_value(self, value):
        self.setText(str(value))
        self.setReadOnly(True)
        self.is_error = False
        self._apply_cell_style()

    def set_error(self, is_error):
        if not self.isReadOnly():
            self.is_error = is_error
            self._apply_cell_style()

    def clear_cell(self):
        self.clear()
        self.setReadOnly(False)
        self.is_error = False
        self._apply_cell_style()