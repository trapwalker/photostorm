
from enum import Enum
import os
import logging

from .exif_driver import DEFAULT_EXIF_DRIVER


log = logging.getLogger(__name__)


class Format(Enum):
    _3fr = ('.3fr', True, ('Hasselblad',))
    r3d = ('.r3d', True, ('RED Digital Cinema',))
    ari = ('.ari', True, ('Arri_Alexa',))
    arw = ('.arw', True, ('Sony',))
    bay = ('.bay', True, ('Casio',))
    cap = ('.cap', True, ('Phase_One',))
    cr2 = ('.cr2', True, ('Canon',))
    cr3 = ('.cr3', True, ('Canon',))
    cri = ('.cri', True, ('Cintel',))
    crw = ('.crw', True, ('Canon',))
    dcr = ('.dcr', True, ('Kodak',))
    dcs = ('.dcs', True, ('Kodak',))
    dng = ('.dng', True, ('Adobe', 'Leica',))
    drf = ('.drf', True, ('Kodak',))
    eip = ('.eip', True, ('Phase_One',))
    erf = ('.erf', True, ('Epson',))
    fff = ('.fff', True, ('Imacon/Hasselblad raw',))
    iiq = ('.iiq', True, ('Phase_One',))
    k25 = ('.k25', True, ('Kodak',))
    kdc = ('.kdc', True, ('Kodak',))
    mdc = ('.mdc', True, ('Minolta, Agfa',))
    mef = ('.mef', True, ('Mamiya',))
    mos = ('.mos', True, ('Leaf',))
    mrw = ('.mrw', True, ('Minolta, Konica Minolta',))
    nef = ('.nef', True, ('Nikon',), DEFAULT_EXIF_DRIVER)
    nrw = ('.nrw', True, ('Nikon',))
    orf = ('.orf', True, ('Olympus',))
    pef = ('.pef', True, ('Pentax',))
    ptx = ('.ptx', True, ('Pentax',))
    pxn = ('.pxn', True, ('Logitech',))
    raf = ('.raf', True, ('Fuji',))
    raw = ('.raw', True, ('Leica', 'Panasonic',))
    rw2 = ('.rw2', True, ('Panasonic',))
    rwl = ('.rwl', True, ('Leica',))
    rwz = ('.rwz', True, ('Rawzor',))
    sr2 = ('.sr2', True, ('Sony',))
    srf = ('.srf', True, ('Sony',))
    srw = ('.srw', True, ('Samsung',))
    x3f = ('.x3f', True, ('Sigma',))

    jpeg = ('.jpeg', False, ('JPEG',), DEFAULT_EXIF_DRIVER,   None, '*.jpeg|*.jpg', 'image/jpeg')
    jpg  = ('.jpg',  False, ('JPEG',), DEFAULT_EXIF_DRIVER, 'jpeg', '*.jpeg|*.jpg', 'image/jpeg')
    tiff = ('.tif',  False, ('TIFF',), DEFAULT_EXIF_DRIVER,   None, '*.tiff|*.tif', 'image/tiff')
    webp = ('.webp', False, ('WebP',), DEFAULT_EXIF_DRIVER,   None, '*.webp',       'image/webp')

    def __init__(
        self,
        ext: str,
        is_raw: bool,
        vendors: tuple,
        exif_driver=None,
        main_alias=None,
        mask: str = None,
        mime=None,
    ):
        self.ext = ext
        self.is_raw = is_raw
        self.vendors = vendors
        self.main_alias = getattr(type(self), main_alias) if main_alias else None
        self.mask = mask or self.ext
        self.exif_driver = exif_driver
        self.mime = mime
        all_formats = getattr(type(self), '_ALL', None)
        if all_formats is None:
            all_formats = type(self)._ALL = {}

        all_formats[ext] = self

    @property
    def name(self):
        return self._name or '; '.join(self.vendors) or self.ext

    @classmethod
    def cast(cls, find_by, case_sens=False) -> 'Format':
        if hasattr(find_by, 'suffix'):  # pathlib.Path support
            ext = find_by.suffix
        elif find_by.startswith('.'):
            ext = find_by
        else:
            ext = os.path.splitext(find_by)[-1]

        if not case_sens:
            ext = ext.lower()

        return cls._ALL.get(ext, None)

    @classmethod
    def cast_general(cls, find_by, case_sens=False) -> 'Format':
        fmt = cls.cast(find_by, case_sens=case_sens)
        return fmt and fmt.main_alias or fmt


BASIC_FORMATS = {Format.jpeg, Format.nef, Format.raw}
