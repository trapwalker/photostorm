
import pathlib

from .formats import BASIC_FORMATS, Format
from .photo import Photo


class Scanner:
    def __init__(self, formats=BASIC_FORMATS, case_sens=False):
        self.formats = formats
        self.case_sens = False

    def scan(self, path):
        path = pathlib.Path(path)
        for fp in path.glob('**/*'):
            fmt = Format.cast_general(fp, case_sens=self.case_sens)
            if fmt in self.formats:
                p = Photo(fp)
                print(p)
