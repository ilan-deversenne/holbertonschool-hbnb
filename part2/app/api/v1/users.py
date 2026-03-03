from flask_restx import Namespace, Resource, fields
from app.services import facade
from datetime import datetime
from re import match


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
dict_user_model = {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
}
user_model = api.model('User', dict_user_model)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if len(user_data['first_name'].strip()) < 3 or len(user_data['first_name'].strip()) > 50:
            return {'error': 'Invalid input data'}, 400

        if len(user_data['last_name'].strip()) < 3 or len(user_data['last_name'].strip()) > 50:
            return {'error': 'Invalid input data'}, 400

        ## Check if its real email pattern (with Regex)
        pattern = r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"
        valid = match(pattern, user_data["email"])

        if not valid:
            return {'error': 'Invalid input data'}, 400

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        def test(pair):
            key, value = pair
            return key in dict_user_model.keys()

        new_user = facade.create_user(dict(filter(test, user_data.items())))

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'updated_at': int(datetime.timestamp(new_user.updated_at)),
            'created_at': int(datetime.timestamp(new_user.created_at))
        }, 201

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self):
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'updated_at': int(datetime.timestamp(user.updated_at)),
            'created_at': int(datetime.timestamp(user.created_at))
        } for user in facade.get_all_users()]

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'updated_at': int(datetime.timestamp(user.updated_at)),
            'created_at': int(datetime.timestamp(user.created_at))
        }, 200
