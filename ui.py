"""Interface graphique regroupée dans un seul fichier (version débutant)."""

from __future__ import annotations

from datetime import datetime, timedelta

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from models import AppSettings, ConnectivityState, PageId, TelemetryFrame, ThemeMode
from services import AlertManager, SettingsRepository, TelemetryService, ThemeManager


class TopStatusBar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TopStatusBar")
        self._speed_label = QLabel("0 km/h")
        self._battery_label = QLabel("Battery: --%")
        self._gps_label = QLabel("GPS: NO FIX")
        self._link_label = QLabel("LINK: DISCONNECTED")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(24)
        for label in [self._speed_label, self._battery_label, self._gps_label, self._link_label]:
            layout.addWidget(label)
        layout.addStretch(1)

    def set_speed_text(self, speed_text: str) -> None:
        self._speed_label.setText(speed_text)

    def set_battery_percent(self, battery_percent: int) -> None:
        self._battery_label.setText(f"Battery: {battery_percent}%")

    def set_gps_state(self, gps_state) -> None:
        self._gps_label.setText(f"GPS: {gps_state.value.replace('_', ' ').upper()}")

    def set_connectivity(self, state: ConnectivityState) -> None:
        self._link_label.setText(f"LINK: {state.value.upper()}")
        self._link_label.setProperty("linkState", state.value)
        self.style().unpolish(self._link_label)
        self.style().polish(self._link_label)


class BottomNavBar(QWidget):
    page_selected = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("BottomNavBar")
        self._buttons: dict[PageId, QPushButton] = {}
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        self._add_button(layout, "🏠 Home", PageId.HOME)
        self._add_button(layout, "🗺 Navigation", PageId.NAVIGATION)
        self._add_button(layout, "📷 Camera", PageId.CAMERA)
        self._add_button(layout, "⚙ Settings", PageId.SETTINGS)
        self.set_active_page(PageId.HOME)

    def _add_button(self, layout: QHBoxLayout, text: str, page: PageId) -> None:
        button = QPushButton(text)
        button.setObjectName("NavButton")
        button.setMinimumHeight(64)
        button.clicked.connect(lambda: self._on_button_clicked(page))
        self._buttons[page] = button
        layout.addWidget(button)

    def _on_button_clicked(self, page: PageId) -> None:
        self.set_active_page(page)
        self.page_selected.emit(page)

    def set_active_page(self, page: PageId) -> None:
        for page_id, button in self._buttons.items():
            button.setProperty("active", page_id == page)
            self.style().unpolish(button)
            self.style().polish(button)


