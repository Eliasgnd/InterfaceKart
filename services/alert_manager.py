"""Alert creation and filtering helpers."""

from domain.telemetry_model import Alert, AlertLevel


class AlertManager:
    """Build alert objects from raw conditions."""

    def create_alert(self, message: str, level: AlertLevel = AlertLevel.INFO) -> Alert:
        """Create a simple alert object with a severity."""
        return Alert(level=level, message=message)
