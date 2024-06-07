"""Module contains class ImageMaker for reading
csv-files and creating QImage-objects
"""

import os
from typing import Optional, Callable, Union
from time import perf_counter
import functools
import logging
import numpy as np
import pandas as pd

from PIL import Image
from PIL.Image import Image as PilImage
from PIL.ImageQt import ImageQt

from PyQt6.QtGui import QImage


logging.basicConfig(
    format='%(asctime)s %(levelname)s:\t%(message)s',
    level=logging.INFO
)


class ImageMaker:
    """Class for reading csv-files and transforming them to
    QImage-objects
    """

    def open_file(func: Callable) -> Optional[Union[dict, np.ndarray]]:
        """Decorator for save file opening
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            filename = args[1]
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                logging.error('File not found: %s.', filename)
                return None
            except PermissionError:
                logging.error('Permission denied: %s.', filename)
                return None
            except UnicodeDecodeError as e:
                logging.error('Error with reading file %s: %s.', filename, e)
                return None
        return wrapper

    def _get_file_mode(self, line: str) -> dict:
        """Method for determine type of image, which
        is contained in csv-file
        """
        split_line = line.split()
        if len(split_line) >= 2:
            if split_line[0] == '#':
                substitution = {'grayscale': 'L', 'rgb': 'RGB'}
                return {
                    'mode': substitution.get(split_line[1], None),
                    'skiprows': 1
                }
            return {'mode': None, 'skiprows': None}
        return {'mode': 'L', 'skiprows': 0}

    @open_file
    def get_file_metadata(self, filename: str) -> Optional[dict]:
        """Method for obtain metadata of image from csv-file:
        image type and header presents
        """
        with open(filename, 'r') as f:
            return self._get_file_mode(f.readline())

    @open_file
    def read_csv_file(
        self, filename: str, sep_, skiprows_
    ) -> Optional[np.ndarray]:
        """Method for reading of csv-file"""
        data = None
        with open(filename, 'r') as f:
            try:
                time_start = perf_counter()
                logging.info('%s: start reading.', filename)
                df = pd.read_csv(
                    f, sep=sep_, header=None, skiprows=skiprows_
                    # filename, sep=sep_, header=None, skiprows=skiprows_
                )
                data = df.values
                time_stop = f'{(perf_counter() - time_start)*1e3:.2f}'
                logging.info(
                    '%s was read successfully in %s ms.',
                    filename,
                    time_stop
                )
            except pd.errors.EmptyDataError as e:
                logging.error('Check %s: %s.', filename, e)
            except pd.errors.ParserError as e:
                logging.error('Check %s: %s.', filename, e)
        return data

    def get_data_for_rgb_image(self, data: np.ndarray) -> np.ndarray:
        """Method for converting a 24-bit integer NumPy array to RGB image"""
        red = (data >> 16) & 0xFF
        green = (data >> 8) & 0xFF
        blue = data & 0xFF
        return np.stack((red, green, blue), axis=-1).astype(np.uint8)

    def convert_to_qimage(self, pilimage, format_: str) -> Optional[QImage]:
        """Method for converting PIL.Image object to QImage object"""
        if format_ == 'RGB':
            return QImage(pilimage).convertToFormat(
                QImage.Format.Format_RGB888,
            )
        if format_ == 'L':
            return QImage(pilimage).convertToFormat(
                QImage.Format.Format_Grayscale8
            )
        return None

    def create_qimage(
        self, data: Optional[np.ndarray], mode_: str
    ) -> Optional[QImage]:
        """Method for QImage-object creation"""
        if data is None:
            return None
        if pd.isna(data).any():
            logging.error('Sourse file contains NaN values.')
            return None
        image_data = None
        image = None
        time_start = perf_counter()
        logging.info('ImageQt object creation was started.')
        try:
            if mode_ == 'L':
                image_data = data.astype(np.uint8)
            if mode_ == 'RGB':
                image_data = self.get_data_for_rgb_image(
                    data.astype(np.uint32)
                )
        except ValueError:
            logging.error(
                'Check the delimeter in source file: it should be `;`.'
            )
        try:
            image = Image.fromarray(image_data, mode=mode_)
            time_stop = f'{(perf_counter() - time_start)*1e3:.2f}.'
            logging.info('ImageQt object was created in %s ms.', time_stop)
        except AttributeError:
            logging.error('ImageQt object cannot be created.')
        if mode_:
            return self.convert_to_qimage(ImageQt(image), mode_)
        return None

    def apply_colormap(
        self, data: np.ndarray, colormap: np.ndarray
    ) -> Optional[QImage]:
        """Method for colormap appling on grayscale image"""
        try:
            image = Image.fromarray(data.astype(np.uint8), mode='P')
        except ValueError:
            logging.error(
                'Check the delimeter in source file: it should be `,`.'
            )
        palette = list(colormap.flat)
        image.putpalette(palette)
        return self.convert_to_qimage(ImageQt(image), 'RGB')

    def save_image(self, image: PilImage, filename: str) -> None:
        """Method for saving QImage-object to the file"""
        is_saved = image.save(filename)
        if is_saved:
            logging.info('Image was saved to file: %s', filename)
        else:
            logging.error('Cannot save image to file %s', filename)


def test():
    """Function for testing ImageMaker class methods"""
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
    image_maker = ImageMaker()
    for filename in test_files:
        metadata = image_maker.get_file_metadata(filename)
        if metadata:
            raw_data = image_maker.read_csv_file(
                os.path.abspath(filename), ';', metadata['skiprows']
            )
            qimage = image_maker.create_qimage(raw_data, metadata['mode'])
            if qimage:
                image_maker.save_image(qimage, f'{filename[:-4]}.png')


if __name__ == '__main__':
    test()
