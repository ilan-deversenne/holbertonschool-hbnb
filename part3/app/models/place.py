#!/usr/bin/env python3

from app.models.base_model import BaseModel
from app.models.amenity import Amenity
from app.models.user import User
from app.api.exceptions import BadRequest


class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: 'User'):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        self.add_place_to_owner()

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value or len(value.strip()) < 3 or len(value.strip()) > 100:
            raise BadRequest('Invalid input data')
        self.__title = value.strip()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not value or len(value) > 500:
            self.__description = ""
        else:
            self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not type(value) in (int, float) or value < 0 or value > 1.0e12:
            raise BadRequest('Invalid input data')
        self.__price = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not type(value) in (int, float) or value < -90 or value > 90:
            raise BadRequest('Invalid input data')
        self.__latitude = float(value)

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not type(value) in (int, float) or value < -180 or value > 180:
            raise BadRequest('Invalid input data')
        self.__longitude = float(value)

    @property
    def owner_id(self):
        return self.owner.id

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_amenities(self, amenities: list[Amenity]):
        for amenity in amenities:
            self.add_amenity(amenity)

    def add_place_to_owner(self):
        self.owner.places_owned.append(self)