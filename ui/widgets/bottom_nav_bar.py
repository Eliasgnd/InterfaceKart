"""Bottom navigation bar widget."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QWidget

from ui.widgets.icon_button import IconButton


class BottomNavBar(QWidget):
    """Provide page navigation buttons."""

    page_requested = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Build navigation button row."""
        self._home_button = IconButton("Home")
        self._navigation_button = IconButton("Navigation")
        self._camera_button = IconButton("Camera")
        self._settings_button = IconButton("Settings")

        layout = QHBoxLayout(self)
        layout.addWidget(self._home_button)
        layout.addWidget(self._navigation_button)
        layout.addWidget(self._camera_button)
        layout.addWidget(self._settings_button)

    def _connect_signals(self) -> None:
        """Forward button clicks as page request signals."""
        self._home_button.clicked.connect(lambda: self.page_requested.emit("home"))
        self._navigation_button.clicked.connect(lambda: self.page_requested.emit("navigation"))
        self._camera_button.clicked.connect(lambda: self.page_requested.emit("camera"))
        self._settings_button.clicked.connect(lambda: self.page_requested.emit("settings"))
