"""Tracks active alerts and acknowledgement state."""

from __future__ import annotations

from domain.telemetry_model import Alert, AlertLevel


class AlertManager:
    """Maintains alert lifecycle for banner display."""

    _priority = {
        AlertLevel.INFO: 0,
        AlertLevel.WARNING: 1,
        AlertLevel.CRITICAL: 2,
    }

    def __init__(self) -> None:
        self._active: dict[str, Alert] = {}
        self._acked: set[str] = set()

    def ingest(self, alerts: list[Alert]) -> None:
        """Merge new alerts into active list."""
        for alert in alerts:
            self._active[alert.alert_id] = alert

    def acknowledge(self, alert_id: str) -> None:
        """Mark an alert as acknowledged."""
        self._acked.add(alert_id)

    def get_banner_alert(self) -> Alert | None:
        """Get highest-priority unacknowledged active alert."""
        candidates = [a for a in self._active.values() if a.alert_id not in self._acked]
        if not candidates:
            return None
        candidates.sort(key=lambda a: self._priority[a.level], reverse=True)
        return candidates[0]
