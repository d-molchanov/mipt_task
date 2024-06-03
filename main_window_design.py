from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QCheckBox


class MainWindowDesign(object):
    """docstring for MainWindowDesign"""
    def __init__(self):
        self.init_gui()
        

    def init_gui(self):
        self.setWindowTitle('Raw data to image')
        self.open_button = QPushButton('Open file(s)', self)
        self.slideshow_checkbox = QCheckBox('Slideshow', self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.open_button)
        hbox.addWidget(self.slideshow_checkbox)
        hbox.addStretch(1)
        

        # self.setLayout(self.vbox)
        # vbox = QVBoxLayout()
        # vbox.addLayout(hbox)
        # vbox.addStretch(1)

        # self.vbox = vbox

        container = QWidget(self)
        container.setLayout(hbox)
        self.setCentralWidget(container)
