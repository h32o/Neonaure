from PyQt6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QIcon
from view.components.grid_thumbnail import GridThumbnail
import os, glob

class GridCarousel(QWidget):
    signal_grid_selected = pyqtSignal(str)

    PANEL_HEIGHT = 220

    def __init__(self, grids_folder: str, parent=None):
        super().__init__(parent)
        self._open = False
        self.setFixedHeight(self.PANEL_HEIGHT + 50)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.toggle_btn = QPushButton("▼  Grilles")
        self.toggle_btn.setFixedSize(140, 40)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #2A2A35;
                color: #E0E0FF;
                border: 1px solid #383A59;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #383A59; }
        """)
        self.toggle_btn.clicked.connect(self.toggle)
        btn_row.addWidget(self.toggle_btn)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

        self.panel = QWidget()
        self.panel.setFixedHeight(0)
        self.panel.setStyleSheet("background-color: #1E1E2E; border-top: 1px solid #383A59;")
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none;")

        container = QWidget()
        self._thumbs_layout = QHBoxLayout(container)
        self._thumbs_layout.setSpacing(15)
        self._thumbs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._load_thumbnails(grids_folder)

        scroll.setWidget(container)
        panel_layout.addWidget(scroll)
        main_layout.addWidget(self.panel)

        self._anim = QPropertyAnimation(self.panel, b"maximumHeight")
        self._anim.setDuration(300)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def _load_thumbnails(self, folder: str):
        json_files = sorted(glob.glob(os.path.join(folder, "*.json")))
        for path in json_files:
            name = os.path.splitext(os.path.basename(path))[0]
            thumb = GridThumbnail(path, name)
            thumb.clicked.connect(self._on_grid_selected)
            self._thumbs_layout.addWidget(thumb)

    def _on_grid_selected(self, path: str):
        self.signal_grid_selected.emit(path)
        self.close_panel() 

    def toggle(self):
        if self._open:
            self.close_panel()
        else:
            self.open_panel()

    def open_panel(self):
        self._open = True
        self.toggle_btn.setText("▲  Grilles")
        self._anim.setStartValue(self.panel.height())
        self._anim.setEndValue(self.PANEL_HEIGHT)
        self._anim.start()

    def close_panel(self):
        self._open = False
        self.toggle_btn.setText("▼  Grilles")
        self._anim.setStartValue(self.panel.height())
        self._anim.setEndValue(0)
        self._anim.start()