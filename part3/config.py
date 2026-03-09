import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-dev-3Ap5U43NcuL8Nk3f')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}