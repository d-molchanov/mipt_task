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

from child_window_design import ChildWindowDesign

class ChildWindow(QMainWindow, ChildWindowDesign):

    def __init__(self):
        super().__init__()

        scale_step = 0.25
        self.plus_button.clicked.connect(
            lambda: self.change_scale(scale_step)
        )
        self.minus_button.clicked.connect(
            lambda: self.change_scale(-scale_step)
        )
        self.text_edit.editingFinished.connect(self.change_image)
        self.button.clicked.connect(self.saveFileDialog)
        self.show()

    def change_scale(self, value):
        self.scale += value
        if self.scale < 0.0:
            self.scale = 0.01
        self.text_edit.setText(f'{self.scale*100.0:.1f}')
        self.scale_pixmap(self.scale)

    # def change_scale(self, value):
    #     try:
    #         scale = float(self.text_edit.text())
    #         scale += value
    #         self.scale = scale/100.0
    #     except ValueError:
    #         scale = self.scale*100.0
    #     self.text_edit.setText(f'{scale:.1f}')
    #     self.scale_pixmap(scale/100)

    # def increase_scale(self):
    #     try:
    #         value = float(self.text_edit.text())
    #         value += 25
    #         self.scale = value/100.0
    #     except ValueError:
    #         value = self.scale*100.0
    #     self.text_edit.setText(f'{value:.1f}')
    #     self.scale_pixmap(value/100)


    # def decrease_scale(self):
    #     try:
    #         value = float(self.text_edit.text())
    #         value -= 25
    #         self.scale = value/100.0
    #     except ValueError:
    #         value = self.scale*100
    #     if value <= 0:
    #         value = 1.0
    #     self.text_edit.setText(f'{value:.1f}')
    #     self.scale_pixmap(value/100)



    # def greet(self):
    #     print('Hello!')
    #     self.load_image('grayscale_test.png')
    def scale_pixmap(self, scale):
        scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*scale), int(self.pixmap.height()*scale)))
        self.label.setPixmap(scaled)


    def change_image(self):
        print(self.text_edit.text())
        try:
            scale = float(self.text_edit.text())/100.0
            scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*scale), int(self.pixmap.height()*scale)))
            self.label.setPixmap(scaled)
            self.scale = scale
        except ValueError:
            scale = self.scale
        self.text_edit.setText(f'{scale*100:.1f}')
        

    def load_image(self, filename):
        self.setWindowTitle(filename)
        self.filename = filename
        self.pixmap = QPixmap(filename)
        print(self.text_edit.height())
        # scaled = pixmap.scaled(QSize(pixmap.width()//2, pixmap.height()//2))
        # scaled = self.pixmap.scaled(QSize(self.pixmap.width(), self.pixmap.height()))
        
        avail_geom = QGuiApplication.primaryScreen().availableSize()
        avail_width = avail_geom.width()
        avail_height = avail_geom.height()
        k_window = 0.9
        init_window_width = avail_width*k_window    # add int() maybe
        init_window_height = avail_height*k_window  # add int() maybe

        k_image = 0.93
        k_w_image = init_window_width * k_image / self.pixmap.width()
        k_h_image = init_window_height * k_image / self.pixmap.height()
        k_min_image = min(k_w_image, k_h_image)

        if k_min_image >= 1.0:
            self.setGeometry(100, 100, int(self.pixmap.width()/k_image), int(self.pixmap.height()/k_image))
            self.text_edit.setText('100.0')
            self.label.setPixmap(self.pixmap)
            self.scale = 1
        else:
            self.setGeometry(100, 100, int(init_window_width), int(init_window_height))
            scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*k_min_image), int(self.pixmap.height()*k_min_image)))
            self.text_edit.setText(f'{k_min_image*100:.1f}')
            self.label.setPixmap(scaled)
            self.scale = k_min_image
        self.area.setWidget(self.label)
        

        # print(f'{self.frameGeometry() = }')
        # print(f'{self.geometry() = }')
        # print(k_min, k_h, k_w)
        # self.setGeometry(100, 100, int(avail_width*0.9), int(avail_height*0.9))
        # self.setGeometry(100, 100, int(self.pixmap.width()/k), int(self.pixmap.height()/k))
        
    def saveFileDialog(self):
        # dialog = QFileDialog()
        # dialog.setNameFilter('*.png, *.jpg, *.bmp')
        # dialog.exec()
        # filename = dialog.getSaveFileName(self, 'Save file', '*.png, *.jpg, *.bmp')
        # filename = QFileDialog.getSaveFileName(self, 'Save file', self.filename, 'Images (*.png, *.jpg, *.bmp)')
        filename, ext = QFileDialog.getSaveFileName(self, 'Save file', '.', '*.png;;*.jpg;;*.bmp')
        new_filename = f'{filename}.{ext[2:]}' 
        print(new_filename)
        self.pixmap.save(new_filename, quality=-1)
        # self.label.resize(600, 600)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = ChildWindow()
    sys.exit(app.exec())
