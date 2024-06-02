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
from PyQt6.QtCore import Qt, QSize, QTimer

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
        self.scale_edit.editingFinished.connect(self.change_image)
        self.button.clicked.connect(self.show_save_dialog)

    def change_scale(self, value):
        self.scale += value
        if self.scale < 0.0:
            self.scale = 0.01
        self.scale_edit.setText(f'{self.scale*100.0:.1f}')
        self.scale_pixmap(self.scale)

    def scale_pixmap(self, scale):
        if scale != 1:
            scaled = self.pixmap.scaled(
                QSize(
                    int(self.pixmap.width()*scale),
                    int(self.pixmap.height()*scale)
                )
            )
            self.label.setPixmap(scaled)
        else:
            self.label.setPixmap(self.pixmap)

    def choose_scale(self, pixmap, avail_geom, k_window, k_image):
        avail_width = avail_geom.width()
        avail_height = avail_geom.height()
        init_window_width = avail_width*k_window
        init_window_height = avail_height*k_window

        k_w_image = init_window_width * k_image / pixmap.width()
        k_h_image = init_window_height * k_image / pixmap.height()
        k_min_image = min(k_w_image, k_h_image)
        if k_min_image >= 1.0:
            scale = 1.0
        else:
            scale = k_min_image
        return scale

    def load_image(self, filename):
        self.setWindowTitle(filename)
        self.filename = filename
        self.pixmap = QPixmap(filename)
        avail_geom = QGuiApplication.primaryScreen().availableSize()
        
        k_window = 0.9
        k_image = 0.93

        scale = self.choose_scale(self.pixmap, avail_geom, k_window, k_image)
        if scale == 1.0:
            self.setGeometry(100, 100, int(self.pixmap.width()/k_image), int(self.pixmap.height()/k_image))
        else:
            self.setGeometry(100, 100, int(avail_geom.width()*k_window), int(avail_geom.height()*k_window))
        self.scale_pixmap(scale)
        self.scale_edit.setText(f'{scale*100:.1f}')
        self.scale = scale
        self.area.setWidget(self.label)

    def scale_pixmap_new(self, pixmap, scale):
        if scale != 1:
            scaled = pixmap.scaled(
                QSize(
                    int(pixmap.width()*scale),
                    int(pixmap.height()*scale)
                )
            )
            self.label.setPixmap(scaled)
        else:
            self.label.setPixmap(pixmap)

    def load_images(self, filenames):
        avail_geom = QGuiApplication.primaryScreen().availableSize()
        
        k_window = 0.9
        k_image = 0.93

        self.images = []
        for f in filenames:
            pixmap = QPixmap(f)
            temp = {
                'path': f,
                'pixmap': pixmap,
                'scale': self.choose_scale(pixmap, avail_geom, k_window, k_image)
            }
            self.images.append(temp)
        self.setGeometry(100, 100, int(avail_geom.width()*k_window), int(avail_geom.height()*k_window))
        self.area.setWidget(self.label)

        self.scale_edit.setEnabled(False)
        self.plus_button.setEnabled(False)
        self.minus_button.setEnabled(False)

        self.period_label = QLabel(self)
        self.period_label.setText('Period:')
        self.period_edit = QLineEdit(self)
        self.seconds_label = QLabel(self)
        self.seconds_label.setText('s')
        self.hbox.insertWidget(5, self.period_label)
        self.hbox.insertWidget(6, self.period_edit)
        self.hbox.insertWidget(7, self.seconds_label)
        # self.hbox.addWidget()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.image_number = 0
        self.timer.timeout.connect(lambda: self.show_images(self.images))
        self.timer.start()

    def show_images(self, images):
        if self.image_number == len(images):
            self.image_number = 0
        self.setWindowTitle(images[self.image_number]['path'])
        print(images[self.image_number]['path'])
        self.scale_pixmap_new(self.images[self.image_number]['pixmap'], self.images[self.image_number]['scale'])
        # self.label.setPixmap(images[self.image_number]['pixmap'])
        self.image_number += 1
            

    def change_image(self):
        try:
            scale = float(self.scale_edit.text())/100.0
        except ValueError:
            scale = self.scale
            self.scale_edit.setText(f'{scale*100:.1f}')
        if scale != self.scale:
            self.scale_pixmap(scale)
            self.scale = scale
            self.scale_edit.setText(f'{scale*100:.1f}')

    def show_save_dialog(self):
        filename, ext = QFileDialog.getSaveFileName(
            self, 'Save file', '.', '*.png;;*.jpg;;*.bmp'
        )
        new_filename = f'{filename}.{ext[2:]}' 
        print(new_filename)
        self.pixmap.save(new_filename, quality=-1)


        # avail_geom = QGuiApplication.primaryScreen().availableSize()
        # avail_width = avail_geom.width()
        # avail_height = avail_geom.height()
        # init_window_width = avail_width*k_window    # add int() maybe
        # init_window_height = avail_height*k_window  # add int() maybe

        # k_w_image = init_window_width * k_image / self.pixmap.width()
        # k_h_image = init_window_height * k_image / self.pixmap.height()
        # k_min_image = min(k_w_image, k_h_image)

        # if k_min_image >= 1.0:
        #     self.setGeometry(100, 100, int(self.pixmap.width()/k_image), int(self.pixmap.height()/k_image))
        #     self.scale_edit.setText('100.0')
        #     self.label.setPixmap(self.pixmap)
        #     self.scale = 1
        # else:
        #     self.setGeometry(100, 100, int(init_window_width), int(init_window_height))
        #     scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*k_min_image), int(self.pixmap.height()*k_min_image)))
        #     self.scale_edit.setText(f'{k_min_image*100:.1f}')
        #     self.label.setPixmap(scaled)
        #     self.scale = k_min_image
        # self.area.setWidget(self.label)

    # def change_scale(self, value):
    #     try:
    #         scale = float(self.scale_edit.text())
    #         scale += value
    #         self.scale = scale/100.0
    #     except ValueError:
    #         scale = self.scale*100.0
    #     self.scale_edit.setText(f'{scale:.1f}')
    #     self.scale_pixmap(scale/100)

    # def increase_scale(self):
    #     try:
    #         value = float(self.scale_edit.text())
    #         value += 25
    #         self.scale = value/100.0
    #     except ValueError:
    #         value = self.scale*100.0
    #     self.scale_edit.setText(f'{value:.1f}')
    #     self.scale_pixmap(value/100)


    # def decrease_scale(self):
    #     try:
    #         value = float(self.scale_edit.text())
    #         value -= 25
    #         self.scale = value/100.0
    #     except ValueError:
    #         value = self.scale*100
    #     if value <= 0:
    #         value = 1.0
    #     self.scale_edit.setText(f'{value:.1f}')
    #     self.scale_pixmap(value/100)



    # def greet(self):
    #     print('Hello!')
    #     self.load_image('grayscale_test.png')


    # def change_image(self):
    #     print(self.scale_edit.text())
    #     try:
    #         scale = float(self.scale_edit.text())/100.0
    #         scaled = self.pixmap.scaled(QSize(int(self.pixmap.width()*scale), int(self.pixmap.height()*scale)))
    #         self.label.setPixmap(scaled)
    #         self.scale = scale
    #     except ValueError:
    #         scale = self.scale
    #     self.scale_edit.setText(f'{scale*100:.1f}')
        

        

        
    # def saveFileDialog(self):
    #     # dialog = QFileDialog()
    #     # dialog.setNameFilter('*.png, *.jpg, *.bmp')
    #     # dialog.exec()
    #     # filename = dialog.getSaveFileName(self, 'Save file', '*.png, *.jpg, *.bmp')
    #     # filename = QFileDialog.getSaveFileName(self, 'Save file', self.filename, 'Images (*.png, *.jpg, *.bmp)')
    #     filename, ext = QFileDialog.getSaveFileName(self, 'Save file', '.', '*.png;;*.jpg;;*.bmp')
    #     new_filename = f'{filename}.{ext[2:]}' 
    #     print(new_filename)
    #     self.pixmap.save(new_filename, quality=-1)
    #     # self.label.resize(600, 600)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = ChildWindow()
    main_window.load_images(
        [
            './colormap_beam.png',
            './colormap_big.png',
            './grayscale_test.png'
        ]
    )
    main_window.show()
    sys.exit(app.exec())
