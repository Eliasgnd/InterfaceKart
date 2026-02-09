"""Top-level application controller."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from app.router import AppRouter
from services.mock_service import MockTelemetryService
from services.settings_repository import SettingsRepository
from services.theme_manager import ThemeManager


class ApplicationController:
    """Wire services, router, and UI lifecycle for the application."""

    def __init__(self, application: QApplication) -> None:
        self._application = application
        self._settings_repository = SettingsRepository()
        self._theme_manager = ThemeManager(self._application)
        self._telemetry_service = MockTelemetryService()
        self._router = AppRouter()

    def start(self) -> None:
        """Initialize services, apply settings, and show the main window."""
        settings = self._settings_repository.load_settings()
        self._theme_manager.apply_theme(settings.theme)
        self._telemetry_service.start_stream()
        self._router.show_main_window()

    def shutdown(self) -> None:
        """Stop background work before application exit."""
        self._telemetry_service.stop_stream()
