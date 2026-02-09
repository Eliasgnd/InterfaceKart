"""Main window composition and telemetry binding."""

from __future__ import annotations

from datetime import datetime, timedelta

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from domain.settings_model import AppSettings, PageId
from domain.telemetry_model import ConnectivityState, TelemetryFrame
from services.alert_manager import AlertManager
from services.settings_repository import SettingsRepository
from services.telemetry_service import TelemetryService
from services.theme_manager import ThemeManager
from ui.pages.camera_page import CameraPage
from ui.pages.home_page import HomePage
from ui.pages.navigation_page import NavigationPage
from ui.pages.settings_page import SettingsPage
from ui.widgets.alert_banner import AlertBannerHost
from ui.widgets.bottom_nav_bar import BottomNavBar
from ui.widgets.top_status_bar import TopStatusBar


class MainWindow(QMainWindow):
    """Root fullscreen cockpit UI window."""

    def __init__(
        self,
        settings: AppSettings,
        settings_repo: SettingsRepository,
        theme_manager: ThemeManager,
        telemetry_service: TelemetryService,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("RootWindow")
        self.setWindowTitle("Electric Kart Console")
        self._settings = settings
        self._settings_repo = settings_repo
        self._theme_manager = theme_manager
        self._telemetry_service = telemetry_service
        self._alert_manager = AlertManager()
        self._last_frame_at = datetime.utcnow()

        self._stack = QStackedWidget()
        self._top_bar = TopStatusBar()
        self._banner_host = AlertBannerHost()
        self._bottom_nav = BottomNavBar()
        self._pages: dict[PageId, QWidget] = {}
        self._build_ui()
        self._connect_signals()

        self._disconnect_watchdog = QTimer(self)
        self._disconnect_watchdog.setInterval(1200)
        self._disconnect_watchdog.timeout.connect(self._check_link_health)
        self._disconnect_watchdog.start()

    def _build_ui(self) -> None:
        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        home_page = HomePage()
        nav_page = NavigationPage(self._settings.map_follow, self._settings.map_zoom)
        cam_page = CameraPage()
        settings_page = SettingsPage(self._settings)

        self._pages = {
            PageId.HOME: home_page,
            PageId.NAVIGATION: nav_page,
            PageId.CAMERA: cam_page,
            PageId.SETTINGS: settings_page,
        }
        for page in self._pages.values():
            self._stack.addWidget(page)

        root.addWidget(self._top_bar)
        root.addWidget(self._banner_host)
        root.addWidget(self._stack, 1)
        root.addWidget(self._bottom_nav)
        self.setCentralWidget(central)
        self.set_page(self._settings.default_page)

    def _connect_signals(self) -> None:
        self._bottom_nav.page_selected.connect(self.set_page)
        self._banner_host.alert_dismissed.connect(self._alert_manager.acknowledge)
        self._telemetry_service.telemetry_updated.connect(self._on_telemetry)

        home_page = self._pages[PageId.HOME]
        if isinstance(home_page, HomePage):
            home_page.go_to_page.connect(self.set_page)

        nav_page = self._pages[PageId.NAVIGATION]
        if isinstance(nav_page, NavigationPage):
            nav_page.follow_changed.connect(self._on_follow_changed)
            nav_page.zoom_changed.connect(self._on_zoom_changed)

        settings_page = self._pages[PageId.SETTINGS]
        if isinstance(settings_page, SettingsPage):
            settings_page.save_requested.connect(self._on_save_settings)

    def set_page(self, page_id: PageId) -> None:
        page = self._pages.get(page_id)
        if page is not None:
            self._stack.setCurrentWidget(page)

    def _on_follow_changed(self, value: bool) -> None:
        self._settings.map_follow = value

    def _on_zoom_changed(self, value: int) -> None:
        self._settings.map_zoom = value

    def _on_save_settings(self, settings: AppSettings) -> None:
        self._settings_repo.save_settings(settings)
        self._theme_manager.apply_theme(settings.theme_mode, settings.brightness)

    def _on_telemetry(self, frame: TelemetryFrame) -> None:
        self._last_frame_at = frame.timestamp
        self._top_bar.set_speed_text(f"{frame.speed_kmh:0.0f} km/h")
        self._top_bar.set_battery_percent(frame.battery_percent)
        self._top_bar.set_gps_state(frame.gps.fix_state)
        self._top_bar.set_connectivity(frame.connectivity)

        self._alert_manager.ingest(frame.alerts)
        self._banner_host.show_alert(self._alert_manager.get_banner_alert())

        if frame.reverse and self.current_page() != PageId.SETTINGS:
            self.set_page(PageId.CAMERA)

        page = self._stack.currentWidget()
        on_telemetry = getattr(page, "on_telemetry", None)
        if callable(on_telemetry):
            on_telemetry(frame)

    def current_page(self) -> PageId:
        current = self._stack.currentWidget()
        for page_id, widget in self._pages.items():
            if widget is current:
                return page_id
        return PageId.HOME

    def _check_link_health(self) -> None:
        if datetime.utcnow() - self._last_frame_at > timedelta(seconds=2):
            self._top_bar.set_connectivity(ConnectivityState.DISCONNECTED)
