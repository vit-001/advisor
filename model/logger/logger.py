# -*- coding: utf-8 -*-
__author__ = 'Vit'

class LogFile:
    def __init__(self, file, echo=False):
        self.file=file

    def out(self, string):
        self.file.write(string)

    def new_line(self):
        self.file.write('\n')

    def close(self):
        self.file.close()

class CsvLogFile(LogFile):
    def out_int(self, n):
        self.file.write("{0:d}; ".format(n))

    def out_float(self, value):
        self.file.write("{0:.8f}; ".format(value).replace('.', ','))

    def out_datatime(self, time):
        self.file.write(time.isoformat(' ') + '; ')

class Logger:
    def __init__(self, path, fname_prefix, fname_suffix):
        self.path = path
        self.prefix = fname_prefix
        self.suffix = fname_suffix

    def _new_file(self, filename,parameter_list=list()):
        p_string="p("
        for par in parameter_list:
            p_string+=par.__str__()+'_'
        p_string=p_string.rstrip('_')+')'
        fname = self.path + self.prefix +p_string+ filename + self.suffix
        file = open(fname, 'w')
        print("-----Logger: создан файл", fname)

        return file

    def new_file(self, filename,parameter_list=list()):
        return LogFile(self._new_file(filename,parameter_list))

    def new_csv_file(self, filename,parameter_list=list()):
        return CsvLogFile(self._new_file(filename,parameter_list))

if __name__ == "__main__":
    pass
