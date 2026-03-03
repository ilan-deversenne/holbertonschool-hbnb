#!/usr/bin/env python3

from app.api.exceptions import BadRequest
from app.models.user import User
import unittest

class TestUserClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        """
        Test to create user

        :param self: instance of the class
        """
        try:
            User("John", "Doe", "john.doe@example.com")
            self.assertTrue(True)
        except Exception:
            return self.assertTrue(False)

    def test_create_bad_user(self):
        """
        Test to create user with bad first_name

        :param self: instance of the class
        """
        try:
            User("Jo", "Doe", "john.doe@example.com")
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_create_bad_user2(self):
        """
        Test to create user with bad last_name

        :param self: instance of the class
        """
        try:
            User("John", "Do", "john.doe@example.com")
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_create_bad_user3(self):
        """
        Test to create user with bad email

        :param self: instance of the class
        """
        try:
            User("John", "Doe", "invalid-email")
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_create_bad_user4(self):
        """
        Test to create user with too long first_name

        :param self: instance of the class
        """
        try:
            User("Johnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn", "Doe", "invalid-email")
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_create_bad_user5(self):
        """
        Test to create user with too long last_name

        :param self: instance of the class
        """
        try:
            User("John", "Doeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "invalid-email")
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_update_with_bad_firstname(self):
        """
        Test to create user and update first_name with bad first_name

        :param self: instance of the class
        """
        user = User("John", "Doe", "john.doe@example.com")

        try:
            user.first_name = "aa"
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_update_with_bad_lastname(self):
        """
        Test to create user and update last_name with bad last_name

        :param self: instance of the class
        """
        user = User("John", "Doe", "john.doe@example.com")

        try:
            user.last_name = "   "
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

    def test_update_with_bad_email(self):
        """
        Test to create user and update email with bad email

        :param self: instance of the class
        """
        user = User("John", "Doe", "john.doe@example.com")

        try:
            user.email = "invalid@email"
        except BadRequest:
            return self.assertTrue(True)

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
