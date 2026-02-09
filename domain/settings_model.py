"""Application settings models."""

from dataclasses import dataclass
from enum import Enum


class ThemeMode(Enum):
    """Supported application themes."""

    DAY = "day"
    NIGHT = "night"


class OperatingMode(Enum):
    """Supported driving/operation modes."""

    NORMAL = "normal"
    ECO = "eco"
    SPORT = "sport"


@dataclass(slots=True)
class AppSettings:
    """User-configurable application settings."""

    theme: ThemeMode = ThemeMode.DAY
    operating_mode: OperatingMode = OperatingMode.NORMAL
    alerts_enabled: bool = True
