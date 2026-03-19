#!/usr/bin/env python3

from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.baseclass import BaseModel
from app.api.exceptions import BadRequest
from app.models.place import Place, User
from sqlalchemy.orm import validates, relationship
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place = relationship('Place', backref='review', lazy=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)

    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @validates("text")
    def validate_text(self, value: str):
        if len(value.strip()) < 8:
            raise BadRequest('Invalid input data')

        return value

    @validates("rating")
    def validate_rating(self, value: int):
        if value < 1 or value > 5:
            raise BadRequest('Invalid input data')

        return value
