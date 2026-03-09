#!/usr/bin/env python3

from app.models.base_model import BaseModel
from app.api.exceptions import BadRequest

class Amenity(BaseModel):
    """
    Docstring: Class Amenity
    """
    def __init__(self, name: str):
        """
        Methode __init__

        :param name: Name
        """
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value or len(value) < 3 or len(value) > 50:
            raise BadRequest('Invalid input data')

        self.__name = value
