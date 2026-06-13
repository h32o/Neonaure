from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
import os

class GridThumbnail(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, json_path: str, label: str, parent=None):
        super().__init__(parent)
        self._path = json_path
        self.setFixedSize(150, 170)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Chercher le PNG au même endroit que le JSON
        png_path = os.path.splitext(json_path)[0] + ".png"

        img_label = QLabel(self)
        img_label.setFixedSize(150, 135)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if os.path.exists(png_path):
            pixmap = QPixmap(png_path).scaled(
                148, 133,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            img_label.setPixmap(pixmap)
        else:
            img_label.setText("No preview")
            img_label.setStyleSheet("color: grey; font-size: 10px;")

        txt_label = QLabel(label, self)
        txt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt_label.setStyleSheet("color: #E0E0FF; font-size: 11px; background: transparent;")
        txt_label.setGeometry(0, 138, 150, 30)

    def mousePressEvent(self, event):
        self.clicked.emit(self._path)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #2A2A3A; border-radius: 6px;")

    def leaveEvent(self, event):
        self.setStyleSheet("")