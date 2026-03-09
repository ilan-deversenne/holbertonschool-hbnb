#!/usr/bin/env python3

from app.models.review import Review
import unittest

class TestReviewClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_text(self):
        try:
            Review("azertyyyy", 1, {},{})
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_bad_text(self):
        try:
            Review("azerty", 1, {},{})
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_rating(self):
        try:
            Review("azertyyyy", 2, {},{})
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_bad_rating(self):
        try:
            Review("azertyyyy", 0, {},{})
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_bad_rating(self):
        try:
            Review("azertyyyy", 6, {},{})
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
