
from pathlib import Path
from pictop.model.formats import Format
from datetime import datetime
from cached_property import cached_property
import typing


def get_exif_value(exif, key, convert=None, default=None):
    if not exif:
        return default

    undefined = object()
    value = exif.get(key, undefined)

    if value is undefined:
        return default

    if convert:
        value = convert(value)

    return value


class Photo:
    def __init__(self, path):
        # todo: dummy file tree structure mode support
        self.path = path if isinstance(path, Path) else Path(path)
        assert self.path.is_file()
        self.hash = None
        self.prev_paths = []
        self.related = []

    @cached_property
    def exif(self) -> dict:
        fmt = self.file_format
        driver = fmt and fmt.exif_driver
        return driver and driver.exif_load(self.path)

    @cached_property
    def file_format(self) -> Format:
        return Format.cast(self.path)

    @property
    def is_raw(self) -> bool:
        fmt = self.file_format
        return fmt and fmt.is_raw

    def __str__(self):
        return f'<{self.path}: [{"R" if self.is_raw else ""}]>'

    @cached_property
    def stat(self):
        return self.path.stat()

    @property
    def file_time_modify(self) -> datetime:
        return datetime.fromtimestamp(self.stat.st_mtime)

    @property
    def file_time_create(self) -> datetime:
        return datetime.fromtimestamp(self.stat.st_ctime)

    @property
    def file_time_access(self) -> datetime:
        return datetime.fromtimestamp(self.stat.st_atime)

    @property
    def file_size(self) -> int:
        return self.stat.st_size

    @property
    def file_inode(self) -> int:
        return self.stat.st_ino

    @property
    def file_hardlinks_count(self) -> int:
        return self.stat.st_nlink

    @property
    def exif_date(self) -> typing.Optional[datetime]:
        exif = self.exif
        if not exif:
            return

        driver = self.file_format.exif_driver
        dt = exif.get(driver.DATETIME_TAG_NAME, None)
        dt = dt and dt.values and datetime.strptime(dt.values, driver.DATETIME_FORMAT)
        return dt
