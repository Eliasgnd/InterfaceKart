"""Simple router for page navigation."""

from ui.main_window import MainWindow


class AppRouter:
    """Manage window creation and page switching."""

    def __init__(self) -> None:
        self._main_window = MainWindow()

    def show_main_window(self) -> None:
        """Show the primary window."""
        self._main_window.show()

    def navigate_to(self, page_name: str) -> None:
        """Navigate to a named page in the main window."""
        self._main_window.set_current_page(page_name)
