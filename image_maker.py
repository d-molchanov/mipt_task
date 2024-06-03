from typing import Optional

import numpy as np
import pandas as pd

from PIL import Image
from PIL.Image import Image as PilImage


class ImageMaker:
    def get_file_metadata(self, filename: str) -> Optional[str]:
        try:
            with open(filename, 'r') as f:
                try:
                    hash_symbol, file_type = f.readline().split()
                except ValueError:
                    return {'file_type': 'grayscale', 'header': 0}
                if hash_symbol != '#':
                    return {'file_type': 'grayscale', 'header': 0}
                if file_type in {'grayscale', 'rgb'}:
                    return {'file_type': file_type, 'header': 1}
        except FileNotFoundError:
            print(f'File not found: {filename}')
        except PermissionError:
            print(f'Permission denied: {filename}')
        except Exception as e:
            print(f'Error with reading file {filename}: {e}')

    def read_file(self, filename: str) -> Optional[np.ndarray]:
        data = None
        file_metadata = self.get_file_metadata(filename)
        try:
            with open(filename, 'r') as f:
                # data = np.genfromtxt(
                #     f, delimiter=';', dtype=None, encoding=None
                # )
                df = pd.read_csv(filename, sep=';', header=file_metadata['header'])
                data = df.values
        except FileNotFoundError:
            print(f'File not found: {filename}')
        except PermissionError:
            print(f'Permission denied: {filename}')
        except Exception as e:
            print(f'Error with reading file {filename}: {e}')
        return data

    def read_file_new(self, filename: str, sep_: str) -> dict:
        data = None
        try:
            with open(filename, 'r') as f:
                df = pd.read_csv(filename, sep=sep_, header=None)
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
        return image


    def create_grayscale_image(self, data: np.ndarray) -> PilImage:
        height = len(data)
        width = len(data[0])
        image = Image.new('L', (width, height))
        image.putdata(list(data.flat))
        return image

    def create_grayscale_image_new(self, data: np.ndarray) -> PilImage:
        image = Image.fromarray(data.astype(np.uint8), mode='L')
        return image

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
    FILENAME = './task/attached_data/for_extra_task/atom_rgb.csv'
    # FILENAME = './task/attached_data/for_extra_task/beam_rgb.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_main_task/big_pic-7680x4320.csv'

    COLORMAP_FILENAME = './task/attached_data/colormap/CET-R1.csv'

    image_maker = ImageMaker()
    print(image_maker.get_file_metadata(FILENAME))
    raw_data = image_maker.read_file(FILENAME)
    raw_colormap_data = image_maker.read_file_new(COLORMAP_FILENAME, ',')
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
