from flask_restx import Namespace, Resource, fields
from app.services import facade
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description'),
    'price': fields.Float(required=True, min=0),
    'latitude': fields.Float(required=True, min=-90, max=90),
    'longitude': fields.Float(required=True, min=-180, max=180),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})


@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized user')
    @jwt_required()
    def post(self):
        """Create a new place"""
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

        place = facade.create_place(api.payload)

        try:
            

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.user_id,
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    } for amenity in place.amenities
                ]
            }, 201

        except Exception as e:
            print(e)

            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get all places"""

        places = facade.get_all_places()

        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description
            'price': place.price
            'latitude': place.latitude,
            'longitude': place.longitude,
            'created_at': int(datetime.timestamp(place.created_at)),
            'updated_at': int(datetime.timestamp(place.updated_at))
        } for place in places]

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in place.amenities
            ],
            'created_at': int(datetime.timestamp(place.created_at)),
            'updated_at': int(datetime.timestamp(place.updated_at))
        }

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized user')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update place"""
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

        place = facade.get_place(place_id)
        if actual_user != place['owner_id'] or not actual_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_place(place_id, api.payload)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {"message": "Place updated successfully"}, 200