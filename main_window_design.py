"""Module contains class MainWindowDesign which defines
main window design
"""
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QCheckBox


class MainWindowDesign:
    """Class defines main window design"""
    def __init__(self):
        self.init_gui()

    def init_gui(self):
        """Method for initializing graphic user interface"""
        self.setWindowTitle('Raw data to image')
        self.setMinimumSize(256, 128)
        self.open_button = QPushButton('Open file(s)', self)
        self.slideshow_checkbox = QCheckBox('Slideshow', self)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.open_button)
        hbox.addSpacing(16)
        hbox.addWidget(self.slideshow_checkbox)
        hbox.addStretch(1)

        container = QWidget(self)
        container.setLayout(hbox)
        self.setCentralWidget(container)
