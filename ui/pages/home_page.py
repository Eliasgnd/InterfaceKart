"""Drive dashboard page."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from domain.settings_model import PageId
from domain.telemetry_model import TelemetryFrame


class HomePage(QWidget):
    """Main drive dashboard with quick actions."""

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
        self._build_ui()

    def _build_ui(self) -> None:
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
