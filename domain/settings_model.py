"""Application settings domain models."""

from dataclasses import dataclass
from enum import Enum


class ThemeMode(str, Enum):
    """Supported application themes."""

    DAY = "day"
    NIGHT = "night"


class PageId(str, Enum):
    """Logical page identifiers for app routing."""

    HOME = "home"
    NAVIGATION = "navigation"
    CAMERA = "camera"
    SETTINGS = "settings"


@dataclass(slots=True)
class AppSettings:
    """User-configurable application settings."""

    theme_mode: ThemeMode = ThemeMode.NIGHT
    brightness: int = 80
    default_page: PageId = PageId.HOME
    map_follow: bool = True
    map_zoom: int = 12
