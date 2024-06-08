"""Module contains class ChildWindow for creating child windows"""
import sys
from time import perf_counter
from typing import List
from typing import Tuple
from typing import Optional

import logging

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QLabel


from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QImage

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

from child_window_design import ChildWindowDesign
from image_maker import ImageMaker


class ChildWindow(QMainWindow, ChildWindowDesign):
    """Class for creating child windows for displaying,
    scaling and saving images from csv-files
"""

    def __init__(self) -> None:
        super().__init__()

        self._timer = QTimer(self)
        self._timer_interval = 1000
        scale_step = 0.25
        self._slideshow_interval = 1000
        self._window_scale_factor = 0.9
        self._image_scale_factor = 0.9

        self._images_data: List[dict] = []
        self._active_image = 0
        self.increase_scale_button.clicked.connect(
            lambda: self._change_scale(scale_step)
        )
        self.decrease_scale_button.clicked.connect(
            lambda: self._change_scale(-scale_step)
        )
        self.scale_edit.editingFinished.connect(self._change_image)
        self.save_button.clicked.connect(self._show_save_dialog)
        self.interval_edit.editingFinished.connect(self._change_interval)
        self.load_colormap_button.clicked.connect(self._show_open_dialog)

    def _disable_scale_controls(self) -> None:
        """Method for disabling scale controls"""
        self.scale_edit.setEnabled(False)
        self.increase_scale_button.setEnabled(False)
        self.decrease_scale_button.setEnabled(False)

    def _get_available_screen_size(self) -> Tuple[int, int]:
        """Method for getting available screen size"""
        available_geometry = QGuiApplication.primaryScreen().availableSize()
        width = available_geometry.width()
        height = available_geometry.height()
        return (width, height)

    def _show_save_dialog(self) -> None:
        """Method for opening box dialog for saving QImage-object to file"""
        qimage = self._images_data[self._active_image]['image']
        filename, ext = QFileDialog.getSaveFileName(
            self, 'Save file', '.', '*.png;;*.jpg;;*.bmp'
        )
        if filename:
            new_filename = f'{filename}.{ext[2:]}'
            is_saved = qimage.save(new_filename)
            if is_saved:
                logging.info('Image was saved to file: %s', new_filename)
            else:
                logging.error('Cannot save image to file %s', new_filename)

    def _show_open_dialog(self) -> None:
        """Method for opening box dialog for load colormap from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open colormap', '.', '*.csv *.txt')
        if filename:
            image_maker = ImageMaker()
            metadata = image_maker.get_file_metadata(filename)
            colormap = image_maker.read_csv_file(
                filename, ',', metadata['skiprows']
            )
            color_qimage = image_maker.apply_colormap(
                self._images_data[self._active_image]['raw_data'], colormap
                )
            self._images_data[self._active_image]['image'] = color_qimage
            scaled_qimage = self.scale_qimage(
                color_qimage, self._images_data[self._active_image]['scale']
            )
            self.load_qimage_to_label(scaled_qimage, self.image_label)

    def _change_scale(self, value: float) -> None:
        """Method for changing active image scale"""
        entry = self._images_data[self._active_image]
        entry['scale'] += value
        if entry['scale'] <= 0.0:
            entry['scale'] = 0.01
        self.scale_edit.setText(f'{entry["scale"]*100.0:.1f}')
        self.scale_qimage_to_label(
            entry['image'], entry['scale'], self.image_label
        )

    def _change_image(self) -> None:
        """Method for scaling image via QLineEdit-object"""
        if not self._images_data:
            return None
        entry = self._images_data[self._active_image]
        try:
            entry['scale'] = float(self.scale_edit.text())/100.0
            if entry['scale'] <= 0:
                entry['scale'] = 0.01
            self.scale_qimage_to_label(
                entry['image'], entry['scale'], self.image_label
            )
        except ValueError:
            logging.error('Invalid scale value: %s', self.scale_edit.text())
        self.scale_edit.setText(f'{entry["scale"]*100:.1f}')

    def _change_interval(self) -> None:
        """Method for changing QTimer-object interval via QLineEdit-object"""
        try:
            interval = int(float(self.interval_edit.text())*1e3)
            self._timer_interval = interval
            self._timer.setInterval(interval)
        except ValueError:
            self.interval_edit.setText(
                f'{float(self._timer_interval/1000):.1f}'
            )

    def load_csv_files(self, filenames: List[str]) -> None:
        """Method for loading image data from csv-files"""
        image_maker = ImageMaker()
        for f in filenames:
            metadata = image_maker.get_file_metadata(f)
            if not metadata:
                continue
            if not metadata['mode']:
                continue
            raw_data = image_maker.read_csv_file(f, ';', metadata['skiprows'])
            qimage = image_maker.create_qimage(raw_data, metadata['mode'])
            if not qimage:
                continue
            self._images_data.append(
                {
                    'path': f,
                    'raw_data': raw_data,
                    'image': qimage,
                    'mode': metadata['mode']
                }
            )
            self._active_image = 0

    def show_slideshow(self) -> None:
        """Method for showing slideshow"""
        self.interval_widget.setVisible(True)
        self.interval_edit.setText(f'{int(self._slideshow_interval*1e-3)}')
        width, height = self._get_available_screen_size()
        self.resize(
            int(width*self._window_scale_factor),
            int(height*self._window_scale_factor)
        )

        for entry in self._images_data:
            entry['scale'] = self.choose_scale(
                entry['image'],
                width,
                height,
                self._window_scale_factor,
                self._image_scale_factor
            )

        if self._images_data:
            self.show_image(self._images_data, self._active_image)
            # self._active_image = 1
            self.image_scroll_area.setWidget(self.image_label)

            self._timer.setInterval(self._slideshow_interval)
            self._timer.timeout.connect(
                lambda: self.show_images(self._images_data)
            )
            self._timer.start()

    def show_image(self, images_data: List[dict], image_number: int) -> None:
        """Method for displaying image during a slideshow"""
        entry = images_data[image_number]
        self.setWindowTitle(entry['path'])
        self.scale_qimage_to_label(
            entry['image'], entry['scale'], self.image_label
        )
        self.scale_edit.setText(f'{entry["scale"]*100:.1f}')

    def show_images(self, images_data: List[dict]):
        """Method for displaying images in a loop"""
        self._active_image += 1
        if self._active_image == len(images_data):
            self._active_image = 0

        self.show_image(self._images_data, self._active_image)
        self.scale_edit.setText(
            f'{images_data[self._active_image]["scale"]*100:.1f}'
        )

    def scale_qimage(self, qimage: QImage, scale: float) -> QImage:
        """Method for scaling QImage-object"""
        if scale == 1:
            return qimage
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

    def load_qimage_to_label(self, qimage: QImage, label: QLabel) -> None:
        """Method for loading QImage-object to the QLabel-object"""
        label.setPixmap(QPixmap.fromImage(qimage))

    def choose_scale(
        self, qimage: QImage, width: int, height: int,
        window_scale_factor: float, image_scale_factor: float
    ) -> float:
        """Method for choosing scale of image to fit the application window"""
        window_width = width*window_scale_factor
        window_height = height*window_scale_factor

        k_w_image = window_width * image_scale_factor / qimage.width()
        k_h_image = window_height * image_scale_factor / qimage.height()
        k_min_image = min(k_w_image, k_h_image)
        if k_min_image >= 1.0:
            scale = 1.0
        else:
            scale = k_min_image
        return scale

    def get_single_image(self, image_number: int) -> Optional[QImage]:
        """Method for getting single image from self._images_data by number"""
        if not self._images_data:
            return None
        if image_number > len(self._images_data) - 1:
            return None
        return self._images_data[image_number]['image']

    def show_single_image(self, image_number: int) -> None:
        """Method for showing single image"""
        if not self._images_data:
            # self.image_label.setText('No data to show')
            return None
        if image_number > len(self._images_data) - 1:
            return None
        width, height = self._get_available_screen_size()
        entry = self._images_data[image_number]
        self.setWindowTitle(entry['path'])
        if entry['mode'] == 'L':
            self.load_colormap_button.setVisible(True)
        scale = self.choose_scale(
            entry['image'],
            width,
            height,
            self._window_scale_factor,
            self._image_scale_factor
        )
        entry['scale'] = scale
        if scale == 1.0:
            self.resize(
                int(entry['image'].width()/self._image_scale_factor),
                int(entry['image'].height()/self._image_scale_factor)
            )
        else:
            self.resize(
                int(width*self._window_scale_factor),
                int(height*self._window_scale_factor)
            )
        self.scale_qimage_to_label(
            entry['image'], entry['scale'], self.image_label
        )
        self.scale_edit.setText(f'{scale*100:.1f}')
        self.image_scroll_area.setWidget(self.image_label)

    def scale_qimage_to_label(self, qimage: QImage, scale: float, label: QLabel) -> None:
        """Method for scaling QImage-object and loading it to QLabel-object"""
        scaled_qimage = self.scale_qimage(qimage, scale)
        self.load_qimage_to_label(scaled_qimage, label)

    def closeEvent(self, e):
        """method to stop slideshow timer when window closes"""
        self._timer.stop()


def test() -> None:
    """Function for testing ChildWindow class methods"""
    app = QApplication(sys.argv)
    main_window = ChildWindow()
    test_files = [
        './test_cases/grayscale_with_wrong_header.csv',
        './test_cases/atom_rgb.csv',
        './test_cases/rgb_with_wrong_header.csv',
        './test_cases/rgb_without_header.csv',
        './test_cases/permission_denied.csv',
        './test_cases/not_exists.csv',
        './test_cases/not_rectangular.csv',
        './test_cases/not_csv.csv',
        './test_cases/atom_grayscale.csv',
        './test_cases/empty.csv',
        './test_cases/different_separator.csv'

    ]
    time_start = perf_counter()
    main_window.load_csv_files(test_files)

    time_stop = f'{(perf_counter() - time_start)*1e3:.2f}.'
    logging.info('Finished in %s ms.', time_stop)
    # main_window.show_single_image(0)
    main_window.show_slideshow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    test()
