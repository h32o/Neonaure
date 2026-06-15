from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QHBoxLayout, QLabel,QDialog,QFormLayout,QDialogButtonBox,QDoubleSpinBox,QSpinBox,QFileDialog, QGraphicsOpacityEffect
from PySide6.QtCore import Signal as pyqtSignal, QTimer, Qt, QPropertyAnimation
from PySide6.QtGui import QKeySequence,QPixmap,QPainter,QColor

class LoadingOverlay(QWidget):
    """Semi-transparent overlay with a message and pulsing dots."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(18, 18, 26, 210);")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel("")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("""
            color: #E0E0FF;
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 2px;
        """)
        layout.addWidget(self._label)

        self._dots_label = QLabel("")
        self._dots_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._dots_label.setStyleSheet("""
            color: #9D4EDD;
            font-size: 36px;
            font-weight: bold;
        """)
        layout.addWidget(self._dots_label)

        self._dot_count = 0
        self._dot_timer = QTimer(self)
        self._dot_timer.timeout.connect(self._tick_dots)
        self.hide()

    def show_with_message(self, message: str):
        self._label.setText(message)
        self._dot_count = 0
        self._dots_label.setText("")
        self._dot_timer.start(400)
        self.raise_()
        self.show()

    def hide_overlay(self):
        self._dot_timer.stop()
        self.hide()

    def _tick_dots(self):
        self._dot_count = (self._dot_count + 1) % 4
        self._dots_label.setText("\u2022  " * self._dot_count)

    def resizeEvent(self, event):
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().resizeEvent(event)