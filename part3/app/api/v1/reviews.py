from flask_restx import Namespace, Resource, fields
from app.api.exceptions import NotFound
from app.services import facade
from datetime import datetime

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
dict_review_model = {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
}
review_model = api.model('Review', dict_review_model)

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload

        def test(pair):
            key, value = pair
            return key in dict_review_model.keys()

        try:
            review = facade.create_review(dict(filter(test, data.items())))
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'updated_at': int(datetime.timestamp(review.updated_at)),
            'created_at': int(datetime.timestamp(review.created_at))
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'updated_at': int(datetime.timestamp(review.updated_at)),
            'created_at': int(datetime.timestamp(review.created_at))
        } for review in facade.get_all_reviews()]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'updated_at': int(datetime.timestamp(review.updated_at)),
                'created_at': int(datetime.timestamp(review.created_at))
            }

        except NotFound:
            try:
                reviews = facade.get_reviews_by_place(review_id)
                return [{
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id,
                    'place_id': review.place.id,
                    'updated_at': int(datetime.timestamp(review.updated_at)),
                    'created_at': int(datetime.timestamp(review.created_at))
                } for review in reviews]

            except Exception as e:
                if hasattr(e, 'httpcode'):
                    return {'error': str(e)}, e.httpcode

        except Exception as e:
                if hasattr(e, 'httpcode'):
                    return {'error': str(e)}, e.httpcode

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        try:
            review = facade.update_review(review_id, data)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {'message': 'Review updated successfully'}

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {'message': 'Review deleted'}
