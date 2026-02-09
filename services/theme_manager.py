"""Theme application service for Qt widgets."""

from pathlib import Path

from PySide6.QtWidgets import QApplication

from domain.settings_model import ThemeMode


class ThemeManager:
    """Load and apply QSS stylesheets to the running application."""

    def __init__(self, application: QApplication) -> None:
        self._application = application

    def apply_theme(self, theme: ThemeMode) -> None:
        """Apply the selected theme stylesheet to the app instance."""
        stylesheet_name = "day.qss" if theme == ThemeMode.DAY else "night.qss"
        stylesheet_path = Path(__file__).resolve().parent.parent / "ui" / "styles" / stylesheet_name
        self._application.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))
