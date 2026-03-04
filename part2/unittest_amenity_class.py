#!/usr/bin/env python3

from app.models.amenity import Amenity
import unittest

class TestAmenityClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_name(self):
        try:
            Amenity("Wi-Fi")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_too_long_name(self):
        try:
            Amenity("Shorttttttttttttttttttttttttttttttttttttttttttttttt")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_too_short_name(self):
        try:
            Amenity("L")
            self.assertTrue(False)
        except:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
