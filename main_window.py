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
        filenames = QFileDialog.getOpenFileNames(self, 'Open file', './task/attached_data/for_extra_task', '*.csv *.txt')[0]
        if self.slideshow_checkbox.isChecked():
            child_window = ChildWindow()
            child_window.load_raw_data(filenames)
            child_window.show_slideshow()
            child_window.show()
            self.child_windows.append(child_window)
        else:
            for f in filenames:
                child_window = ChildWindow()
                child_window.load_raw_data([f])
                child_window.show_single_image()
                child_window.show()
                self.child_windows.append(child_window)


if __name__ == '__main__':
    CSVs_ = [
        './task/attached_data/for_extra_task/test_rgb.csv',
        './task/attached_data/for_extra_task/atom_rgb.csv',
        './task/attached_data/for_extra_task/beam_rgb.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_rgb.csv',
        './task/attached_data/for_extra_task/atom_grayscale.csv',
        './task/attached_data/for_extra_task/beam_grayscale.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_grayscale.csv'
    ]

    app = QApplication(sys.argv)
    main_window = MainWindow()
    windows = []
    for i in range(4):
    # for filename in CSVs_[:4]:
        filename = CSVs_[3]
        print(filename)
        child_window = ChildWindow()
        # child_window.test_load_file(filename)
        child_window.test_load_csv_to_label(filename, 4)
        child_window.show()
        windows.append(child_window)
    main_window.show()
    sys.exit(app.exec())