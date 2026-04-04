#!/usr/bin/env python3

from app.models.baseclass import BaseModel
from app.api.exceptions import BadRequest
from sqlalchemy.orm import validates
from app import db


class Amenity(BaseModel):
    """
    Docstring: Class Amenity
    """

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        """
        Methode __init__

        :param name: Name
        """
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) < 3 or len(value) > 50:
            raise BadRequest('Invalid input data')

        return value
