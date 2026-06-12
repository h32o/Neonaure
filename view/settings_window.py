from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QPushButton, QCheckBox, QLabel, QLineEdit, QSpinBox
from PyQt6.QtCore import pyqtSignal, Qt

class SettingsWindow(QWidget):
    signal_load = pyqtSignal()
    signal_save = pyqtSignal()
    signal_reset = pyqtSignal()
    signal_generate = pyqtSignal()
    signal_background_change = pyqtSignal()
    signal_quit = pyqtSignal()
    signal_toggle_timer = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.menu_list = QListWidget()
        self.menu_list.setFixedWidth(180)
        self.menu_list.addItem("General")
        self.menu_list.addItem("Display")
        self.menu_list.addItem("Rules of the Game")
        
        self.menu_list.setStyleSheet("""
            QListWidget {
                color: white;
                background-color: #2f3136;
                border: none;
                padding-left: 0px;  
                outline: none;      
            }
            QListWidget::item {
                padding: 12px 15px; 
            }
            QListWidget::item:selected {
                background-color: #40444b; 
            }
        """)
        
        self.main_layout.addWidget(self.menu_list)
        
        self.content = QStackedWidget()
        self.content.setStyleSheet("background-color: #36393f; color: white;")
        self.main_layout.addWidget(self.content)
        
        self.page_general = QWidget()
        layout_general = QVBoxLayout(self.page_general)
        
        self.btn_load = QPushButton("Load Grid")
        self.btn_save = QPushButton("Save Grid")
        self.btn_reset = QPushButton("Reset Grid")
        self.btn_generate = QPushButton("Generate Grid")
        self.btn_quit = QPushButton("Quit Application")
        
        button_style = """
            QPushButton {
                background-color: #40444b; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 5px;
                text-align: left; 
            }
            QPushButton:hover {
                background-color: black;
            }
        """
        self.btn_load.setStyleSheet(button_style)
        self.btn_save.setStyleSheet(button_style)
        self.btn_reset.setStyleSheet(button_style)
        self.btn_generate.setStyleSheet(button_style)
        self.btn_quit.setStyleSheet(button_style)
        
        layout_general.addWidget(QLabel("General Settings"))
        layout_general.addWidget(self.btn_load)
        layout_general.addWidget(self.btn_save)
        layout_general.addWidget(self.btn_reset)
        layout_general.addWidget(self.btn_generate)
        layout_general.addWidget(self.btn_quit)
        layout_general.addStretch()
     
        self.page_display = QWidget()
        layout_display = QVBoxLayout(self.page_display)
        
        layout_display.addWidget(QLabel("Display Settings"))
        
        self.checkbox_timer = QCheckBox("Show timer")
        self.checkbox_timer.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        self.checkbox_timer.setChecked(False)
        layout_display.addWidget(self.checkbox_timer)
        
        self.background_change = QPushButton("Change Backgound")
        self.background_change.setStyleSheet(button_style)
        layout_display.addWidget(self.background_change)
        
        layout_display.addStretch()
        
        self.page_rules = QWidget()
        layout_rules = QVBoxLayout(self.page_rules)
        
        rules_text = QLabel(
            "Welcome to the Néonaure!\n"
            "Here are the rules for solving the grid:\n\n"
            "• one number per cell\n"
            "• a number must be surrounded by different numbers (including diagonally)\n"
            "• a pattern of N cells (marked with bold lines) must contain all numbers from 1 to N\n"
        )
        rules_text.setWordWrap(True)
        
        layout_rules.addWidget(QLabel("Rules of the Game"))
        layout_rules.addWidget(rules_text)
        layout_rules.addStretch()
        
        self.content.addWidget(self.page_general)
        self.content.addWidget(self.page_display)
        self.content.addWidget(self.page_rules)
        
        self.menu_list.currentRowChanged.connect(self.content.setCurrentIndex)
        
        self.btn_load.clicked.connect(self.signal_load.emit)
        self.btn_save.clicked.connect(self.signal_save.emit)
        self.btn_reset.clicked.connect(self.signal_reset.emit)
        self.btn_generate.clicked.connect(self.signal_generate.emit)
        self.btn_quit.clicked.connect(self.signal_quit.emit)
        self.checkbox_timer.toggled.connect(self.signal_toggle_timer.emit)
        self.background_change.clicked.connect(self.signal_background_change.emit)