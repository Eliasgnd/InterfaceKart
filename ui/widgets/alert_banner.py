"""Alert banner widgets."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from domain.telemetry_model import Alert


class AlertBanner(QWidget):
    """Renders one alert with optional acknowledge action."""

    dismissed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._alert: Alert | None = None
        self.setObjectName("AlertBanner")
        self._message = QLabel("")
        self._dismiss_btn = QPushButton("Dismiss")
        self._dismiss_btn.clicked.connect(self._emit_dismiss)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(self._message, 1)
        layout.addWidget(self._dismiss_btn)

    def set_alert(self, alert: Alert) -> None:
        self._alert = alert
        self._message.setText(alert.message)
        self._dismiss_btn.setVisible(alert.ack_required)
        self.setProperty("alertLevel", alert.level.value)
        self.style().unpolish(self)
        self.style().polish(self)

    def _emit_dismiss(self) -> None:
        if self._alert is not None:
            self.dismissed.emit(self._alert.alert_id)


class AlertBannerHost(QWidget):
    """Shows/hides alert banner container."""

    alert_dismissed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._banner = AlertBanner()
        self._banner.dismissed.connect(self.alert_dismissed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.addWidget(self._banner)
        self.hide()

    def show_alert(self, alert: Alert | None) -> None:
        if alert is None:
            self.hide()
            return
        self._banner.set_alert(alert)
        self.show()
