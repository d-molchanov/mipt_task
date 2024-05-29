import numpy as np

class DataReader:

    def read_file(self, filename):
        data = np.genfromtxt(filename, delimiter=';', dtype=None)  
        print([len(line) for line in data])
        print(len(data))     

def main():
    FILENAME = 'atom.csv'

    dr = DataReader()
    dr.read_file(FILENAME)

if __name__ == '__main__':
    main()