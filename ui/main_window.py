"""Main application window."""

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from ui.pages.camera_page import CameraPage
from ui.pages.home_page import HomePage
from ui.pages.navigation_page import NavigationPage
from ui.pages.settings_page import SettingsPage
from ui.widgets.bottom_nav_bar import BottomNavBar
from ui.widgets.top_status_bar import TopStatusBar


class MainWindow(QMainWindow):
    """Root window that hosts top bar, pages, and bottom navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("InterfaceKart")
        self._page_stack = QStackedWidget()
        self._pages: dict[str, QWidget] = {}
        self._top_status_bar = TopStatusBar()
        self._bottom_nav = BottomNavBar()

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Create layout and register pages."""
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self._pages = {
            "home": HomePage(),
            "navigation": NavigationPage(),
            "camera": CameraPage(),
            "settings": SettingsPage(),
        }
        for page in self._pages.values():
            self._page_stack.addWidget(page)

        layout.addWidget(self._top_status_bar)
        layout.addWidget(self._page_stack, stretch=1)
        layout.addWidget(self._bottom_nav)
        self.setCentralWidget(central_widget)

    def _connect_signals(self) -> None:
        """Connect reusable widget signals to page routing."""
        self._bottom_nav.page_requested.connect(self.set_current_page)

    def set_current_page(self, page_name: str) -> None:
        """Switch visible page if the name exists."""
        page = self._pages.get(page_name)
        if page is not None:
            self._page_stack.setCurrentWidget(page)
