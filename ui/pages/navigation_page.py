"""Navigation page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class NavigationPage(QWidget):
    """Display navigation map and route guidance placeholders."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build placeholder navigation UI."""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Navigation"))
        layout.addWidget(QLabel("Map view placeholder"))
        layout.addStretch()
