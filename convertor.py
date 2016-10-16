# -*- coding: utf-8 -*-
__author__ = 'Nikitin'


class AbstractInputFile:
    pass


class AbstractOutputFile:
    pass


class Convertor:
    def __init__(self, input_file, output_file):
        pass

    def convert(self):
        pass


class InputV20(AbstractInputFile):
    pass


class OutputV21(AbstractOutputFile):
    pass


if __name__ == "__main__":
    inp = InputV20()
    out = OutputV21()
    conv = Convertor(inp, out)

    conv.convert()
