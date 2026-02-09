"""Application entry point for InterfaceKart."""

from PySide6.QtWidgets import QApplication

from app.controller import ApplicationController


def main() -> int:
    """Create the Qt application and start the main event loop."""
    app = QApplication([])
    controller = ApplicationController(app)
    controller.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
