from typing import Optional
from time import perf_counter
import numpy as np
import pandas as pd

from PIL import Image
from PIL.Image import Image as PilImage
from PIL.ImageQt import ImageQt

from PyQt6.QtGui import QImage, QPixmap

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

    def get_file_metadata(self, filename: str) -> Optional[str]:
        try:
            with open(filename, 'r') as f:
                try:
                    hash_symbol, mode = f.readline().split()
                except ValueError:
                    return {'mode': 'L', 'header': 0}
                if hash_symbol != '#':
                    return {'mode': 'L', 'header': 0}
                if mode in {'grayscale', 'rgb'}:
                    substitution = {'grayscale': 'L', 'rgb': 'RGB'}
                    return {'mode': substitution[mode], 'header': 1}
        except FileNotFoundError:
            print(f'File not found: {filename}')
        except PermissionError:
            print(f'Permission denied: {filename}')
        except Exception as e:
            print(f'Error with reading file {filename}: {e}')

    def read_file_new(self, filename: str, sep_: str, header_: int) -> dict:
        data = None
        try:
            with open(filename, 'r') as f:
                df = pd.read_csv(filename, sep=sep_, header=header_)
                data = df.values
        except FileNotFoundError:
            print(f'File not found: {filename}')
        except PermissionError:
            print(f'Permission denied: {filename}')
        except Exception as e:
            print(f'Error with reading file {filename}: {e}')
        return data

    def apply_colormap(self, data, colormap):
        height = len(data)
        width = len(data[0])
        pixels = []
        for line in data:
            for value in line:
                pixels.append(tuple(colormap[value]))
        image = Image.new('RGB', (width, height))
        image.putdata(pixels)
        return image

    def apply_colormap_new(self, data, colormap):
        image = Image.fromarray(data.astype(np.uint8), mode='P')
        palette = list(colormap.flat)
        image.putpalette(palette)
        return ImageQt(image)


    def create_grayscale_image(self, data: np.ndarray) -> PilImage:
        height = len(data)
        width = len(data[0])
        image = Image.new('L', (width, height))
        image.putdata(list(data.flat))
        return image

    def create_grayscale_image_new(self, data: np.ndarray) -> PilImage:
        image = Image.fromarray(data.astype(np.uint8), mode='L')
        return image

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

    def create_color_image(self, data: np.ndarray) -> PilImage:
        height = len(data)
        width = len(data[0])
        pixels = []
        for line in data:
            for value in line:
                red = (value >> 16) & 0xff
                green = (value >> 8) & 0xff
                blue = value & 0xff
                pixels.append((red, green, blue))
        image = Image.new('RGB', (width, height))
        image.putdata(pixels)
        return image

    def create_image(self, data: np.ndarray, format_: str) -> Optional[PilImage]:
        height = len(data)
        width = len(data[0])
        pixels = []
        if format_ == 'L':
            pixels = list(data.flat)
        elif format_ == 'RGB':
            for line in data:
                for value in line:
                    red = (value >> 16) & 0xff
                    green = (value >> 8) & 0xff
                    blue = value & 0xff
                    pixels.append((red, green, blue))
        else:
            return None
        image = Image.new(format_, (width, height))
        image.putdata(pixels)
        return image

    def save_image(self, image: PilImage, filename: str) -> None:
        try:
            image.save(filename)
        except ValueError:
            print('Image type is unknown. Please, check extention.')
        except IOError:
            print(f'Cannot write to file: {filename}')
        # img = Image.fromarray(raw_data)
        # img.save('grayscale_test.png')
        # img.show()


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
    main()
