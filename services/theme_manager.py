"""Theme stylesheet application utility."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

from domain.settings_model import ThemeMode


class ThemeManager:
    """Apply day/night QSS and coarse brightness filter."""

    def __init__(self, application: QApplication) -> None:
        self._application = application

    def apply_theme(self, theme_mode: ThemeMode, brightness: int) -> None:
        """Apply selected stylesheet and global brightness tint."""
        stylesheet_name = "day.qss" if theme_mode == ThemeMode.DAY else "night.qss"
        stylesheet_path = Path(__file__).resolve().parent.parent / "ui" / "styles" / stylesheet_name
        base_qss = stylesheet_path.read_text(encoding="utf-8")
        clamped = max(0, min(100, brightness))
        overlay_opacity = (100 - clamped) / 130.0
        brightness_qss = (
            "QWidget#RootWindow {"
            f"background-color: rgba(0, 0, 0, {overlay_opacity:.2f});"
            "}"
        )
        self._application.setStyleSheet(base_qss + "\n" + brightness_qss)
