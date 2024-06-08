"""Module contains class MainWindow for creating
main application window
"""
import sys
from typing import List
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog

from main_window_design import MainWindowDesign
from child_window import ChildWindow


class MainWindow(QMainWindow, MainWindowDesign):
    """Class for creating main application window"""
    def __init__(self):
        super().__init__()

        self.child_windows = []
        self.open_button.clicked.connect(self._show_open_dialog)

    def create_child_windows(self, filenames: List[str]) -> None:
        """Method for creating child windows"""
        for f in filenames:
            child_window = ChildWindow()
            child_window.load_csv_files([f])
            if child_window.get_single_image(0):
                child_window.show_single_image(0)
                child_window.show()
                self.child_windows.append(child_window)

    def create_slideshow_window(self, filenames: List[str]) -> None:
        """Method for creating slideshow window"""
        child_window = ChildWindow()
        child_window.load_csv_files(filenames)
        child_window.show_slideshow()
        child_window.show()
        self.child_windows.append(child_window)

    def _show_open_dialog(self) -> None:
        """Method for opening a dialog box to select scv-files to process"""
        filenames = QFileDialog.getOpenFileNames(
            self, 'Open file', '.', '*.csv *.txt'
        )[0]
        if filenames:
            if self.slideshow_checkbox.isChecked():
                self.create_slideshow_window(filenames)
            else:
                self.create_child_windows(filenames)


def test() -> None:
    """Function for testing MainWindow class methods"""
    test_files = [
        './test_cases/grayscale_with_wrong_header.csv',
        './test_cases/atom_rgb.csv',
        './test_cases/rgb_with_wrong_header.csv',
        './test_cases/rgb_without_header.csv',
        './test_cases/permission_denied.csv',
        './test_cases/not_exists.csv',
        './test_cases/not_rectangular.csv',
        './test_cases/not_csv.csv',
        './test_cases/atom_grayscale.csv',
        './test_cases/empty.csv',
        './test_cases/different_separator.csv'

    ]
    main_window = MainWindow()
    main_window.create_slideshow_window(test_files)
    main_window.create_child_windows(test_files)
    main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test()
    sys.exit(app.exec())
