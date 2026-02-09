"""Telemetry service contract."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from domain.telemetry_model import TelemetryFrame


class TelemetryService(QObject):
    """Abstract telemetry provider interface."""

    telemetry_updated = Signal(object)

    def start(self) -> None:
        """Start telemetry streaming."""
        raise NotImplementedError

    def stop(self) -> None:
        """Stop telemetry streaming."""
        raise NotImplementedError
