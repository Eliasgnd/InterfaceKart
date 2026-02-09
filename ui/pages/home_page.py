"""Home dashboard page."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.widgets.alert_banner import AlertBanner


class HomePage(QWidget):
    """Default landing page for high-level telemetry summaries."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._alert_banner = AlertBanner()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create home page content widgets."""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Home"))
        layout.addWidget(self._alert_banner)
        layout.addStretch()
