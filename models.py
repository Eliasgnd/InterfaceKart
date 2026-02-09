"""Modèles simples de l'application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ThemeMode(str, Enum):
    DAY = "day"
    NIGHT = "night"


class PageId(str, Enum):
    HOME = "home"
    NAVIGATION = "navigation"
    CAMERA = "camera"
    SETTINGS = "settings"


@dataclass(slots=True)
class AppSettings:
    theme_mode: ThemeMode = ThemeMode.NIGHT
    brightness: int = 80
    default_page: PageId = PageId.HOME
    map_follow: bool = True
    map_zoom: int = 12


class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ConnectivityState(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"


class GpsFixState(str, Enum):
    NO_FIX = "no_fix"
    FIX_2D = "fix_2d"
    FIX_3D = "fix_3d"


@dataclass(slots=True)
class GpsData:
    latitude: float = 0.0
    longitude: float = 0.0
    heading_deg: float = 0.0
    fix_state: GpsFixState = GpsFixState.NO_FIX


@dataclass(slots=True)
class Alert:
    alert_id: str
    level: AlertLevel
    message: str
    ack_required: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class TelemetryFrame:
    speed_kmh: float = 0.0
    battery_percent: int = 100
    reverse: bool = False
    connectivity: ConnectivityState = ConnectivityState.DISCONNECTED
    gps: GpsData = field(default_factory=GpsData)
    alerts: list[Alert] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
