#!/usr/bin/python3

from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.user_repository import UserRepository
from app.api.exceptions import BadRequest, NotFound
from app.models.place import Place, User
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()


    ##############################################
    ##                  Place                   ##
    ##############################################

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if owner is None:
            raise NotFound("Owner not found")

        amenity_ids = place_data.get('amenities', [])
        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity is None:
                raise NotFound("Amenity not found")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            user_id=place_data['owner_id']
        )

        place.add_amenities(amenities)
        self.place_repo.add(place)

        return place


    def get_place(self, place_id: str):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)

        if place is None:
            raise NotFound("Place not found")

        clean_data = place_data.copy()

        if 'owner_id' in clean_data:
            owner = self.user_repo.get(clean_data['owner_id'])
            if owner is None:
                raise NotFound("Owner not found")
            clean_data['owner'] = owner
            del clean_data['owner_id']

        if 'amenities' in clean_data:
            amenities = []
            for amenity_id in clean_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity is None:
                    raise NotFound("Amenity {} not found".format(amenity_id))
                amenities.append(amenity)

            clean_data['amenities'] = amenities

        place.update(clean_data)

        self.place_repo.update(place_id, place)


    ##############################################
    ##                  User                    ##
    ##############################################

    def create_user(self, user_data):
        if self.user_repo.get_user_by_email(user_data['email']):
            raise BadRequest('Email already registered')

        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)

        return user

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

        user = self.user_repo.get(user_id)
        if not user:
            raise NotFound('User not found')

        return user

    def get_all_users(self) -> dict[User]:
        return self.user_repo.get_all()

    def get_user(self, user_id: str) -> User:
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFound('User not found')

        return user

    def get_user_by_email(self, email: str) -> User:
        return self.user_repo.get_by_attribute('email', email)


    ##############################################
    ##                 Amenity                  ##
    ##############################################

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise NotFound('Amenity not found')

        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise NotFound('Amenity not found')

        return amenity


    ##############################################
    ##                 Review                   ##
    ##############################################

    def create_review(self, review_data: dict):
        review_data['user'] = self.get_user(review_data['user_id'])
        review_data['place'] = self.get_place(review_data['place_id'])
        del review_data['user_id']
        del review_data['place_id']

        if not review_data['user'] or not review_data['place']:
            raise BadRequest('Invalid input data')

        review = Review(**review_data)
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise NotFound('Review not found')

        return review

    def get_all_reviews(self) -> dict:
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str):
        result = []
        for review in self.review_repo.get_all():
            if review.place_id == place_id:
                result.append(review)

        return result

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

        review = self.review_repo.get(review_id)
        if not review:
            raise NotFound('Review not found')

        return review

    def delete_review(self, review_id):
        if not self.review_repo.get(review_id):
            raise NotFound('Review not found')

        self.review_repo.delete(review_id)
