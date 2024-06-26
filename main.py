"""Module for launching the application"""
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main() -> None:
    """Main method"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
