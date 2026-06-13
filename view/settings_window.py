from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QPushButton, QCheckBox, QLabel, QLineEdit, QSpinBox
from PyQt6.QtCore import pyqtSignal, Qt

class SettingsWindow(QWidget):
    signal_load = pyqtSignal()
    signal_save = pyqtSignal()
    signal_reset = pyqtSignal()
    signal_generate = pyqtSignal()
    signal_quit = pyqtSignal()
    signal_toggle_timer = pyqtSignal(bool)
    signal_pseudo_changed = pyqtSignal(str) 
    
    def __init__(self):
        super().__init__()
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.menu_list = QListWidget()
        self.menu_list.setFixedWidth(180)
        self.menu_list.addItem("General")
        self.menu_list.addItem("Display")
        self.menu_list.addItem("Rules of the Game")
        self.menu_list.addItem("Account") 
        
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
        self.btn_load.setShortcut("Ctrl+L")
        self.btn_save = QPushButton("Save Grid")
        self.btn_save.setShortcut("Ctrl+S")
        self.btn_reset = QPushButton("Reset Grid")
        self.btn_reset.setShortcut("Ctrl+R")
        self.btn_generate = QPushButton("Generate Grid")
        self.btn_generate.setShortcut("Ctrl+G")
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

  
        self.page_account = QWidget()
        layout_account = QVBoxLayout(self.page_account)
        
        layout_account.addWidget(QLabel("Account Settings"))
        
        layout_account.addWidget(QLabel("Pseudonym:"))
        self.pseudo_input = QLineEdit()
        self.pseudo_input.setPlaceholderText("Enter your pseudo...")
        self.pseudo_input.setStyleSheet("""
            QLineEdit {
                background-color: #40444b; 
                color: white; 
                border: 1px solid #383A59; 
                border-radius: 5px; 
                padding: 8px;
            }
        """)
        layout_account.addWidget(self.pseudo_input)
        
        self.btn_save_pseudo = QPushButton("Save Pseudonym")
        self.btn_save_pseudo.setStyleSheet(button_style)
        self.btn_save_pseudo.clicked.connect(self.save_pseudo)
        layout_account.addWidget(self.btn_save_pseudo)
        
        layout_account.addStretch()
    
        self.content.addWidget(self.page_general)   
        self.content.addWidget(self.page_display)   
        self.content.addWidget(self.page_rules)    
        self.content.addWidget(self.page_account)   
        
        self.menu_list.currentRowChanged.connect(self.content.setCurrentIndex)
        
        self.btn_load.clicked.connect(self.signal_load.emit)
        self.btn_save.clicked.connect(self.signal_save.emit)
        self.btn_reset.clicked.connect(self.signal_reset.emit)
        self.btn_generate.clicked.connect(self.signal_generate.emit)
        self.btn_quit.clicked.connect(self.signal_quit.emit)
        self.checkbox_timer.toggled.connect(self.signal_toggle_timer.emit)

    def save_pseudo(self):
        pseudo = self.pseudo_input.text()
        if pseudo:
            self.signal_pseudo_changed.emit(pseudo)