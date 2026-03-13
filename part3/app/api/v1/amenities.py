from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
dict_amenity_model = {
    'name': fields.String(required=True, description='Name of the amenity')
}
amenity_model = api.model('Amenity', dict_amenity_model)

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized user')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401
        
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        def test(pair):
            key, value = pair
            return key in dict_amenity_model.keys()
        try:
            new_amenity = facade.create_amenity(dict(filter(test, amenity_data.items())))
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(401, 'Unauthorized user')
    @jwt_required()
    def get(self):
        """Retrieve a list of all amenities"""
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

        amenities = facade.get_all_amenities()
        list_amenities = [{
                "id": amenity.id,
                "name": amenity.name
            } for amenity in amenities
        ]
        return list_amenities, 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.response(401, 'Unauthorized user')
    @jwt_required()
    def get(self, amenity_id):
        """Get amenity details by ID"""
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

        try:
            amenity = facade.get_amenity(amenity_id)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized user')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401
        
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        

        def test(pair):
            key, value = pair
            return key in dict_amenity_model.keys()

        try:
            amenity = facade.update_amenity(amenity_id, dict(filter(test, amenity_data.items())))
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {'id': amenity.id, 'name': amenity.name}, 200
