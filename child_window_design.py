"""Module contains class ChildWindowDesign which defines
design of child windows
"""
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea

from PyQt6.QtCore import Qt


class ChildWindowDesign:
    """Class defines design of child windows"""
    def __init__(self):
        self.init_gui()

    def init_gui(self):
        """Method for initializing graphic user interface"""
        self.save_button = QPushButton('Save as', self)
        self.decrease_scale_button = QPushButton('-', self)
        self.decrease_scale_button.setFixedSize(24, 24)
        self.scale_edit = QLineEdit(
            self, alignment=Qt.AlignmentFlag.AlignRight
        )
        self.scale_edit.setFixedWidth(42)
        self.increase_scale_button = QPushButton('+', self)
        self.increase_scale_button.setFixedSize(24, 24)
        self.load_colormap_button = QPushButton('Load colormap', self)
        self.load_colormap_button.setVisible(False)

        self.interval_widget = QWidget(self)
        interval_hbox = QHBoxLayout(self.interval_widget)
        self.interval_edit = QLineEdit(
            self, alignment=Qt.AlignmentFlag.AlignRight
        )
        self.interval_edit.setFixedWidth(42)
        interval_hbox.addWidget(QLabel('Slideshow interval:', self))
        interval_hbox.addWidget(self.interval_edit)
        interval_hbox.addWidget(QLabel('s', self))
        self.interval_widget.setVisible(False)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.decrease_scale_button)
        self.hbox.addWidget(self.scale_edit)
        self.hbox.addWidget(QLabel(self, text='%'))
        self.hbox.addWidget(self.increase_scale_button)
        self.hbox.addWidget(self.load_colormap_button)
        self.hbox.addWidget(self.interval_widget)
        self.hbox.addStretch(1)

        self.image_label = QLabel(
            self, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.image_scroll_area = QScrollArea(self)
        self.image_scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addLayout(self.hbox)
        layout.addWidget(self.image_scroll_area)
        layout.addWidget(self.image_label)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
