"""Bottom navigation bar widget."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from domain.settings_model import PageId


class BottomNavBar(QWidget):
    """Touch-first bottom navigation with large buttons."""

    page_selected = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("BottomNavBar")
        self._buttons: dict[PageId, QPushButton] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        self._add_button(layout, "🏠 Home", PageId.HOME)
        self._add_button(layout, "🗺 Navigation", PageId.NAVIGATION)
        self._add_button(layout, "📷 Camera", PageId.CAMERA)
        self._add_button(layout, "⚙ Settings", PageId.SETTINGS)
        self.set_active_page(PageId.HOME)

    def _add_button(self, layout: QHBoxLayout, text: str, page: PageId) -> None:
        button = QPushButton(text)
        button.setObjectName("NavButton")
        button.setMinimumHeight(64)
        button.clicked.connect(lambda: self._on_button_clicked(page))
        self._buttons[page] = button
        layout.addWidget(button)

    def _on_button_clicked(self, page: PageId) -> None:
        self.set_active_page(page)
        self.page_selected.emit(page)

    def set_active_page(self, page: PageId) -> None:
        for page_id, button in self._buttons.items():
            button.setProperty("active", page_id == page)
            self.style().unpolish(button)
            self.style().polish(button)