class AlertBanner(QWidget):
    dismissed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._alert = None
        self.setObjectName("AlertBanner")
        self._message = QLabel("")
        self._dismiss_btn = QPushButton("Dismiss")
        self._dismiss_btn.clicked.connect(self._emit_dismiss)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(self._message, 1)
        layout.addWidget(self._dismiss_btn)

    def set_alert(self, alert) -> None:
        self._alert = alert
        self._message.setText(alert.message)
        self._dismiss_btn.setVisible(alert.ack_required)
        self.setProperty("alertLevel", alert.level.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def _emit_dismiss(self) -> None:
        if self._alert is not None:
            self.dismissed.emit(self._alert.alert_id)


class AlertBannerHost(QWidget):
    alert_dismissed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._banner = AlertBanner()
        self._banner.dismissed.connect(self.alert_dismissed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.addWidget(self._banner)
        self.hide()

    def show_alert(self, alert) -> None:
        if alert is None:
            self.hide()
            return
        self._banner.set_alert(alert)
        self.show()


class HomePage(QWidget):
    go_to_page = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._speed = QLabel("0")
        self._unit = QLabel("km/h")
        self._battery = QLabel("100%")
        self._gps = QLabel("GPS: --")
        self._reverse = QLabel("OFF")
        self._heading = QLabel("--°")
        self._power = QLabel("0 kW")

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(12)

        hero = QFrame()
        hero.setObjectName("HeroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(18, 14, 18, 14)

        speed_row = QHBoxLayout()
        speed_row.addWidget(self._speed)
        self._speed.setObjectName("HeroSpeed")
        self._unit.setObjectName("HeroSpeedUnit")
        speed_row.addWidget(self._unit, alignment=Qt.AlignBottom)
        speed_row.addStretch(1)
        hero_layout.addLayout(speed_row)
        hero_layout.addWidget(QLabel("Live speed"), alignment=Qt.AlignLeft)
        root.addWidget(hero)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(self._card("Battery", self._battery), 0, 0)
        grid.addWidget(self._card("GPS fix", self._gps), 0, 1)
        grid.addWidget(self._card("Reverse", self._reverse), 1, 0)
        grid.addWidget(self._card("Heading", self._heading), 1, 1)
        grid.addWidget(self._card("Power", self._power), 2, 0, 1, 2)
        root.addLayout(grid)

        actions = QHBoxLayout()
        nav_btn = QPushButton("Open Navigation")
        cam_btn = QPushButton("Open Camera")
        for btn in [nav_btn, cam_btn]:
            btn.setMinimumHeight(56)
            btn.setObjectName("PrimaryButton")
            actions.addWidget(btn)
        nav_btn.clicked.connect(lambda: self.go_to_page.emit(PageId.NAVIGATION))
        cam_btn.clicked.connect(lambda: self.go_to_page.emit(PageId.CAMERA))
        root.addLayout(actions)

    def _card(self, title: str, value_label: QLabel) -> QGroupBox:
        box = QGroupBox(title)
        box.setObjectName("PanelCard")
        layout = QVBoxLayout(box)
        value_label.setObjectName("MetricValue")
        layout.addWidget(value_label)
        return box

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._speed.setText(f"{frame.speed_kmh:0.0f}")
        self._battery.setText(f"{frame.battery_percent}%")
        self._gps.setText(frame.gps.fix_state.value.replace("_", " ").upper())
        self._reverse.setText("ON" if frame.reverse else "OFF")
        self._heading.setText(f"{frame.gps.heading_deg:.0f}°")
        self._power.setText(f"{frame.speed_kmh * 0.8:0.1f} kW")


class NavigationPage(QWidget):
    follow_changed = Signal(bool)
    zoom_changed = Signal(int)

    def __init__(self, map_follow: bool, map_zoom: int, parent=None) -> None:
        super().__init__(parent)
        self._follow = map_follow
        self._zoom = map_zoom
        self._latlon = QLabel("Lat/Lon: --")
        self._heading = QLabel("Heading: --")
        self._fix = QLabel("Fix: --")
        self._follow_button = QPushButton("")
        self._zoom_label = QLabel("")

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(12)

        map_placeholder = QFrame()
        map_placeholder.setObjectName("MapPlaceholder")
        map_layout = QVBoxLayout(map_placeholder)
        map_layout.addStretch(1)
        map_layout.addWidget(QLabel("Map view"), alignment=Qt.AlignHCenter)
        map_layout.addWidget(QLabel("OSM/QtLocation integration ready"), alignment=Qt.AlignHCenter)
        map_layout.addStretch(1)

        info_panel = QFrame()
        info_panel.setObjectName("InfoCard")
        info_layout = QGridLayout(info_panel)
        info_layout.addWidget(self._latlon, 0, 0)
        info_layout.addWidget(self._heading, 0, 1)
        info_layout.addWidget(self._fix, 1, 0)
        info_layout.addWidget(self._zoom_label, 1, 1)

        controls = QHBoxLayout()
        zoom_in = QPushButton("+")
        zoom_out = QPushButton("-")
        zoom_in.setObjectName("RoundControl")
        zoom_out.setObjectName("RoundControl")
        zoom_in.clicked.connect(lambda: self._set_zoom(self._zoom + 1))
        zoom_out.clicked.connect(lambda: self._set_zoom(self._zoom - 1))
        self._follow_button.clicked.connect(self._toggle_follow)
        controls.addWidget(self._follow_button)
        controls.addStretch(1)
        controls.addWidget(QLabel("Zoom"))
        controls.addWidget(zoom_out)
        controls.addWidget(zoom_in)

        root.addWidget(map_placeholder, 1)
        root.addWidget(info_panel)
        root.addLayout(controls)
        self._refresh_controls()

    def _toggle_follow(self) -> None:
        self._follow = not self._follow
        self._refresh_controls()
        self.follow_changed.emit(self._follow)

    def _set_zoom(self, value: int) -> None:
        self._zoom = max(1, min(20, value))
        self._refresh_controls()
        self.zoom_changed.emit(self._zoom)

    def _refresh_controls(self) -> None:
        self._follow_button.setText("Follow kart: ON" if self._follow else "Follow kart: OFF")
        self._zoom_label.setText(f"Zoom: {self._zoom}")

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._latlon.setText(f"Lat/Lon: {frame.gps.latitude:.5f}, {frame.gps.longitude:.5f}")
        self._heading.setText(f"Heading: {frame.gps.heading_deg:.0f}°")
        self._fix.setText(f"Fix: {frame.gps.fix_state.value.replace('_', ' ').upper()}")


class CameraPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._mode = QLabel("Mode: Rear")
        self._reverse = QLabel("Reverse engaged: NO")

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(12)

        feeds = QGridLayout()
        feeds.addWidget(self._camera_tile("Rear camera"), 0, 0, 2, 2)
        feeds.addWidget(self._camera_tile("Left side"), 0, 2)
        feeds.addWidget(self._camera_tile("Right side"), 1, 2)
        root.addLayout(feeds, 1)

        status = QHBoxLayout()
        status.addWidget(self._mode)
        status.addStretch(1)
        status.addWidget(self._reverse)
        root.addLayout(status)

        buttons = QHBoxLayout()
        for mode in ["Rear", "Front", "Mosaic", "Bird-eye"]:
            btn = QPushButton(mode)
            btn.clicked.connect(lambda _=False, m=mode: self._mode.setText(f"Mode: {m}"))
            buttons.addWidget(btn)
        root.addLayout(buttons)

    def _camera_tile(self, text: str) -> QFrame:
        tile = QFrame()
        tile.setObjectName("CameraPlaceholder")
        layout = QVBoxLayout(tile)
        layout.addStretch(1)
        layout.addWidget(QLabel(text))
        layout.addStretch(1)
        return tile

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._reverse.setText("Reverse engaged" if frame.reverse else "Reverse engaged: NO")


class SettingsPage(QWidget):
    save_requested = Signal(object)

    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._theme_toggle = QCheckBox("Night mode")
        self._follow_toggle = QCheckBox("Follow map")
        self._brightness = QSlider()
        self._brightness_value = QLabel("")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        card = QFrame()
        card.setObjectName("InfoCard")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(QLabel("Display & Driving Preferences"))
        card_layout.addWidget(self._theme_toggle)
        card_layout.addWidget(self._follow_toggle)

        self._brightness.setOrientation(Qt.Horizontal)
        self._brightness.setMinimum(0)
        self._brightness.setMaximum(100)
        self._brightness.valueChanged.connect(self._sync_brightness_label)

        row = QHBoxLayout()
        row.addWidget(QLabel("Brightness"))
        row.addWidget(self._brightness, 1)
        row.addWidget(self._brightness_value)
        card_layout.addLayout(row)

        layout.addWidget(card)

        save_btn = QPushButton("Save settings")
        save_btn.setMinimumHeight(56)
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self._emit_save)
        layout.addWidget(save_btn)
        layout.addStretch(1)

        self._load_values()

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


class MainWindow(QMainWindow):
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

        home_page = HomePage()
        nav_page = NavigationPage(self._settings.map_follow, self._settings.map_zoom)
        cam_page = CameraPage()
        settings_page = SettingsPage(self._settings)

        self._pages: dict[PageId, QWidget] = {
            PageId.HOME: home_page,
            PageId.NAVIGATION: nav_page,
            PageId.CAMERA: cam_page,
            PageId.SETTINGS: settings_page,
        }

        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)
        for page in self._pages.values():
            self._stack.addWidget(page)
        root.addWidget(self._top_bar)
        root.addWidget(self._banner_host)
        root.addWidget(self._stack, 1)
        root.addWidget(self._bottom_nav)
        self.setCentralWidget(central)

        self._bottom_nav.page_selected.connect(self.set_page)
        self._banner_host.alert_dismissed.connect(self._alert_manager.acknowledge)
        self._telemetry_service.telemetry_updated.connect(self._on_telemetry)
        home_page.go_to_page.connect(self.set_page)
        nav_page.follow_changed.connect(self._on_follow_changed)
        nav_page.zoom_changed.connect(self._on_zoom_changed)
        settings_page.save_requested.connect(self._on_save_settings)

        self.set_page(self._settings.default_page)

        self._disconnect_watchdog = QTimer(self)
        self._disconnect_watchdog.setInterval(1200)
        self._disconnect_watchdog.timeout.connect(self._check_link_health)
        self._disconnect_watchdog.start()

    def set_page(self, page_id: PageId) -> None:
        page = self._pages.get(page_id)
        if page is not None:
            self._stack.setCurrentWidget(page)
            self._bottom_nav.set_active_page(page_id)

    def current_page(self) -> PageId:
        current = self._stack.currentWidget()
        for page_id, widget in self._pages.items():
            if widget is current:
                return page_id
        return PageId.HOME

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

    def _check_link_health(self) -> None:
        if datetime.utcnow() - self._last_frame_at > timedelta(seconds=2):
            self._top_bar.set_connectivity(ConnectivityState.DISCONNECTED)
