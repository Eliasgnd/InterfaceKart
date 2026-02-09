"""Mock telemetry implementation for local development."""

from domain.telemetry_model import ConnectionState, GpsData, TelemetryFrame
from services.telemetry_service import TelemetryService


class MockTelemetryService(TelemetryService):
    """Generate deterministic placeholder telemetry data."""

    def __init__(self) -> None:
        self._running = False
        self._frame = TelemetryFrame()

    def start_stream(self) -> None:
        """Mark the mock stream as active and seed dummy state."""
        self._running = True
        self._frame.connection_state = ConnectionState.CONNECTED
        self._frame.gps = GpsData(latitude=37.7749, longitude=-122.4194, speed_kmh=42.0)

    def stop_stream(self) -> None:
        """Mark the mock stream as inactive."""
        self._running = False
        self._frame.connection_state = ConnectionState.DISCONNECTED

    def latest_frame(self) -> TelemetryFrame:
        """Return the current in-memory mock frame."""
        return self._frame
