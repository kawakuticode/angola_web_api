import os
DATABASE_URI = 'postgres://kawakuticode@localhost:5432/angola_web'
PROD_DATABASE_URI = 'postgres://wsteasfakevqhq:3cae8bc967753884fde1db46469c5736064a47813a9923327126e60668d11aa2@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/d13tl0r9i43etv'
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
