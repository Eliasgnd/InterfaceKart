"""WebSocket telemetry service stub."""

from domain.telemetry_model import TelemetryFrame
from services.telemetry_service import TelemetryService


class WebSocketTelemetryService(TelemetryService):
    """Placeholder implementation for future WebSocket integration."""

    def __init__(self, endpoint_url: str) -> None:
        self._endpoint_url = endpoint_url
        self._frame = TelemetryFrame()

    def start_stream(self) -> None:
        """Connect to a WebSocket endpoint and begin receiving data."""
        # TODO: add websocket connection lifecycle.

    def stop_stream(self) -> None:
        """Disconnect from the WebSocket endpoint."""
        # TODO: close websocket connection.

    def latest_frame(self) -> TelemetryFrame:
        """Return the latest frame received from the socket."""
        return self._frame
