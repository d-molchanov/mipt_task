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

class ChildWindowDesign(object):

    def __init__(self):

        self.init_gui()

    def init_gui(self):
        self.label = QLabel(self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        self.button = QPushButton('Save as')
        self.plus_button = QPushButton('+')
        self.plus_button.setFixedSize(QSize(24, 24))
        self.minus_button = QPushButton('-')
        self.minus_button.setFixedSize(QSize(24, 24))

        self.scale_edit = QLineEdit(self)
        self.scale_edit.setFixedWidth(42)
        self.persentage = QLabel(self, text='%')

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.minus_button)
        self.hbox.addWidget(self.scale_edit)
        self.hbox.addWidget(self.persentage)
        self.hbox.addWidget(self.plus_button)
        self.hbox.addStretch(1)
        
        layout = QVBoxLayout()
        layout.addLayout(self.hbox)
        layout.addWidget(self.area)
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        
        # self.show()