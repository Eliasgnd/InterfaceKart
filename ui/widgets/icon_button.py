"""Icon-aware push button widget."""

from PySide6.QtWidgets import QPushButton


class IconButton(QPushButton):
    """Button wrapper for future icon and action enhancements."""

    def __init__(self, label: str, parent=None) -> None:
        super().__init__(label, parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Apply base visual defaults for icon buttons."""
        self.setMinimumHeight(32)
