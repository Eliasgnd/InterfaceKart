"""Camera placeholder page."""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

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
        video_placeholder = QFrame()
        video_placeholder.setObjectName("CameraPlaceholder")
        video_layout = QVBoxLayout(video_placeholder)
        video_layout.addStretch(1)
        video_layout.addWidget(QLabel("Camera/Bird-eye feed placeholder"))
        video_layout.addStretch(1)
        root.addWidget(video_placeholder, 1)
        root.addWidget(self._mode)
        root.addWidget(self._reverse)

        buttons = QHBoxLayout()
        for mode in ["Rear", "Front", "Mosaic", "Bird-eye"]:
            btn = QPushButton(mode)
            btn.clicked.connect(lambda _=False, m=mode: self._mode.setText(f"Mode: {m}"))
            buttons.addWidget(btn)
        root.addLayout(buttons)

    def on_telemetry(self, frame: TelemetryFrame) -> None:
        self._reverse.setText("Reverse engaged" if frame.reverse else "Reverse engaged: NO")
