import os

DATABASE_URI = 'postgres://clsqdvzjgrdnph:d2edd909c3ebda2c1a429b6ea009e1296146f6c12673ab3309146e7a5cbd1f60@ec2-34-248-165-3.eu-west-1.compute.amazonaws.com:5432/d3eb1j101k1dhm'
PROD_DATABASE_URI = 'postgres://clsqdvzjgrdnph:d2edd909c3ebda2c1a429b6ea009e1296146f6c12673ab3309146e7a5cbd1f60@ec2-34-248-165-3.eu-west-1.compute.amazonaws.com:5432/d3eb1j101k1dhm'
DEV_DATABASE_URI = 'postgres://kawakuticode@localhost:5432/angola_web'


class Config:
    """Base config."""
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
