#!/usr/bin/env python3

from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Boolean, String
from app.models.baseclass import BaseModel
from app.api.exceptions import BadRequest
from app import db, bcrypt
from re import match


class User(BaseModel):
    """
    Docstring for User
    """

    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    places_owned = relationship('Place', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool=False):
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

    @validates("first_name")
    def validate_first_name(self, key: str, value: str):
        if len(value.strip()) < 3 or len(value.strip()) > 50:
            raise BadRequest('Invalid input data')

        return value

    @validates("last_name")
    def validate_last_name(self, key: str, value: str):
        if len(value.strip()) < 3 or len(value.strip()) > 50:
            raise BadRequest('Invalid input data')

        return value

    @validates("email")
    def validate_email(self, key: str, value: str):
        if not self.__check_email_regex(value):
            raise BadRequest('Invalid input data')

        return value

    def __check_email_regex(self, email: str) -> bool:
        """
        Docstring for __check_email_regex

        :param self: instance of the class
        :param email: Email to check
        """
        pattern = r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"
        return match(pattern, email) is not None

    def hash_password(self, password: str):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
