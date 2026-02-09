"""Camera page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CameraPage(QWidget):
    """Display camera feed placeholders."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build placeholder camera widgets."""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Camera"))
        layout.addWidget(QLabel("Rear/Front camera feed placeholder"))
        layout.addStretch()
