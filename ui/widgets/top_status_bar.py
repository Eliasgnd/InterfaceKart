"""Top status bar widget."""

from domain.telemetry_model import ConnectivityState, GpsFixState
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class TopStatusBar(QWidget):
    """Displays compact telemetry status indicators."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TopStatusBar")
        self._speed_label = QLabel("0 km/h")
        self._battery_label = QLabel("Battery: --%")
        self._gps_label = QLabel("GPS: NO FIX")
        self._link_label = QLabel("LINK: DISCONNECTED")
        self._setup_ui()

    def _setup_ui(self) -> None:
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

    def set_gps_state(self, gps_state: GpsFixState) -> None:
        self._gps_label.setText(f"GPS: {gps_state.value.replace('_', ' ').upper()}")

    def set_connectivity(self, state: ConnectivityState) -> None:
        self._link_label.setText(f"LINK: {state.value.upper()}")
        self._link_label.setProperty("linkState", state.value)
        self.style().unpolish(self._link_label)
        self.style().polish(self._link_label)
