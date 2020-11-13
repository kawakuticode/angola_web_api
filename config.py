import os
DATABASE_URI = 'postgres://idmeieufmbqydw:ea6f51abb4056d53c5c908f8fc5b302e32aeca6b0dc2a56cc1f9c706b20ddaab@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/df6346qe2d6qjf'
PROD_DATABASE_URI = 'postgres://idmeieufmbqydw:ea6f51abb4056d53c5c908f8fc5b302e32aeca6b0dc2a56cc1f9c706b20ddaab@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/df6346qe2d6qjf'
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
