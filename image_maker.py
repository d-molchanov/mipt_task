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

    image_maker = ImageMaker()
    raw_data = image_maker.read_file(FILENAME)
    image = image_maker.create_grayscale_image(raw_data)
    image_maker.save_image(image, 'grayscale_test.png')
    # image.show()
    print(raw_data[0])

if __name__ == '__main__':
    main()