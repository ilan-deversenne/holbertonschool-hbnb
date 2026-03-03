#!/usr/bin/env python3

from app.models.base_model import BaseModel
from app.api.exceptions import BadRequest
from re import match

class User(BaseModel):
    """
    Docstring for User
    """
    # we will have to import an email validator (maybe regex)
    def __init__(self, first_name: str, last_name: str, email, is_admin: bool=False):
        """
        Docstring for __init__

        :param self: instance of the class
        :param first_name: e.g Elliot
        :param last_name: e.g CHARLET
        :param email: email that respect the email validator
        :param is_admin: bool that is set to false by default
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places_owned = []

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        if len(value.strip()) < 3:
            raise BadRequest('Invalid input data')

        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        if len(value.strip()) < 3:
            raise BadRequest('Invalid input data')

        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):
        if not self.__check_email_regex(value):
            raise BadRequest('Invalid input data')

        self.__email = value

    def __check_email_regex(self, email: str) -> bool:
        """
        Docstring for __check_email_regex

        :param self: instance of the class
        :param email: Email to check
        """
        pattern = r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"
        return match(pattern, email) is not None
