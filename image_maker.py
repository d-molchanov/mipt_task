"""Module contains class ImageMaker for reading
csv-files and QImage objects creation
"""

import os
from typing import Optional
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

    def open_file(func):
        """Decorator for save file opening
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            filename = args[1]
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                logging.error('File not found: %s.', filename)
            except PermissionError:
                logging.error('Permission denied: %s.', filename)
            except UnicodeDecodeError as e:
                logging.error('Error with reading file %s: %s.', filename, e)
        return wrapper

    def get_file_mode_new(self, line: str) -> dict:
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
        else:
            return {'mode': 'L', 'skiprows': 0}

    @open_file
    def get_file_metadata_new(self, filename: str) -> Optional[dict]:
        """Method for obtain metadata of image from csv-file:
        image type and header presents
        """
        with open(filename, 'r') as f:
            return self.get_file_mode_new(f.readline())

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
                logging.error('!%s', e)
        return data

    def get_data_for_rgb_image(self, data: np.ndarray):
        """!Method for convert 24bit-integer ndarray to rgb-image """
        red = (data >> 16) & 0xFF
        green = (data >> 8) & 0xFF
        blue = data & 0xFF
        return np.stack((red, green, blue), axis=-1).astype(np.uint8)

    def create_imageqt(
        self, data: Optional[np.ndarray], mode_: str
    ) -> Optional[ImageQt]:
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
        return ImageQt(image)
        # return image

    def apply_colormap_new(
        self, data: np.ndarray, colormap: np.ndarray
    ) -> PilImage:
        """Method for colormap appling on grayscale image"""
        try:
            image = Image.fromarray(data.astype(np.uint8), mode='P')
        except ValueError:
            logging.error(
                'Check the delimeter in source file: it should be `,`.'
            )
        palette = list(colormap.flat)
        image.putpalette(palette)
        return ImageQt(image)

    def save_image(self, image: PilImage, filename: str) -> None:
        """Method for saving QImage-object to the file"""
        try:
            image.save(filename)
            logging.info('Image was saved to file: %s', filename)
        except ValueError:
            logging.error(
                'Image type is unknown. Please, check file extention: %s',
                filename
            )
        except IOError:
            logging.error('Cannot write to file: %s.', filename)


def test():
    FILENAMES = [
        './task/attached_data/for_extra_task/test_rgb.csv',
        './task/attached_data/for_extra_task/beam_rgb.csv',
        './task/attached_data/for_extra_task/atom_rgb.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_rgb.csv',
        './task/attached_data/for_extra_task/atom_grayscale.csv',
        './task/attached_data/for_extra_task/beam_grayscale.csv',
        './task/attached_data/for_extra_task/big_pic-7680x4320_grayscale.csv',
        './task/attached_data/colormap/CET-R1.csv'
    ]
    TEST_SCV = [
        './test_cases/grayscale_with_wrong_header.csv',
        './test_cases/rgb.csv',
        './test_cases/rgb_with_wrong_header.csv',
        './test_cases/rgb_without_header.csv',
        './test_cases/permission_denied.csv',
        './test_cases/not_exists.csv',
        './test_cases/not_rectangular.csv',
        './test_cases/not_csv.csv',
        './test_cases/grayscale.csv',
        './test_cases/empty.csv',
        './test_cases/different_separator.csv'

    ]
    filename = FILENAMES[-1]
    image_maker = ImageMaker()
    # data = image_maker.get_file_metadata(filename)
    # print(data)
    # for i, filename in enumerate(FILENAMES[2:3]):
    for i, filename in enumerate(TEST_SCV[1:2]):
        # print(f'\n{i+1}. Parsing %(filename)s')
        metadata = image_maker.get_file_metadata_new(filename)
        if metadata:
            raw_data = image_maker.read_csv_file(
                # filename, ';', metadata['skiprows']
                os.path.abspath(filename), ';', metadata['skiprows']
            )
            # logging.debug(f'Raw data:\n{raw_data}')
            imageqt = image_maker.create_imageqt(raw_data, metadata['mode'])
            if imageqt:
                image_maker.save_image(imageqt, f'{filename[:-4]}.png')
                pass


if __name__ == '__main__':
    test()
