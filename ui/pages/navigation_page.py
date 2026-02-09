"""Navigation placeholder page."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from domain.telemetry_model import TelemetryFrame


class NavigationPage(QWidget):
    """Map placeholder with map controls and GPS details."""

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
        self._build_ui()
        self._refresh_controls()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(12)

        map_placeholder = QFrame()
        map_placeholder.setObjectName("MapPlaceholder")
        map_layout = QVBoxLayout(map_placeholder)
        map_layout.addStretch(1)
        title = QLabel("Map view")
        title.setObjectName("PlaceholderTitle")
        subtitle = QLabel("OSM/QtLocation integration ready")
        subtitle.setObjectName("PlaceholderSubtitle")
        map_layout.addWidget(title, alignment=Qt.AlignHCenter)
        map_layout.addWidget(subtitle, alignment=Qt.AlignHCenter)
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
