"""Application entry point for InterfaceKart."""

from PySide6.QtWidgets import QApplication

from services.mock_service import MockTelemetryService
from services.settings_repository import SettingsRepository
from services.theme_manager import ThemeManager
from ui.main_window import MainWindow


def main() -> int:
    """Create app, load settings, show window, and start telemetry."""
    app = QApplication([])

    settings_repo = SettingsRepository()
    settings = settings_repo.load_settings()
    theme_manager = ThemeManager(app)
    theme_manager.apply_theme(settings.theme_mode, settings.brightness)

    telemetry_service = MockTelemetryService()
    window = MainWindow(
        settings=settings,
        settings_repo=settings_repo,
        theme_manager=theme_manager,
        telemetry_service=telemetry_service,
    )
    window.showFullScreen()
    telemetry_service.start()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
