import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QCheckBox


from PyQt6.QtGui import QAction, QIcon, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QSize

class MainWindowDesign(object):
    """docstring for MainWindowDesign"""
    def __init__(self):
        self.init_gui()
        

    def init_gui(self):
        self.setWindowTitle('Raw data to image')

        self.open_button = QPushButton(self)
        self.open_button.setText('Open file(s)')

        self.slideshow_checkbox = QCheckBox(self)
        self.slideshow_checkbox.setText('Slideshow')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.open_button)
        self.vbox.addWidget(self.slideshow_checkbox)
        self.vbox.addStretch(1)
        

        # self.setLayout(self.vbox)
        # vbox = QVBoxLayout()
        # vbox.addLayout(hbox)
        # vbox.addStretch(1)

        # self.vbox = vbox

        container = QWidget(self)
        container.setLayout(self.vbox)
        self.setCentralWidget(container)
