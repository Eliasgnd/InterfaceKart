"""Drive dashboard page."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QPushButton, QVBoxLayout, QWidget

from domain.settings_model import PageId
from domain.telemetry_model import TelemetryFrame


class HomePage(QWidget):
    """Main drive dashboard with quick actions."""

    go_to_page = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._speed = QLabel("0 km/h")
        self._battery = QLabel("100%")
        self._gps = QLabel("GPS: --")
        self._reverse = QLabel("Reverse: OFF")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        self._speed.setObjectName("HeroSpeed")
        root.addWidget(self._speed)

        grid = QGridLayout()
        grid.addWidget(self._card("Battery", self._battery), 0, 0)
        grid.addWidget(self._card("GPS", self._gps), 0, 1)
        grid.addWidget(self._card("Reverse", self._reverse), 1, 0)
        root.addLayout(grid)

        nav_btn = QPushButton("Go to Navigation")
        cam_btn = QPushButton("Go to Camera")
        nav_btn.setMinimumHeight(56)
        cam_btn.setMinimumHeight(56)
        nav_btn.clicked.connect(lambda: self.go_to_page.emit(PageId.NAVIGATION))
        cam_btn.clicked.connect(lambda: self.go_to_page.emit(PageId.CAMERA))
        root.addWidget(nav_btn)
        root.addWidget(cam_btn)
        root.addStretch(1)

    def _card(self, title: str, value_label: QLabel) -> QGroupBox:
        box = QGroupBox(title)
        box.setObjectName("PanelCard")
        layout = QVBoxLayout(box)
        layout.addWidget(value_label)
        return box

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._speed.setText(f"{frame.speed_kmh:0.0f} km/h")
        self._battery.setText(f"{frame.battery_percent}%")
        self._gps.setText(frame.gps.fix_state.value.replace("_", " ").upper())
        self._reverse.setText("ON" if frame.reverse else "OFF")
