from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade
from datetime import datetime

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
dict_user_model = {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
}
user_model = api.model('User', dict_user_model)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'updated_at': int(datetime.timestamp(new_user.updated_at)),
                'created_at': int(datetime.timestamp(new_user.created_at))
            }, 201

        except Exception as e:
            print(e)

            if hasattr(e, 'httpcode'):
                return {'error': str(e)}, e.httpcode

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self):
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

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
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401

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
    @api.response(401, 'Unauthorized user')
    @api.response(400, 'You cannot modify email or password.')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        data = api.payload

        actual_user = get_jwt_identity()
        if not actual_user:
            return {'error': 'Unauthorized user'}, 401
        
        # you can't change the email or the password of the user
        the_user_to_modify = facade.get_user(user_id)
        if data['email'] != the_user_to_modify['email'] or data['password'] != the_user_to_modify['password']:
            return {'error', 'You cannot modify email or password.'}, 400

        # verify the current user has admin privilege
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # antoher user can't modify someone else
        if actual_user != data['user_id']:
            return {'error': 'Unauthorized action.'}, 403

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
