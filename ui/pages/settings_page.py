"""Settings page."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from domain.settings_model import AppSettings, ThemeMode


class SettingsPage(QWidget):
    """Settings form for theme, map-follow, and brightness."""

    save_requested = Signal(object)

    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._theme_toggle = QCheckBox("Night mode")
        self._follow_toggle = QCheckBox("Follow map")
        self._brightness = QSlider()
        self._brightness_value = QLabel("")
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        self._brightness.setOrientation(Qt.Horizontal)
        self._brightness.setMinimum(0)
        self._brightness.setMaximum(100)
        self._brightness.valueChanged.connect(self._sync_brightness_label)

        layout.addWidget(QLabel("Display & Driving Preferences"))
        layout.addWidget(self._theme_toggle)
        layout.addWidget(self._follow_toggle)
        row = QHBoxLayout()
        row.addWidget(QLabel("Brightness"))
        row.addWidget(self._brightness, 1)
        row.addWidget(self._brightness_value)
        layout.addLayout(row)

        save_btn = QPushButton("Save settings")
        save_btn.setMinimumHeight(56)
        save_btn.clicked.connect(self._emit_save)
        layout.addWidget(save_btn)
        layout.addStretch(1)

    def _load_values(self) -> None:
        self._theme_toggle.setChecked(self._settings.theme_mode == ThemeMode.NIGHT)
        self._follow_toggle.setChecked(self._settings.map_follow)
        self._brightness.setValue(self._settings.brightness)
        self._sync_brightness_label(self._settings.brightness)

    def _sync_brightness_label(self, value: int) -> None:
        self._brightness_value.setText(f"{value}%")

    def _emit_save(self) -> None:
        self._settings.theme_mode = ThemeMode.NIGHT if self._theme_toggle.isChecked() else ThemeMode.DAY
        self._settings.map_follow = self._follow_toggle.isChecked()
        self._settings.brightness = self._brightness.value()
        self.save_requested.emit(self._settings)
