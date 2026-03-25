#!/usr/bin/env python3

from sqlalchemy import Table, Column, Float, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from app.models.baseclass import BaseModel
from app.api.exceptions import BadRequest
from app.models.amenity import Amenity
from app.models.user import User
from app import db

# Table for relationship between place and amenity
place_amenity = Table('place_amenity', db.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    amenities = relationship('Course', secondary=place_amenity, lazy='subquery',
                           backref=db.backref('places', lazy=True))


    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float, user_id: str):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.reviews = []
        self.amenities = []

    @validates("title")
    def validate_title(self, key: str, value: str):
        if not value or len(value.strip()) < 3 or len(value.strip()) > 100:
            raise BadRequest('Invalid input data')

        return value

    @validates("description")
    def validate_description(self, key: str, value: str):
        if not value or len(value) > 500:
            return ""

        return value

    @validates("price")
    def validate_price(self, key: str, value: str):
        if not type(value) in (int, float) or value < 0 or value > 1.0e12:
            raise BadRequest('Invalid input data')

        return value

    @validates("latitude")
    def validate_latitude(self, key: str, value: str):
        if not type(value) in (int, float) or value < -90 or value > 90:
            raise BadRequest('Invalid input data')

        return float(value)

    @validates("longitude")
    def validate_longitude(self, key: str, value: str):
        if not type(value) in (int, float) or value < -180 or value > 180:
            raise BadRequest('Invalid input data')

        return float(value)

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_amenities(self, amenities: list[Amenity]):
        for amenity in amenities:
            self.add_amenity(amenity)
