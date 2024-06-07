import sys
from time import perf_counter
from typing import List

import logging
from PIL import ImageQt

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QImage

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

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

        self.images_data = []
        self.active_image = 0
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
        entry = self.images_data[self.active_image]
        entry['scale'] += value
        if entry['scale'] <= 0.0:
            entry['scale'] = 0.01
        self.scale_edit.setText(f'{entry["scale"]*100.0:.1f}')
        qimage = self.convert_to_qimage(entry['image'])
        scaled_qimage = self.scale_qimage(qimage, entry['scale'])
        self.load_qimage_to_label(scaled_qimage, self.image_label)

    def change_image(self):
        entry = self.images_data[self.active_image]
        try:
            entry['scale'] = float(self.scale_edit.text())/100.0
            if entry['scale'] <= 0:
                entry['scale'] = 0.01
            qimage = self.convert_to_qimage(entry['image'])
            scaled_qimage = self.scale_qimage(qimage, entry['scale'])
            self.load_qimage_to_label(scaled_qimage, self.image_label)
        except ValueError:
            logging.error('Invalid scale value: %s', self.scale_edit.text())
        self.scale_edit.setText(f'{entry["scale"]*100:.1f}')

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
        # self.disable_scale_controls()
        self.interval_widget.setVisible(True)
        self.interval_edit.setText(f'{int(self.slideshow_interval*1e-3)}')
        width, height = self._get_available_screen_size()
        self.resize(
            int(width*self.window_scale_factor),
            int(height*self.window_scale_factor)
        )

        for entry in self.images_data:
            entry['scale'] = self.choose_scale(
                entry['image'],
                width,
                height,
                self.window_scale_factor,
                self.image_scale_factor
            )

        if self.images_data:
            print(len(self.images_data))
            self.show_image(self.images_data, self.active_image)
            # self.active_image = 1
            self.image_scroll_area.setWidget(self.image_label)

            self.timer.setInterval(self.slideshow_interval)
            self.timer.timeout.connect(
                lambda: self.show_images(self.images_data)
            )
            self.timer.start()

    def show_image(self, images_data, image_number) -> None:
        entry = images_data[image_number]
        self.setWindowTitle(entry['path'])
        qimage = self.convert_to_qimage(entry['image'])
        scaled_qimage = self.scale_qimage(qimage, entry['scale'])
        self.load_qimage_to_label(scaled_qimage, self.image_label)
        self.scale_edit.setText(f'{entry["scale"]*100:.1f}')
        # !add check for image mode

    def show_images(self, images_data):
        self.active_image += 1
        if self.active_image == len(images_data):
            self.active_image = 0

        self.show_image(self.images_data, self.active_image)
        self.scale_edit.setText(
            f'{images_data[self.active_image]["scale"]*100:.1f}'
        )

    def change_interval(self):
        try:
            interval = int(float(self.interval_edit.text())*1e3)
            self.timer_interval = interval
            self.timer.setInterval(interval)
        except ValueError:
            self.interval_edit.setText(
                f'{float(self.timer_interval/1000):.1f}'
            )

    def show_save_dialog(self):
        imageqt = self.images_data[self.active_image]['image']
        qimage = self.convert_to_qimage(imageqt)
        filename, ext = QFileDialog.getSaveFileName(
            self, 'Save file', '.', '*.png;;*.jpg;;*.bmp'
        )
        new_filename = f'{filename}.{ext[2:]}'
        qimage.save(new_filename)

    def show_open_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open colormap', '.', '*.csv *.txt')
        if filename:
            image_maker = ImageMaker()
            metadata = image_maker.get_file_metadata_new(filename)
            colormap = image_maker.read_csv_file(
                filename, ',', metadata['skiprows']
            )
            color_qimage = image_maker.apply_colormap_new(
                self.images_data[self.active_image]['raw_data'], colormap
                )
            self.images_data[self.active_image]['image'] = color_qimage
            scaled_qimage = self.scale_qimage(
                color_qimage, self.images_data[self.active_image]['scale']
            )
            self.load_qimage_to_label(scaled_qimage, self.image_label)
        # pixmap = QPixmap.fromImage(color_image)
        # self.scale_pixmap_new(pixmap, self.scale)

    def closeEvent(self, e):
        self.timer.stop()

    #===========================================================+++++++

    def load_csv_files(self, filenames: List[str]) -> None:
        image_maker = ImageMaker()
        for f in filenames:
            metadata = image_maker.get_file_metadata_new(f)
            raw_data = image_maker.read_csv_file(f, ';', metadata['skiprows'])
            imageqt = image_maker.create_imageqt(raw_data, metadata['mode'])
            self.images_data.append(
                {
                    'path': f,
                    'raw_data': raw_data,
                    'image': imageqt,
                    'mode': metadata['mode']
                }
            )
            self.active_image = 0

    def convert_to_qimage(self, imageqt) -> QImage:
        return QImage(imageqt).convertToFormat(
            QImage.Format.Format_RGB888,
            flags=Qt.ImageConversionFlag.ColorOnly
        )

    def scale_qimage(self, qimage, scale):
        if scale == 1:
            logging.info('Image does not need to be scaled: scale equals 100%')
            return qimage
        else:
            logging.info('Image scaling has started.')
            time_start = perf_counter()
            scaled_qimage = qimage.scaled(
                int(qimage.width()*scale),
                int(qimage.height()*scale),
                transformMode=Qt.TransformationMode.FastTransformation
            )
            time_stop = f'{(perf_counter() - time_start)*1e3:.2f}.'
            logging.info('Image scaling finished in %s ms.', time_stop)
            return scaled_qimage

    def load_imageqt_to_label(self, imageqt, label) -> None:
        label.setPixmap(
            QPixmap.fromImage(self.convert_to_qimage(imageqt))
        )

    def load_qimage_to_label(self, qimage, label) -> None:
        label.setPixmap(QPixmap.fromImage(qimage))

    def choose_scale(
        self, imageqt: ImageQt, width: int, height: int,
        window_scale_factor: float, image_scale_factor: float
    ) -> float:
        window_width = width*window_scale_factor
        window_height = height*window_scale_factor

        k_w_image = window_width * image_scale_factor / imageqt.width()
        k_h_image = window_height * image_scale_factor / imageqt.height()
        k_min_image = min(k_w_image, k_h_image)
        if k_min_image >= 1.0:
            scale = 1.0
        else:
            scale = k_min_image
        return scale

    def show_single_image_new(self, image_number) -> None:
        width, height = self._get_available_screen_size()
        print(width, height)
        entry = self.images_data[image_number]
        self.setWindowTitle(entry['path'])
        if entry['mode'] == 'L':
            self.load_colormap_button.setVisible(True)
        print(1)
        scale = self.choose_scale(
            entry['image'],
            width,
            height,
            self.window_scale_factor,
            self.image_scale_factor
        )
        print(2, scale)
        self.images_data[image_number]['scale'] = scale
        if scale == 1.0:
            self.resize(
                int(entry['image'].width()/self.image_scale_factor),
                int(entry['image'].height()/self.image_scale_factor)
            )
        else:
            self.resize(
                int(width*self.window_scale_factor),
                int(height*self.window_scale_factor)
            )
        print(3, entry['image'])
        # image['image'].save('without_scale.png')
        # print(4)
        qimage = self.convert_to_qimage(entry['image'])
        scaled_qimage = self.scale_qimage(qimage, scale)
        self.load_qimage_to_label(scaled_qimage, self.image_label)
        # self.image_label.setPixmap(QPixmap(scaled))
        # self.scale_pixmap_new(self.pixmap, scale)
        print(4)
        print(entry.keys())
        self.scale_edit.setText(f'{scale*100:.1f}')
        # self.scale = scale
        self.image_scroll_area.setWidget(self.image_label)


def test():
    app = QApplication(sys.argv)
    main_window = ChildWindow()
    CSVs = [
        './task/attached_data/for_extra_task/atom_grayscale.csv',
        './task/attached_data/for_extra_task/atom_rgb.csv',
        './task/attached_data/for_extra_task/test_rgb.csv',
        './task/attached_data/for_extra_task/beam_rgb.csv',
        './task/attached_data/for_extra_task/beam_grayscale.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_rgb.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_grayscale.csv'
    ]
    time_start = perf_counter()
    main_window.load_csv_files(CSVs[:-2])

    time_stop = f'{(perf_counter() - time_start)*1e3:.2f}.'
    logging.info('Finished in %s ms.', time_stop)
    # entry = main_window.images_data[-1]
    # main_window.show_single_image_new(0)
    main_window.show_slideshow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    test()
