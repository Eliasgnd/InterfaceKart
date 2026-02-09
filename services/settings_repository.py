"""JSON-backed settings persistence."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from domain.settings_model import AppSettings, PageId, ThemeMode


class SettingsRepository:
    """Load/save app settings from project-root JSON."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or Path(__file__).resolve().parent.parent / "user_settings.json"

    def load_settings(self) -> AppSettings:
        """Load persisted settings or return safe defaults."""
        if not self._path.exists():
            return AppSettings()
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            return AppSettings(
                theme_mode=ThemeMode(payload.get("theme_mode", AppSettings().theme_mode.value)),
                brightness=int(payload.get("brightness", AppSettings().brightness)),
                default_page=PageId(payload.get("default_page", AppSettings().default_page.value)),
                map_follow=bool(payload.get("map_follow", AppSettings().map_follow)),
                map_zoom=int(payload.get("map_zoom", AppSettings().map_zoom)),
            )
        except (ValueError, TypeError, json.JSONDecodeError):
            return AppSettings()

    def save_settings(self, settings: AppSettings) -> None:
        """Persist settings to disk."""
        payload = asdict(settings)
        payload["theme_mode"] = settings.theme_mode.value
        payload["default_page"] = settings.default_page.value
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
