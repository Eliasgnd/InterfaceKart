"""Top status bar widget."""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class TopStatusBar(QWidget):
    """Display connectivity and high-level status text."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._status_label = QLabel("Status: Ready")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build bar layout."""
        layout = QHBoxLayout(self)
        layout.addWidget(self._status_label)
        layout.addStretch()

    def update_status(self, message: str) -> None:
        """Update the status text shown to the user."""
        self._status_label.setText(f"Status: {message}")
