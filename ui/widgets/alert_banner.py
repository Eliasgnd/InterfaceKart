"""Alert banner widget for messages."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AlertBanner(QWidget):
    """Simple banner to display warning or informational messages."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._message_label = QLabel("No active alerts")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create layout for the alert banner."""
        layout = QVBoxLayout(self)
        layout.addWidget(self._message_label)

    def show_alert(self, message: str) -> None:
        """Set the current alert text."""
        self._message_label.setText(message)
