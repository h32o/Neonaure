
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QMimeData, Signal as pyqtSignal, QSize
from PySide6.QtGui import QDrag, QPainter, QColor, QFont, QPen


class DraggableNumberTile(QLabel):
    """
    A single tile displaying a number (or 'X' for eraser) that can be
    dragged onto a CellWidget to set its value.
    """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self._text = text
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(56, 56)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        if text == "X":
            bg = "#2A2A35"
            fg = "#FF6B6B"
            border_color = "#FF6B6B"
        else:
            bg = "#2A2A35"
            fg = "#E0E0FF"
            border_color = "#5B5B8A"

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border: 2px solid {border_color};
                border-radius: 10px;
                font-size: 24px;
                font-weight: bold;
            }}
            QLabel:hover {{
                background-color: #383A59;
                border-color: #9D4EDD;
            }}
        """)

    def mousePressEvent(self, event):
        """Initiate a drag when the user clicks and moves the tile."""
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
          
            if self._text == "X":
                mime.setText("")
                mime.setData("application/x-suguru-erase", b"1")
            else:
                mime.setText(self._text)
                mime.setData("application/x-suguru-number", self._text.encode())
            drag.setMimeData(mime)

         
            pixmap = self.grab()
            drag.setPixmap(pixmap)
            drag.setHotSpot(pixmap.rect().center())

            drag.exec(Qt.DropAction.CopyAction)


class NumberPalette(QWidget):
    """
    Horizontal palette containing draggable tiles for numbers 1-5
    and an eraser tile.
    """

    signal_erase = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for number in range(1, 6):
            tile = DraggableNumberTile(str(number))
            layout.addWidget(tile)

    
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: #383A59;")
        sep.setFixedWidth(2)
        layout.addWidget(sep)

        eraser = DraggableNumberTile("X")
        eraser.setToolTip("Drag to erase a cell")
        layout.addWidget(eraser)