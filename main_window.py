import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog

from main_window_design import MainWindowDesign
from child_window import ChildWindow

class MainWindow(QMainWindow, MainWindowDesign):

    def __init__(self):
        super().__init__()

        self.child_windows = []
        self.open_button.clicked.connect(self.show_open_dialog)

    def create_window(self):
        child_window = ChildWindow()
        self.child_windows.append(child_window)

    def show_open_dialog(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Open file', '.')[0]
        if self.slideshow_checkbox.isChecked():
            child_window = ChildWindow()
            child_window.show_slideshow(filenames)
            child_window.show()
            self.child_windows.append(child_window)
        else:
            for f in filenames:
                child_window = ChildWindow()
                child_window.load_image(f)
                child_window.show()
                self.child_windows.append(child_window)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())