from flask_restx import Namespace, Resource, fields
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

        if not data['text'] or len(data['text'].strip()) < 8:
            return {'error': 'Invalid input data'}, 400

        if data['rating'] < 0 or data['rating'] > 5:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Invalid input data'}, 400

        if facade.get_user(data['user_id']) == None:
            return {'error': 'Invalid input data'}, 400

        def test(pair):
            key, value = pair
            return key in dict_review_model.keys()

        review = facade.create_review(dict(filter(test, data.items())))

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
        result = []
        reviews = facade.get_all_reviews()
        for review in reviews:
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'updated_at': int(datetime.timestamp(review.updated_at)),
                'created_at': int(datetime.timestamp(review.created_at))
            })

        return result

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'updated_at': int(datetime.timestamp(review.updated_at)),
                'created_at': int(datetime.timestamp(review.created_at))
            }

        reviews = facade.get_reviews_by_place(review_id)
        if not review or len(reviews) == 0:
            return {'error': 'Review not found'}, 404

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'updated_at': int(datetime.timestamp(review.updated_at)),
            'created_at': int(datetime.timestamp(review.created_at))

        } for review in reviews]

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        if len(data['text'].strip()) < 8:
            return {'error': 'Invalid input data'}, 400

        if data['rating'] < 0 or data['rating'] > 5:
            return {'error': 'Invalid input data'}

        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Invalid input data'}, 400

        facade.update_review(review_id, data)

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not facade.get_review(review_id):
            return {'error': 'Review not found'}, 404

        facade.delete_review(review_id)
        return {'message': 'Review deleted'}
