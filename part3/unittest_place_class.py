#!/usr/bin/env python3

from app.api.exceptions import BadRequest
from app.models.place import Place, User
import unittest

class TestPlaceClass(unittest.TestCase):
    def setUp(self):
        an_owner = User("John", "Doe", "john.doe@example.com")
        self.owner = an_owner
        pass


    def test_create_place(self):
        """
        Test to create place

        :param self: instance of the class
        """
        try:
            Place("Cozy Apartment", "A nice place to stay", 100.0, 37.7749, -122.4194, self.owner)
            self.assertTrue(True)
        except Exception:
            return self.assertTrue(False)
        
    def test_bad_name_too_short(self):
        """
        Test place with too short name
        """
        try:
            Place("Ap", "A nice place to stay", 100.0, 37.7749, -122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_price_negative(self):
        """
        Test place with negative price
        """
        try:
            Place("Cozy Apartment", "Nice place", -10.0, 37.7749, -122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_price_bool(self):
        """
        Test place with negative price
        """
        try:
            Place("Cozy Apartment", "Nice place", True, 37.7749, -122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_price_not_number(self):
        """
        Test place with non numeric price
        """
        try:
            Place("Cozy Apartment", "Nice place", "one hundred", 37.7749, -122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_latitude_out_of_range_minus(self):
        """
        Test place with invalid latitude
        """
        try:
            Place("Cozy Apartment", "Nice place", 100.0, -120.0, -122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_latitude_out_of_range_plus(self):
        """
        Test place with invalid latitude
        """
        try:
            Place("Cozy Apartment", "Nice place", 100.0, 120.0, 122.4194, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_bad_longitude_out_of_range_minus(self):
        """
        Test place with invalid longitude
        """
        try:
            Place("Cozy Apartment", "Nice place", 100.0, 37.7749, -200.0, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)
    
    def test_bad_longitude_out_of_range_plus(self):
        """
        Test place with invalid longitude
        """
        try:
            Place("Cozy Apartment", "Nice place", 100.0, 37.7749, 200.0, self.owner)
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)



    def test_bad_owner_none(self):
        """
        Test place with no owner
        """
        try:
            Place("Cozy Apartment", "Nice place", 100.0, 37.7749, -122.4194, None)
        except AttributeError:
            return self.assertTrue(True)

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()