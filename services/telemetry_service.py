"""Telemetry service contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.telemetry_model import TelemetryFrame


class TelemetryService(ABC):
    """Base interface for telemetry providers."""

    @abstractmethod
    def start_stream(self) -> None:
        """Start telemetry data collection."""

    @abstractmethod
    def stop_stream(self) -> None:
        """Stop telemetry data collection."""

    @abstractmethod
    def latest_frame(self) -> TelemetryFrame:
        """Return the latest telemetry snapshot."""
