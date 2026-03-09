from flask_restx import Namespace, Resource, fields
from app.services import facade
from datetime import datetime

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
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        def test(pair):
            key, value = pair
            return key in dict_user_model.keys()

        try:
            new_user = facade.create_user(dict(filter(test, user_data.items())))
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

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
        try:
            user = facade.get_user(user_id)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'updated_at': int(datetime.timestamp(user.updated_at)),
            'created_at': int(datetime.timestamp(user.created_at))
        }, 200

    @api.response(200, 'User has been updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        data = api.payload

        try:
            user = facade.update_user(user_id, data)
        except Exception as e:
            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'updated_at': int(datetime.timestamp(user.updated_at)),
            'created_at': int(datetime.timestamp(user.created_at))
        }, 200
