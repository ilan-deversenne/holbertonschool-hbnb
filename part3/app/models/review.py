#!/usr/bin/env python3

from app.models.base_model import BaseModel
from app.models.place import Place, User

from app.api.exceptions import BadRequest

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        if len(value.strip()) < 8:
            raise BadRequest('Invalid input data')

        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: int):
        if value < 1 or value > 5:
            raise BadRequest('Invalid input data')

        self.__rating = value
