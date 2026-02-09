"""Camera placeholder page."""

from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from domain.telemetry_model import TelemetryFrame


class CameraPage(QWidget):
    """Camera feed placeholders and mode selectors."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._mode = QLabel("Mode: Rear")
        self._reverse = QLabel("Reverse engaged: NO")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(12)

        feeds = QGridLayout()
        main_feed = self._camera_tile("Rear camera")
        side_left = self._camera_tile("Left side")
        side_right = self._camera_tile("Right side")
        feeds.addWidget(main_feed, 0, 0, 2, 2)
        feeds.addWidget(side_left, 0, 2)
        feeds.addWidget(side_right, 1, 2)
        root.addLayout(feeds, 1)

        status = QHBoxLayout()
        status.addWidget(self._mode)
        status.addStretch(1)
        status.addWidget(self._reverse)
        root.addLayout(status)

        buttons = QHBoxLayout()
        for mode in ["Rear", "Front", "Mosaic", "Bird-eye"]:
            btn = QPushButton(mode)
            btn.clicked.connect(lambda _=False, m=mode: self._mode.setText(f"Mode: {m}"))
            buttons.addWidget(btn)
        root.addLayout(buttons)

    def _camera_tile(self, text: str) -> QFrame:
        tile = QFrame()
        tile.setObjectName("CameraPlaceholder")
        layout = QVBoxLayout(tile)
        layout.addStretch(1)
        layout.addWidget(QLabel(text))
        layout.addStretch(1)
        return tile

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._reverse.setText("Reverse engaged" if frame.reverse else "Reverse engaged: NO")
