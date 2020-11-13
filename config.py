import os
DATABASE_URI = 'postgres://jpkvgsekzvacjd:c77ece78d8692ec1c55f7a00e3d2fb69193e1f99323a778650955070526ff1b3@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/dtqr7hcn2fosr'
PROD_DATABASE_URI = 'postgres://jpkvgsekzvacjd:c77ece78d8692ec1c55f7a00e3d2fb69193e1f99323a778650955070526ff1b3@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/dtqr7hcn2fosr'
DEV_DATABASE_URI = 'postgres://kawakuticode@localhost:5432/angola_web'


class Config:
    """Base config."""
    # SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    SECRET_KEY = os.urandom(32)
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):

    SECRET_KEY = os.urandom(32)
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = PROD_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevConfig(Config):

    SECRET_KEY = os.urandom(32)
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

    # Database
    SQLALCHEMY_DATABASE_URI = DEV_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
