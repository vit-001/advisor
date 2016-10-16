__author__ = 'Nikitin'

from os import listdir


class FileSeries:
    def __init__(self, path, file_prefix, file_suffix):
        files = listdir(path)
        self.file_list = list()
        for item in files:
            if item.endswith(file_suffix) and item.startswith(file_prefix):
                self.file_list.append(path + item)

    def iterator(self):
        for i in sorted(self.file_list):
            yield i


if __name__ == "__main__":
    f = FileSeries('files/v2.0/', '', '.uld')
    filenames = f.iterator()
    print(filenames.__next__())
    for i in filenames:
        print(i)
