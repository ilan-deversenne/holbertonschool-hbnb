from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity
from app import db


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
