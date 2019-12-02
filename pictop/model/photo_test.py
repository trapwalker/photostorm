import unittest
from pictop.model.photo import Photo
from pprint import pprint as pp


class MyTestCase(unittest.TestCase):
    def test_something(self):
        j = Photo('../tests/data/nikon_d850_09.jpg')
        r = Photo('../tests/data/nikon_d850_09.nef')
        self.assertEqual(r.exif['Image DateTime'].printable, j.exif['Image DateTime'].printable)
        pp(j.exif)



if __name__ == '__main__':
    unittest.main()
