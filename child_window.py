import sys
import io
import time
from typing import List

from PIL import ImageQt

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

from PyQt6.QtGui import QAction, QIcon, QPixmap, QGuiApplication, QImage
from PyQt6.QtCore import Qt, QTimer, QBuffer

from child_window_design import ChildWindowDesign
from image_maker import ImageMaker

class ChildWindow(QMainWindow, ChildWindowDesign):

    def __init__(self):
        super().__init__()
        self.show()
        
        self.timer = QTimer(self)

        scale_step = 0.25
        self.slideshow_interval = 1000
        self.window_scale_factor = 0.9
        self.image_scale_factor = 0.9
        self.increase_scale_button.clicked.connect(
            lambda: self.change_scale(scale_step)
        )
        self.decrease_scale_button.clicked.connect(
            lambda: self.change_scale(-scale_step)
        )
        self.scale_edit.editingFinished.connect(self.change_image)
        self.save_button.clicked.connect(self.show_save_dialog)
        self.interval_edit.editingFinished.connect(self.change_interval)
        self.load_colormap_button.clicked.connect(self.show_open_dialog)

    def change_scale(self, value):
        self.scale += value
        if self.scale <= 0.0:
            self.scale = 0.01
        self.scale_edit.setText(f'{self.scale*100.0:.1f}')
        self.scale_pixmap_new(self.pixmap, self.scale)

    def change_image(self):
        try:
            self.scale = float(self.scale_edit.text())/100.0
            if self.scale <= 0:
                self.scale = 0.01
            self.scale_pixmap_new(self.pixmap, self.scale)
        except ValueError:
            pass
        self.scale_edit.setText(f'{self.scale*100:.1f}')

    def scale_image(self, image, scale):
        if scale != 1:
            scaled = image.scaled(
                int(image.width()*scale),
                int(image.height()*scale),
                transformMode=Qt.TransformationMode.FastTransformation
            )
            print(5)
            return scaled
            # self.image_label.setPixmap(QPixmap(scaled))
            # print(6)
        else:
            # self.image_label.setPixmap(QPixmap(scaled))
            return image
        # print(self.image_label.pixmap().size())

    def scale_pixmap_new(self, pixmap, scale):
        print(scale, pixmap.width(), pixmap.height())
        if scale != 1:
            scaled = pixmap.scaled(
                int(pixmap.width()*scale),
                int(pixmap.height()*scale),
                transformMode=Qt.TransformationMode.FastTransformation
            )
            # image = QImage(pixmap)
            # print(image)
            # pil_image = ImageQt.fromqimage(image)
            # print(pil_image)
            # image = image.scaledToWidth(
            #     int(image.width()*scale),
            #     mode=Qt.TransformationMode.FastTransformation
            # )
            print(5)
            # pixmap.resize(
            #     int(pixmap.width()*scale),
            #     int(pixmap.height()*scale)
            # )
            self.image_label.setPixmap(QPixmap(scaled))
            print(6)
        else:
            self.image_label.setPixmap(pixmap)
        print(self.image_label.pixmap().size())

    def choose_scale(
        self, pixmap: QPixmap, width: int, height: int,
        window_scale_factor: float, image_scale_factor: float
    ) -> float:
        window_width = width*window_scale_factor
        window_height = height*window_scale_factor

        k_w_image = window_width * image_scale_factor / pixmap.width()
        k_h_image = window_height * image_scale_factor / pixmap.height()
        k_min_image = min(k_w_image, k_h_image)
        if k_min_image >= 1.0:
            scale = 1.0
        else:
            scale = k_min_image
        return scale

    def show_single_image(self) -> None:
        width, height = self._get_available_screen_size()
        print(width, height)
        image = self.images[0]
        self.setWindowTitle(image['path'])
        if image['mode'] == 'L':
            self.load_colormap_button.setVisible(True)
        # self.pixmap = image['pixmap']
        print(1)
        # scale = self.choose_scale(
        #     image['pixmap'],
        #     width,
        #     height,
        #     self.window_scale_factor,
        #     self.image_scale_factor
        # )
        scale = self.choose_scale(
            image['image'],
            width,
            height,
            self.window_scale_factor,
            self.image_scale_factor
        )
        print(2, scale)
        image['scale'] = scale
        if scale == 1.0:
            self.resize(
                int(image['image'].width()/self.image_scale_factor),
                int(image['image'].height()/self.image_scale_factor)
            )
        else:
            self.resize(
                int(width*self.window_scale_factor),
                int(height*self.window_scale_factor)
            )
        print(3, image['image'])
        image['image'].save('without_scale.png')
        print(4)
        scaled = self.scale_image(image['image'], scale)
        self.image_label.setPixmap(QPixmap(scaled))
        # self.scale_pixmap_new(self.pixmap, scale)
        print(4)
        self.scale_edit.setText(f'{scale*100:.1f}')
        self.scale = scale
        self.image_scroll_area.setWidget(self.image_label)
        
    def load_images(self, filenames: str) -> None:
        self.images = []
        for f in filenames:
            pixmap = QPixmap(f)
            image = {
                'path': f,
                'pixmap': pixmap
            }
            self.images.append(image)

    def load_raw_data(self, filenames: List[str]) -> None:
        self.images = []
        image_maker = ImageMaker()
        for f in filenames:
            metadata = image_maker.get_file_metadata(f)
            print(f, metadata)
            raw_data = image_maker.read_file_new(f, ';', metadata['header'])
            image = image_maker.create_image_new(raw_data, metadata['mode'])
            print(image, image.format(), image.hasAlphaChannel())
            image = QImage(image)
            print(image, image.format(), image.hasAlphaChannel())
            # del raw_data

            # image = image.convertToFormat(QImage.Format.Format_RGB888, flags=Qt.ImageConversionFlag.ColorOnly)
            print(image)
            # image_new = QImage(image, image.size[0], image.size[1], QImage.Format_RGB888)
            # pixmap = QPixmap.fromImage(image)
            # print(pixmap)
            # self.images.append({'path': f, 'pixmap': pixmap, 'mode': metadata['mode']})
            self.images.append({'raw_data': raw_data, 'path': f, 'image': image, 'mode': metadata['mode']})

    def disable_scale_controls(self) -> None:
        self.scale_edit.setEnabled(False)
        self.increase_scale_button.setEnabled(False)
        self.decrease_scale_button.setEnabled(False)

    def _get_available_screen_size(self) -> tuple:
        available_geometry = QGuiApplication.primaryScreen().availableSize()
        width = available_geometry.width()
        height = available_geometry.height()
        return (width, height)

    def show_slideshow(self):
        self.disable_scale_controls()
        self.interval_widget.setVisible(True)
        self.interval_edit.setText(f'{int(self.slideshow_interval*1e-3)}')
        width, height = self._get_available_screen_size()
        self.resize(
            int(width*self.window_scale_factor),
            int(height*self.window_scale_factor)
        )

        for image in self.images:
            image['scale'] = self.choose_scale(
                image['pixmap'],
                width,
                height,
                self.window_scale_factor,
                self.image_scale_factor
            )
        
        if self.images:
            self.show_image(0)
            self.image_number = 1
            self.image_scroll_area.setWidget(self.image_label)

            self.timer.setInterval(self.slideshow_interval)
            self.timer.timeout.connect(lambda: self.show_images(self.images))
            self.timer.start()

    def show_image(self, image_number: int) -> None:
        self.setWindowTitle(self.images[image_number]['path'])
        self.scale_pixmap_new(
            self.images[image_number]['pixmap'],
            self.images[image_number]['scale']
        )
        self.scale_edit.setText(
            f'{self.images[image_number]["scale"]*100:.1f}'
        )

    def show_images(self, images):
        if self.image_number == len(images):
            self.image_number = 0
        # print(images[self.image_number]['path'])
        self.show_image(self.image_number)
        self.image_number += 1
            
    def change_interval(self):
        try:
            interval = int(float(self.interval_edit.text())*1e3)
            self.timer_interval = interval
            self.timer.setInterval(interval)
        except ValueError:
            self.interval_edit.setText(f'{float(self.timer_interval/1000):.1f}')

    def show_save_dialog(self):
        filename, ext = QFileDialog.getSaveFileName(
            self, 'Save file', '.', '*.png;;*.jpg;;*.bmp'
        )
        new_filename = f'{filename}.{ext[2:]}' 
        self.pixmap.save(new_filename, quality=-1)
        # print(new_filename)

    def show_open_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open Colormap', '.', '*.csv *.txt')
        print(filename)
        image_maker = ImageMaker()
        colormap = image_maker.read_file_new(filename, ',', 0)
        color_image = image_maker.apply_colormap_new(self.images[0]['raw_data'], colormap)
        pixmap = QPixmap.fromImage(color_image)
        self.scale_pixmap_new(pixmap, self.scale)

    def test_method(self, filename):
        image_maker = ImageMaker()
        raw_data = image_maker.read_file_new(filename, ';', 1)
        image_csv = image_maker.create_image_new(raw_data, 'RGB')
        qimage = QImage(image_csv)
        try:
            self.images_data.append({'path': filename, 'qimage': qimage, 'raw_data': raw_data})
        except AttributeError:
            self.images_data = [{'path': filename, 'qimage': qimage, 'raw_data': raw_data}]

        print(qimage, qimage.size(), self.images_data[-1]['qimage'], self.images_data[-1]['qimage'].size())
        qimage = self.images_data[-1]['qimage'].scaled(int(qimage.width()*1), int(qimage.height()*1))
        print(qimage, qimage.size(), self.images_data[-1]['qimage'], self.images_data[-1]['qimage'].size())
        # qimage = self.qimage.scaled(int(qimage.width()*4), int(qimage.height()*4))
        # qimage = self.qimage.scaledToWidth(int(qimage.width()*4))
        self.image_label.setPixmap(QPixmap(qimage))
        self.image_scroll_area.setWidget(main_window.image_label)

    #===========================================================+++++++

    def test_load_file(self, filename):
        self.image_label.setText(f'Loading {filename}')
        image_maker = ImageMaker()
        raw_data = image_maker.read_file_new(filename, ';', 1)
        image_csv = image_maker.create_image_new(raw_data, 'RGB')
        qimage = QImage(image_csv)
        qimage = qimage.convertToFormat(QImage.Format.Format_RGB888, flags=Qt.ImageConversionFlag.ColorOnly)
        self.qimage = qimage
        self.qfilename = filename
        del qimage
        qimage = self.qimage.scaled(int(self.qimage.width()*1), int(self.qimage.height()*1))
        print(qimage, qimage.size(), self.qimage, self.qimage.size())
        self.image_label.setPixmap(QPixmap(qimage))
        self.image_scroll_area.setWidget(self.image_label)

    def test_load_csv_file(self, filename):
        image_maker = ImageMaker()
        metadata = image_maker.get_file_metadata_new(filename)

        raw_data = image_maker.read_csv_file(filename, ';', metadata['skiprows'])
        image_csv = image_maker.create_imageqt(raw_data, metadata['mode'])
        # image_csv = image_maker.create_image_new(raw_data, 'RGB')
        qimage = QImage(image_csv)
        qimage = qimage.convertToFormat(QImage.Format.Format_RGB888, flags=Qt.ImageConversionFlag.ColorOnly)
        self.qimage = qimage
        self.qfilename = filename
        del qimage

    def test_scale_qimage(self, scale):
        if scale != 1:
            scaled_qimage = self.qimage.scaled(
                int(self.qimage.width()*scale),
                int(self.qimage.height()*scale),
                transformMode=Qt.TransformationMode.FastTransformation
            )
            return scaled_qimage
        else:
            return self.qimage

    def test_load_qimage_to_label(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        del pixmap

    def test_load_csv_to_label(self, filename, scale):
        self.test_load_csv_file(filename)
        qimage = self.test_scale_qimage(scale)
        self.test_load_qimage_to_label(qimage)
        del qimage
        self.image_scroll_area.setWidget(self.image_label)
        self.resize(1200, 800)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = ChildWindow()
    FILENAMES = [
        './colormap_beam.png',
        './colormap_big.png',
        './grayscale_test.png'
    ]
    # FILENAMES = []
    # main_window.load_image('./grayscale_test.png')
    # main_window.load_images(FILENAMES)
    # main_window.show_slideshow()
    # main_window.show_single_image()
    # main_window.show_slideshow(
    #     [
    #         './image1.jpg',
    #         './image2.png',
    #         './grayscale_test.png'
    #     ]
    # )
    CSVs = [
        './task/attached_data/for_extra_task/test_rgb.csv',
        './task/attached_data/for_extra_task/beam_rgb.csv',
        './task/attached_data/for_extra_task/atom_rgb.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_rgb.csv',
        './task/attached_data/for_extra_task/atom_grayscale.csv',
        './task/attached_data/for_extra_task/beam_grayscale.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_grayscale.csv'
    ]
    # sys.exit(app.exec())

    main_window.show()
    print('Load window')
    # time.sleep(1)
    print('Timeout')
    main_window.image_label.setText('Yo!')
    main_window.test_load_csv_to_label(CSVs[1], 1)
    main_window.image_scroll_area.setWidget(main_window.image_label)
    # main_window.test_method(CSVs[5])

    # main_window.test_load_file(CSVs[5])
    # image_maker = ImageMaker()
    # raw_data = image_maker.read_file_new(CSVs[1], ';', 1)
    # image_csv = image_maker.create_image_new(raw_data, 'RGB')
    # qimage = QImage(image_csv)
    # qimage = qimage.scaled(5000, 5000)
    # print(qimage)
    # main_window.image_label.setPixmap(QPixmap(qimage))
    # main_window.image_scroll_area.setWidget(main_window.image_label)
    # main_window.load_raw_data([CSVs[1]])
    # main_window.show_single_image()
    sys.exit(app.exec())
