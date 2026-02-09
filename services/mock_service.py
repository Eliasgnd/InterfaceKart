"""Mock telemetry service driven by QTimer."""

from __future__ import annotations

import math
from datetime import datetime

from PySide6.QtCore import QTimer

from domain.telemetry_model import (
    Alert,
    AlertLevel,
    ConnectivityState,
    GpsData,
    GpsFixState,
    TelemetryFrame,
)
from services.telemetry_service import TelemetryService


class MockTelemetryService(TelemetryService):
    """Emits smooth fake telemetry at interactive refresh rates."""

    def __init__(self, update_ms: int = 80) -> None:
        super().__init__()
        self._timer = QTimer(self)
        self._timer.setInterval(update_ms)
        self._timer.timeout.connect(self._tick)
        self._phase = 0.0
        self._battery = 100.0
        self._lat = 37.7749
        self._lon = -122.4194

    def start(self) -> None:
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def _tick(self) -> None:
        self._phase += 0.07
        speed = max(0.0, 28 + 16 * math.sin(self._phase))
        self._battery = max(5.0, self._battery - 0.006)
        heading = (self._phase * 37) % 360
        self._lat += 0.00002 * math.cos(self._phase)
        self._lon += 0.00002 * math.sin(self._phase)
        reverse = speed < 6 and int(self._phase * 9) % 30 == 0

        alerts: list[Alert] = []
        if self._battery < 20 and int(self._phase * 10) % 35 == 0:
            alerts.append(
                Alert(
                    alert_id="battery-low",
                    level=AlertLevel.WARNING,
                    message="Battery low. Please plan a recharge soon.",
                    ack_required=False,
                )
            )
        if int(self._phase * 10) % 250 == 0:
            alerts.append(
                Alert(
                    alert_id="overheat",
                    level=AlertLevel.CRITICAL,
                    message="Motor temperature critical. Slow down now.",
                    ack_required=True,
                )
            )

        frame = TelemetryFrame(
            speed_kmh=speed,
            battery_percent=int(self._battery),
            reverse=reverse,
            connectivity=ConnectivityState.CONNECTED,
            gps=GpsData(
                latitude=self._lat,
                longitude=self._lon,
                heading_deg=heading,
                fix_state=GpsFixState.FIX_3D,
            ),
            alerts=alerts,
            timestamp=datetime.utcnow(),
        )
        self.telemetry_updated.emit(frame)
