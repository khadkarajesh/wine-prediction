from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'api/.env'))


class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DB_SERVER = '192.168.1.56'


class ProductionConfig(Config):
    DB_SERVER = ''
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{environ.get('USER_NAME')}:{environ.get('USER_PASSWORD')}@{DB_SERVER}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')} "


class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'
