from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator


class CellWidget(QLineEdit):
    def __init__(self, line, column):
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
        self.row = line
        self.column = column
        self.is_error = False
        
    
        self.bold_borders = {'top': "0.5px solid lightgray",
                             'right': "0.5px solid lightgray", 
                             'bottom': "0.5px solid lightgray", 
                             'left': "0.5px solid lightgray"} 
        
    def set_borders(self, top_bold, right_bold, bottom_bold, left_bold):
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