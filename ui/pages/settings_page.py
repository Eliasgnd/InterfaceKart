"""Settings page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    """Display user settings controls placeholders."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build settings UI placeholder components."""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings"))
        layout.addWidget(QLabel("Theme and telemetry preferences placeholder"))
        layout.addStretch()
