"""Domain models for telemetry frames and alerts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AlertLevel(str, Enum):
    """Severity for alert presentation."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ConnectivityState(str, Enum):
    """Link state of telemetry source."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"


class GpsFixState(str, Enum):
    """GPS lock quality."""

    NO_FIX = "no_fix"
    FIX_2D = "fix_2d"
    FIX_3D = "fix_3d"


@dataclass(slots=True)
class GpsData:
    """GPS position and heading details."""

    latitude: float = 0.0
    longitude: float = 0.0
    heading_deg: float = 0.0
    fix_state: GpsFixState = GpsFixState.NO_FIX


@dataclass(slots=True)
class Alert:
    """Alert event carried inside telemetry frame."""

    alert_id: str
    level: AlertLevel
    message: str
    ack_required: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class TelemetryFrame:
    """Snapshot for UI updates."""

    speed_kmh: float = 0.0
    battery_percent: int = 100
    reverse: bool = False
    connectivity: ConnectivityState = ConnectivityState.DISCONNECTED
    gps: GpsData = field(default_factory=GpsData)
    alerts: list[Alert] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
