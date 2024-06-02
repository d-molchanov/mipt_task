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
        self.slideshow_checkbox.clicked.connect(self.test)
        self.show()

    def create_window(self):
        child_window = ChildWindow()
        self.child_windows.append(child_window)

    def show_open_dialog(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Open file', '.')[0]
        for f in filenames:
            child_window = ChildWindow()
            child_window.load_image(f)
            child_window.show()
            self.child_windows.append(child_window)

    def test(self):
        print(self.slideshow_checkbox.isChecked())
        # if self.slideshow_checkbox.isChecked():
        #     self.period_hbox = QHBoxLayout()
        #     self.led = QLineEdit(self)
        #     self.led.setText('1')

        #     self.lbl = QLabel(self)
        #     self.lbl.setText('s')
        #     self.period_hbox.addWidget(self.led)
        #     self.period_hbox.addWidget(self.lbl)
        #     self.period_hbox.addStretch(1)
        #     self.vbox.insertLayout(1, self.period_hbox)

        #     # self.vbox.addWidget(self.led)
        #     # self.vbox.addStretch(1)
        # else:
        #     self.period_hbox.deleteLater()
        #     self.led.deleteLater()
        #     self.lbl.deleteLater()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())