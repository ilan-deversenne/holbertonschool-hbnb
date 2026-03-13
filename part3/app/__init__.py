#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask import Flask
import config
from flask_jwt_extended import JWTManager
import datetime

jwt = JWTManager()

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as login_ns

    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=60)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(login_ns, path='/api/v1')

    return app
