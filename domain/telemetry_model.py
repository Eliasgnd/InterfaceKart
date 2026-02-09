"""Domain models for telemetry and alerts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AlertLevel(Enum):
    """Severity levels for alerts."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ConnectionState(Enum):
    """Telemetry source connectivity state."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"


@dataclass(slots=True)
class GpsData:
    """GPS coordinates and travel information."""

    latitude: float = 0.0
    longitude: float = 0.0
    speed_kmh: float = 0.0


@dataclass(slots=True)
class Alert:
    """Single alert message emitted by telemetry checks."""

    level: AlertLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class TelemetryFrame:
    """Snapshot of incoming telemetry values."""

    gps: GpsData = field(default_factory=GpsData)
    battery_percent: int = 100
    connection_state: ConnectionState = ConnectionState.DISCONNECTED
