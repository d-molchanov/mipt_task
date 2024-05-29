import numpy as np
from PIL import Image
# import matplotlib as mpl
# import matplotlib.pyplot as plt


class DataReader:

    def read_file(self, filename):
        data = np.genfromtxt(filename, encoding=None, delimiter=';', dtype=None)
        # print([len(line) for line in data])
        # print(len(data))
        print(data[0])
        return data

    def create_image(self, raw_data):
        height = len(raw_data)
        width = len(raw_data[0])
        img = Image.new('L', (width, height))
        img.putdata(list(raw_data.flat))
        # img = Image.fromarray(raw_data)
        img.save('grayscale_test.png')
        # img.show()

    def create_color_image(self, raw_data):
        height = len(raw_data)
        width = len(raw_data[0])
        pixels = []
        for line in raw_data:
            for value in line:
                red = (value >> 16) & 0xff
                green = (value >> 8) & 0xff
                blue = value & 0xff
                pixels.append((red, green, blue))
        img = Image.new('RGB', (width, height))
        img.putdata(pixels)
        img.save('test.bmp')
        # img = Image.fromarray(raw_data, mode='RGB')
        img.show()


def main():
    FILENAME = './task/attached_data/for_main_task/atom.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_extra_task/atom_rgb.csv'
    # FILENAME = './task/attached_data/for_main_task/beam.csv'
    # FILENAME = './task/attached_data/for_main_task/big_pic-7680x4320.csv'

    dr = DataReader()
    raw_data = dr.read_file(FILENAME)
    dr.create_image(raw_data)
    # dr.create_color_image(raw_data)

if __name__ == '__main__':
    main()