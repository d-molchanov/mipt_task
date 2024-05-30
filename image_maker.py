from typing import List, Tuple, Dict, Optional, Union

import numpy as np

from PIL import Image



class ImageMaker:
    def read_file(self, filename: str) -> Optional[np.ndarray]:
        data = None
        try:
            with open(filename, 'r') as f:
                data = np.genfromtxt(
                    f, delimiter=';', dtype=None, encoding=None 
                )
                return data
        except FileNotFoundError:
            print(f'File not found: {filename}')
        except PermissionError:
            print(f'Permission denied: {filename}')
        except Exception as e:
            print(f'Error with reading file {filename}: {e}')
        return data

    def create_grayscale_image(self, data: np.ndarray) -> Image:
        height = len(data)
        width = len(data[0])
        image = Image.new('L', (width, height))
        image.putdata(list(data.flat))
        return image

    def create_color_image(self, data: np.ndarray) -> Image:
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

    def create_image(self, data: np.ndarray, format_: str) -> Optional[Image]:
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

    def save_image(self, image: Image, filename: str) -> None:
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
    FILENAME = './task/attached_data/for_main_task/atom.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_extra_task/atom_rgb.csv'
    # FILENAME = './task/attached_data/for_extra_task/beam_rgb.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_main_task/big_pic-7680x4320.csv'

    image_maker = ImageMaker()
    raw_data = image_maker.read_file(FILENAME)
    # image = image_maker.create_grayscale_image(raw_data)
    # image = image_maker.create_color_image(raw_data)
    image = image_maker.create_image(raw_data, 'L')

    image_maker.save_image(image, 'grayscale_test.png')
    # image.show()
    print(raw_data[0])

if __name__ == '__main__':
    main()