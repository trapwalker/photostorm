
import logging

from cached_property import cached_property

log = logging.getLogger(__name__)


class ExifDriver:
    DATETIME_FORMAT = '%Y:%m:%d %H:%M:%S'
    DATETIME_TAG_NAME = 'Image DateTime'

    @cached_property
    def _lib(self):
        try:
            import exifread
            return exifread
        except ImportError:
            log.error("Can't import EXIF library: `exifread` library is not installed")

        return None

    def exif_read(self, file):
        lib = self._lib
        if not lib:
            return None

        try:
            return lib.process_file(file)
        except Exception as e:
            log.error("Can't read EXIF data: %s", e)

    def exif_load(self, file_path):
        if not self._lib:
            return None

        try:
            with open(file_path, 'rb') as f:
                return self.exif_read(f)
        except Exception as e:
            log.error("Can't load EXIF data: %s", e)


DEFAULT_EXIF_DRIVER = ExifDriver()
