from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        def test(pair):
            key, value = pair
            return key in dict_amenity_model.keys()
 
        new_amenity = facade.create_amenity(dict(filter(test, amenity_data.items())))
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
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
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)

        if facade.get_amenity(amenity_id) is None:
            return {'error': 'Amenity not found'}, 404

        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        if not amenity_data['name'] or len(amenity_data['name'].strip()) < 2:
            return {'error': 'Invalid input data'}, 400

        if facade.get_amenity(amenity_id) is None:
            return {'error': 'Amenity not found'}, 404

        def test(pair):
            key, value = pair
            return key in dict_amenity_model.keys()
        amenity = facade.update_amenity(amenity_id, dict(filter(test, amenity_data.items())))

        return {'id': amenity.id, 'name': amenity.name}, 200
