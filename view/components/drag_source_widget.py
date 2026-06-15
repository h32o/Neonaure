from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

class DragSourceWidget(QWidget):
    """
    A widget containing the draggable cases (Case 1 to Case 5).
    Implements drag and drop source logic.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Initializes the layout and draggable buttons."""
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create 5 draggable case buttons/widgets
        for i in range(1, 6):
            case_button = QPushButton(f"Case {i}")
            case_button.setFixedSize(100, 80)
            case_button.setStyleSheet("""
                QPushButton {
                    background-color: #3A3A59;
                    color: white;
                    border-radius: 10px;
                    border: 2px solid #5C5CAE;
                    font-size: 16px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #4A4AA8;
                }
            """)
            case_button.mousePressEvent = self._make_draggable(case_button, i)
            layout.addWidget(case_button)

    def _make_draggable(self, widget, case_id):
        """
        Overwrites mousePressEvent for a specific widget to enable dragging.
        Returns the custom event handler function.
        """
        def make_drag_source(event):
            if event.button() == Qt.MouseButton.LeftButton:
                # Start drag operation
                mimeData = QMimeData()

                # Store the case ID (1-5) as the data being dragged
                mimeData.setText(str(case_id)) 
                
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                # Start drag operation at the widget's position
                drag.exec(Qt.DropAction.CopyAction)
        return make_drag_source

    def mousePressEvent(self, event):
        """
        Intercepts mouse press events to ensure all child widgets are draggable.
        This is a general handler for the container widget itself.
        """
        # We rely on setting the custom event handlers in setup_ui, 
        # but this method ensures the base class handles it if needed.
        super().mousePressEvent(event)

    def dragEnterEvent(self, event):
        """
        Handles when a potential drop target enters the widget area.
        We allow drops only if the MIME data contains a case ID (string).
        """
        if "text/plain" in event.mimeData().formats():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handles when an item is dropped onto the widget area.
        """
        pass
