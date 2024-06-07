from typing import Optional
from time import perf_counter
import functools
import logging
import numpy as np
import pandas as pd
import os

from PIL import Image
from PIL.Image import Image as PilImage
from PIL.ImageQt import ImageQt

from PyQt6.QtGui import QImage, QPixmap

logging.basicConfig(
    # format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    format='%(asctime)s %(levelname)s:\t%(message)s',
    level=logging.INFO
)

class ImageMaker:
    # def read_file(self, filename: str) -> Optional[np.ndarray]:
    #     data = None
    #     file_metadata = self.get_file_metadata(filename)
    #     try:
    #         with open(filename, 'r') as f:
    #             # data = np.genfromtxt(
    #             #     f, delimiter=';', dtype=None, encoding=None
    #             # )
    #             df = pd.read_csv(filename, sep=';', header=file_metadata['header'])
    #             data = df.values
    #     except FileNotFoundError:
    #         print(f'File not found: {filename}')
    #     except PermissionError:
    #         print(f'Permission denied: {filename}')
    #     except Exception as e:
    #         print(f'Error with reading file {filename}: {e}')
    #     return data

    

    # def read_file_new(self, filename: str, sep_: str, header_: int) -> dict:
    #     data = None
    #     try:
    #         with open(filename, 'r') as f:
    #             df = pd.read_csv(filename, sep=sep_, header=header_)
    #             data = df.values
    #     except FileNotFoundError:
    #         print(f'File not found: {filename}')
    #     except PermissionError:
    #         print(f'Permission denied: {filename}')
    #     except Exception as e:
    #         print(f'Error with reading file {filename}: {e}')
    #     return data

    # def apply_colormap(self, data, colormap):
    #     height = len(data)
    #     width = len(data[0])
    #     pixels = []
    #     for line in data:
    #         for value in line:
    #             pixels.append(tuple(colormap[value]))
    #     image = Image.new('RGB', (width, height))
    #     image.putdata(pixels)
    #     return image




    # def create_grayscale_image(self, data: np.ndarray) -> PilImage:
    #     height = len(data)
    #     width = len(data[0])
    #     image = Image.new('L', (width, height))
    #     image.putdata(list(data.flat))
    #     return image

    # def create_grayscale_image_new(self, data: np.ndarray) -> PilImage:
    #     image = Image.fromarray(data.astype(np.uint8), mode='L')
    #     return image

    def create_image_new(self, data: np.ndarray, mode_: str) -> Optional[PilImage]:
        if mode_ == 'L':
            image = Image.fromarray(data.astype(np.uint8), mode=mode_)
        if mode_ == 'RGB':
            data_ = data.astype(np.uint32)
            red = (data_ >> 16) & 0xFF
            green = (data_ >> 8) & 0xFF
            blue = data_ & 0xFF
            rgb_data = np.stack((red, green, blue), axis=-1).astype(np.uint8)
            image = Image.fromarray(rgb_data)
            # k = 0.5
            # image = image.resize((int(image.width * k), int(image.height*k)))
            # return image
        # print(image.mode, type(image), image)
        return ImageQt(image)

    # def create_color_image(self, data: np.ndarray) -> PilImage:
    #     height = len(data)
    #     width = len(data[0])
    #     pixels = []
    #     for line in data:
    #         for value in line:
    #             red = (value >> 16) & 0xff
    #             green = (value >> 8) & 0xff
    #             blue = value & 0xff
    #             pixels.append((red, green, blue))
    #     image = Image.new('RGB', (width, height))
    #     image.putdata(pixels)
    #     return image

    # def create_image(self, data: np.ndarray, format_: str) -> Optional[PilImage]:
    #     height = len(data)
    #     width = len(data[0])
    #     pixels = []
    #     if format_ == 'L':
    #         pixels = list(data.flat)
    #     elif format_ == 'RGB':
    #         for line in data:
    #             for value in line:
    #                 red = (value >> 16) & 0xff
    #                 green = (value >> 8) & 0xff
    #                 blue = value & 0xff
    #                 pixels.append((red, green, blue))
    #     else:
    #         return None
    #     image = Image.new(format_, (width, height))
    #     image.putdata(pixels)
    #     return image

    

    def open_file(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            filename = args[1]
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                logging.error(f'File not found: {filename}.')
            except PermissionError:
                logging.error(f'Permission denied: {filename}.')
            except UnicodeDecodeError as e:
                logging.error(f'Error with reading file {filename}: {e}.')
        return wrapper

    # def get_file_mode(self, line: str) -> dict:
    #     try:
    #         hash_symbol, mode = line.split()
    #     except ValueError:
    #         return {'mode': 'L', 'header': None}
    #     if hash_symbol != '#':
    #         return {'mode': 'L', 'header': None}
    #     if mode in {'grayscale', 'rgb'}:
    #         substitution = {'grayscale': 'L', 'rgb': 'RGB'}
    #         return {'mode': substitution[mode], 'header': 0}

    def get_file_mode_new(self, line: str) -> dict:
        # hash_symbol, mode = line.split()
        split_line = line.split()
        if len(split_line) >= 2:
            if split_line[0] == '#':
                substitution = {'grayscale': 'L', 'rgb': 'RGB'}
                return {'mode': substitution.get(split_line[1], None), 'skiprows': 1}
            return {'mode': None, 'skiprows': None}
        else:
            return {'mode': 'L', 'skiprows': 0}


    @open_file
    def get_file_metadata_new(self, filename: str) -> Optional[dict]:
        with open(filename, 'r') as f:
            return self.get_file_mode_new(f.readline())

    @open_file
    def read_csv_file(self, filename: str, sep_, skiprows_) -> Optional[np.ndarray]:
        data = None
        with open(filename, 'r') as f:
            try:
                time_start = perf_counter()
                logging.info(f'{filename}: start reading.')
                df = pd.read_csv(filename, sep=sep_, header=None, skiprows=skiprows_)
                data = df.values
                time_stop = f'{(perf_counter() - time_start)*1e3:.2f}'
                logging.info(
                    f'{filename} was read successfully in {time_stop} ms.'
                )
            except pd.errors.EmptyDataError as e:
                logging.error(f'Check {filename}: {e}.')
            except pd.errors.ParserError as e:
                logging.error(f'!{e}')
        return data

    def get_data_for_rgb_image(self, data: np.ndarray):
        red = (data >> 16) & 0xFF
        green = (data >> 8) & 0xFF
        blue = data & 0xFF
        return np.stack((red, green, blue), axis=-1).astype(np.uint8)

    def create_imageqt(self, data: Optional[np.ndarray], mode_: str) -> Optional[ImageQt]:
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
        except ValueError as e:
            logging.error('Check the delimeter in source file: it should be `;`.')
        try:    
            image = Image.fromarray(image_data, mode=mode_)
            time_stop = f'{(perf_counter() - time_start)*1e3:.2f}.'
            logging.info(
                f'ImageQt object was created in {time_stop} ms.'
            )
        except AttributeError as e:
            logging.error(f'ImageQt object cannot be created.')
        return ImageQt(image)
        # return image

    def apply_colormap_new(self, data: np.ndarray, colormap: np.ndarray) -> PilImage:
        try:
            image = Image.fromarray(data.astype(np.uint8), mode='P')
        except ValueError:
            logging.error('Check the delimeter in source file: it should be `,`.')
        palette = list(colormap.flat)
        image.putpalette(palette)
        return ImageQt(image)

    def save_image(self, image: PilImage, filename: str) -> None:
        try:
            image.save(filename)
            logging.info(f'Image was saved to file: {filename}')
        except ValueError:
            logging.error(f'Image type is unknown. Please, check file extention: {filename}')
        except IOError:
            logging.error(f'Cannot write to file: {filename}.')

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
        # print(f'\n{i+1}. Parsing {filename}')
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

def main():
    # FILENAME = './task/attached_data/for_main_task/atom.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_extra_task/atom_grayscale.csv'
    # FILENAME = './task/attached_data/for_extra_task/atom_rgb.csv'
    # FILENAME = './task/attached_data/for_extra_task/beam_rgb.csv'
    FILENAME = './task/attached_data/for_extra_task/big_pic-7680x4320_rgb.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_main_task/big_pic-7680x4320.csv'

    COLORMAP_FILENAME = './task/attached_data/colormap/CET-R1.csv'

    image_maker = ImageMaker()
    metadata = image_maker.get_file_metadata(FILENAME)
    raw_data = image_maker.read_file_new(FILENAME, ';', metadata['header'])
    image_csv = image_maker.create_image_new(raw_data, metadata['mode'])
    # image_csv.save('color_test.png')
    image_file = Image.open('color_test.png')
    print(image_csv, image_file, sep='\n')
    k = 2
    tst = perf_counter()
    image_csv_new = image_csv.resize((int(image_csv.width * k), int(image_csv.height*k)))
    print('Resize pil.image from csv:', perf_counter() - tst, image_csv_new)
    tst = perf_counter()
    image_file_new = image_file.resize((int(image_file.width * k), int(image_file.height*k)))
    print('Resize pil.image from png:', perf_counter() - tst, image_file_new)
    qimage_scv = ImageQt(image_csv)
    tst = perf_counter()
    qimage_scv_new = qimage_scv.scaled(int(image_file.width * k), int(image_file.height*k))
    print('Resize QImage from csv:', perf_counter() - tst, qimage_scv_new, qimage_scv_new.size())

    tst = perf_counter()
    qimage_file = ImageQt(image_file)
    qimage_file_new = qimage_file.scaled(int(image_file.width * k), int(image_file.height*k))
    print('Resize QImage from png:', perf_counter() - tst, qimage_file_new, qimage_file_new.size())

    tst = perf_counter()
    qimage = QImage(ImageQt(image_csv))
    pixmap = QPixmap(qimage)
    pixmap.new = pixmap.scaled(int(image_file.width * k), int(image_file.height*k))
    print(pixmap_new, pixmap_new.size(), perf_counter() - tst)

    raw_colormap_data = image_maker.read_file_new(COLORMAP_FILENAME, ',', 0)
    print(raw_colormap_data[0])
    print(raw_data[0])
    # # color_image = image_maker.apply_colormap_new(raw_data, raw_colormap_data)
    # # image_maker.save_image(color_image, 'colormap_beam.png')

    # image = image_maker.create_grayscale_image_new(raw_data)
    # # image = image_maker.create_color_image(raw_data)
    # # image = image_maker.create_image(raw_data, 'L')

    # image_maker.save_image(image, 'grayscale_test_big.png')
    # # image.show()
    # print(raw_data[0])
    # # print(raw_colormap_data[0])
    # # print(len(raw_colormap_data[0]))
    # # print(type(raw_colormap_data[0]))


if __name__ == '__main__':
    # main()
    test()
