"""Services simples de l'application (settings, thème, telemetry, alertes)."""

from __future__ import annotations

import json
import math
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QApplication

from models import (
    Alert,
    AlertLevel,
    AppSettings,
    ConnectivityState,
    GpsData,
    GpsFixState,
    PageId,
    TelemetryFrame,
    ThemeMode,
)


class TelemetryService(QObject):
    telemetry_updated = Signal(object)

    def start(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError


class MockTelemetryService(TelemetryService):
    def __init__(self, update_ms: int = 80) -> None:
        super().__init__()
        self._timer = QTimer(self)
        self._timer.setInterval(update_ms)
        self._timer.timeout.connect(self._tick)
        self._phase = 0.0
        self._battery = 100.0
        self._lat = 37.7749
        self._lon = -122.4194

    def start(self) -> None:
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def _tick(self) -> None:
        self._phase += 0.07
        speed = max(0.0, 28 + 16 * math.sin(self._phase))
        self._battery = max(5.0, self._battery - 0.006)
        heading = (self._phase * 37) % 360
        self._lat += 0.00002 * math.cos(self._phase)
        self._lon += 0.00002 * math.sin(self._phase)
        reverse = speed < 6 and int(self._phase * 9) % 30 == 0

        alerts: list[Alert] = []
        if self._battery < 20 and int(self._phase * 10) % 35 == 0:
            alerts.append(
                Alert(
                    alert_id="battery-low",
                    level=AlertLevel.WARNING,
                    message="Battery low. Please plan a recharge soon.",
                )
            )
        if int(self._phase * 10) % 250 == 0:
            alerts.append(
                Alert(
                    alert_id="overheat",
                    level=AlertLevel.CRITICAL,
                    message="Motor temperature critical. Slow down now.",
                    ack_required=True,
                )
            )

        frame = TelemetryFrame(
            speed_kmh=speed,
            battery_percent=int(self._battery),
            reverse=reverse,
            connectivity=ConnectivityState.CONNECTED,
            gps=GpsData(
                latitude=self._lat,
                longitude=self._lon,
                heading_deg=heading,
                fix_state=GpsFixState.FIX_3D,
            ),
            alerts=alerts,
            timestamp=datetime.utcnow(),
        )
        self.telemetry_updated.emit(frame)


class SettingsRepository:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or Path(__file__).resolve().parent / "user_settings.json"

    def load_settings(self) -> AppSettings:
        if not self._path.exists():
            return AppSettings()
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            defaults = AppSettings()
            return AppSettings(
                theme_mode=ThemeMode(payload.get("theme_mode", defaults.theme_mode.value)),
                brightness=int(payload.get("brightness", defaults.brightness)),
                default_page=PageId(payload.get("default_page", defaults.default_page.value)),
                map_follow=bool(payload.get("map_follow", defaults.map_follow)),
                map_zoom=int(payload.get("map_zoom", defaults.map_zoom)),
            )
        except (ValueError, TypeError, json.JSONDecodeError):
            return AppSettings()

    def save_settings(self, settings: AppSettings) -> None:
        payload = asdict(settings)
        payload["theme_mode"] = settings.theme_mode.value
        payload["default_page"] = settings.default_page.value
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class ThemeManager:
    def __init__(self, application: QApplication) -> None:
        self._application = application

    def apply_theme(self, theme_mode: ThemeMode, brightness: int) -> None:
        stylesheet_name = "day.qss" if theme_mode == ThemeMode.DAY else "night.qss"
        stylesheet_path = Path(__file__).resolve().parent / "styles" / stylesheet_name
        base_qss = stylesheet_path.read_text(encoding="utf-8")
        clamped = max(0, min(100, brightness))
        overlay_opacity = (100 - clamped) / 130.0
        brightness_qss = (
            "QWidget#RootWindow {"
            f"background-color: rgba(0, 0, 0, {overlay_opacity:.2f});"
            "}"
        )
        self._application.setStyleSheet(base_qss + "\n" + brightness_qss)


class AlertManager:
    _priority = {AlertLevel.INFO: 0, AlertLevel.WARNING: 1, AlertLevel.CRITICAL: 2}

    def __init__(self) -> None:
        self._active: dict[str, Alert] = {}
        self._acked: set[str] = set()

    def ingest(self, alerts: list[Alert]) -> None:
        for alert in alerts:
            self._active[alert.alert_id] = alert

    def acknowledge(self, alert_id: str) -> None:
        self._acked.add(alert_id)

    def get_banner_alert(self) -> Alert | None:
        candidates = [a for a in self._active.values() if a.alert_id not in self._acked]
        if not candidates:
            return None
        candidates.sort(key=lambda a: self._priority[a.level], reverse=True)
        return candidates[0]
